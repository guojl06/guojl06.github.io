/*
 * =============================================================================
 * MVC — Model（模型层）实现
 * 棋盘坐标：rank 0 为白方底线，rank 7 为黑方底线；file 0=a，file 7=h。
 * =============================================================================
 */

#include "model/ChessModel.h"

#include <algorithm>

namespace {

inline int sign(ChessColor c) { return c == ChessColor::White ? 1 : -1; }

}  // namespace

Piece ChessModel::pieceAt(Square s) const {
    if (!s.valid()) return {};
    return board_[s.r][s.f];
}

Piece ChessModel::pieceAt(int file, int rank) const { return pieceAt(Square::fromFR(file, rank)); }

void ChessModel::reset() {
    for (int r = 0; r < 8; ++r)
        for (int f = 0; f < 8; ++f) board_[r][f] = {};

    const auto put = [this](int f, int r, PieceType t, ChessColor c) { board_[r][f] = {t, c}; };

    put(0, 0, PieceType::Rook, ChessColor::White);
    put(1, 0, PieceType::Knight, ChessColor::White);
    put(2, 0, PieceType::Bishop, ChessColor::White);
    put(3, 0, PieceType::Queen, ChessColor::White);
    put(4, 0, PieceType::King, ChessColor::White);
    put(5, 0, PieceType::Bishop, ChessColor::White);
    put(6, 0, PieceType::Knight, ChessColor::White);
    put(7, 0, PieceType::Rook, ChessColor::White);
    for (int f = 0; f < 8; ++f) put(f, 1, PieceType::Pawn, ChessColor::White);

    put(0, 7, PieceType::Rook, ChessColor::Black);
    put(1, 7, PieceType::Knight, ChessColor::Black);
    put(2, 7, PieceType::Bishop, ChessColor::Black);
    put(3, 7, PieceType::Queen, ChessColor::Black);
    put(4, 7, PieceType::King, ChessColor::Black);
    put(5, 7, PieceType::Bishop, ChessColor::Black);
    put(6, 7, PieceType::Knight, ChessColor::Black);
    put(7, 7, PieceType::Rook, ChessColor::Black);
    for (int f = 0; f < 8; ++f) put(f, 6, PieceType::Pawn, ChessColor::Black);

    side_ = ChessColor::White;
    status_ = GameStatus::Playing;
    castleWK_ = castleWQ_ = castleBK_ = castleBQ_ = true;
    epTarget_ = {-1, -1};
    clearSelection();
    undoStack_.clear();
    recomputeStatus();
}

void ChessModel::clearSelection() {
    selected_ = {-1, -1};
    legalTargets_.clear();
}

void ChessModel::selectSquare(Square sq) {
    selected_ = sq;
    legalTargets_.clear();
    if (!sq.valid()) return;
    collectLegalMovesFrom(sq, legalTargets_);
}

bool ChessModel::inCheck() const { return kingInCheck(side_); }

bool ChessModel::kingInCheck(ChessColor who) const {
    Square k{-1, -1};
    for (int r = 0; r < 8; ++r)
        for (int f = 0; f < 8; ++f) {
            const Piece p = board_[r][f];
            if (!p.empty() && p.color == who && p.type == PieceType::King) {
                k = Square::fromFR(f, r);
                break;
            }
        }
    if (!k.valid()) return false;
    return squareAttacked(k, opposite(who));
}

bool ChessModel::squareAttacked(Square sq, ChessColor by) const {
    const int tf = sq.f, tr = sq.r;

    const int pawnDir = sign(by);
    const int pr = tr - pawnDir;
    if (pr >= 0 && pr < 8) {
        for (int df : {-1, 1}) {
            const int nf = tf + df;
            if (nf < 0 || nf >= 8) continue;
            const Piece p = board_[pr][nf];
            if (!p.empty() && p.color == by && p.type == PieceType::Pawn) return true;
        }
    }

    const int kdf[] = {-2, -1, 1, 2, 2, 1, -1, -2};
    const int kdr[] = {1, 2, 2, 1, -1, -2, -2, -1};
    for (int i = 0; i < 8; ++i) {
        const int nf = tf + kdf[i], nr = tr + kdr[i];
        if (nf < 0 || nf >= 8 || nr < 0 || nr >= 8) continue;
        const Piece p = board_[nr][nf];
        if (!p.empty() && p.color == by && p.type == PieceType::Knight) return true;
    }

    const int rdf[] = {1, -1, 0, 0, 1, 1, -1, -1};
    const int rdr[] = {0, 0, 1, -1, 1, -1, 1, -1};
    for (int d = 0; d < 8; ++d) {
        for (int n = 1; n < 8; ++n) {
            const int nf = tf + rdf[d] * n, nr = tr + rdr[d] * n;
            if (nf < 0 || nf >= 8 || nr < 0 || nr >= 8) break;
            const Piece p = board_[nr][nf];
            if (p.empty()) continue;
            if (p.color != by) break;
            if (p.type == PieceType::Queen) return true;
            if (p.type == PieceType::Rook && d < 4) return true;
            if (p.type == PieceType::Bishop && d >= 4) return true;
            break;
        }
    }

    for (int df = -1; df <= 1; ++df)
        for (int dr = -1; dr <= 1; ++dr) {
            if (df == 0 && dr == 0) continue;
            const int nf = tf + df, nr = tr + dr;
            if (nf < 0 || nf >= 8 || nr < 0 || nr >= 8) continue;
            const Piece p = board_[nr][nf];
            if (!p.empty() && p.color == by && p.type == PieceType::King) return true;
        }

    return false;
}

void ChessModel::collectPseudoLegal(Square src, std::vector<Square>& out) const {
    out.clear();
    if (!src.valid()) return;
    const Piece me = pieceAt(src);
    if (me.empty() || me.color != side_) return;

    const int f0 = src.f, r0 = src.r;
    const int fwd = sign(me.color);

    auto addIfEmptyOrEnemy = [&](int tf, int tr) {
        if (tf < 0 || tf >= 8 || tr < 0 || tr >= 8) return;
        const Piece t = board_[tr][tf];
        if (t.empty() || t.color != me.color) out.push_back(Square::fromFR(tf, tr));
    };

    switch (me.type) {
        case PieceType::Pawn: {
            const int r1 = r0 + fwd;
            if (r1 >= 0 && r1 < 8 && board_[r1][f0].empty()) {
                out.push_back(Square::fromFR(f0, r1));
                const int startRank = me.color == ChessColor::White ? 1 : 6;
                const int r2 = r0 + 2 * fwd;
                if (r0 == startRank && board_[r2][f0].empty()) out.push_back(Square::fromFR(f0, r2));
            }
            for (int df : {-1, 1}) {
                const int tf = f0 + df, tr = r0 + fwd;
                if (tf < 0 || tf >= 8 || tr < 0 || tr >= 8) continue;
                const Piece t = board_[tr][tf];
                if (!t.empty() && t.color != me.color) out.push_back(Square::fromFR(tf, tr));
                if (epTarget_.valid() && epTarget_.f == tf && epTarget_.r == tr && t.empty())
                    out.push_back(Square::fromFR(tf, tr));
            }
            break;
        }
        case PieceType::Knight: {
            const int kdf[] = {-2, -1, 1, 2, 2, 1, -1, -2};
            const int kdr[] = {1, 2, 2, 1, -1, -2, -2, -1};
            for (int i = 0; i < 8; ++i) addIfEmptyOrEnemy(f0 + kdf[i], r0 + kdr[i]);
            break;
        }
        case PieceType::Bishop:
        case PieceType::Rook:
        case PieceType::Queen: {
            const int dirs = (me.type == PieceType::Bishop) ? 4 : (me.type == PieceType::Rook) ? 4 : 8;
            const int start = (me.type == PieceType::Bishop) ? 4 : 0;
            const int rdf[] = {1, -1, 0, 0, 1, 1, -1, -1};
            const int rdr[] = {0, 0, 1, -1, 1, -1, 1, -1};
            for (int d = start; d < start + dirs; ++d) {
                for (int n = 1; n < 8; ++n) {
                    const int tf = f0 + rdf[d] * n, tr = r0 + rdr[d] * n;
                    if (tf < 0 || tf >= 8 || tr < 0 || tr >= 8) break;
                    const Piece t = board_[tr][tf];
                    if (t.empty()) {
                        out.push_back(Square::fromFR(tf, tr));
                        continue;
                    }
                    if (t.color != me.color) out.push_back(Square::fromFR(tf, tr));
                    break;
                }
            }
            break;
        }
        case PieceType::King: {
            for (int df = -1; df <= 1; ++df)
                for (int dr = -1; dr <= 1; ++dr) {
                    if (df == 0 && dr == 0) continue;
                    addIfEmptyOrEnemy(f0 + df, r0 + dr);
                }
            if (!kingInCheck(me.color)) {
                if (me.color == ChessColor::White && r0 == 0 && f0 == 4) {
                    if (castleWK_ && board_[0][5].empty() && board_[0][6].empty() && board_[0][7].type == PieceType::Rook &&
                        board_[0][7].color == ChessColor::White) {
                        const Square s5 = Square::fromFR(5, 0), s6 = Square::fromFR(6, 0);
                        if (!squareAttacked(Square::fromFR(4, 0), ChessColor::Black) && !squareAttacked(s5, ChessColor::Black) &&
                            !squareAttacked(s6, ChessColor::Black))
                            out.push_back(s6);
                    }
                    if (castleWQ_ && board_[0][1].empty() && board_[0][2].empty() && board_[0][3].empty() &&
                        board_[0][0].type == PieceType::Rook && board_[0][0].color == ChessColor::White) {
                        const Square s2 = Square::fromFR(2, 0), s3 = Square::fromFR(3, 0);
                        if (!squareAttacked(Square::fromFR(4, 0), ChessColor::Black) && !squareAttacked(s3, ChessColor::Black) &&
                            !squareAttacked(s2, ChessColor::Black))
                            out.push_back(s2);
                    }
                }
                if (me.color == ChessColor::Black && r0 == 7 && f0 == 4) {
                    if (castleBK_ && board_[7][5].empty() && board_[7][6].empty() && board_[7][7].type == PieceType::Rook &&
                        board_[7][7].color == ChessColor::Black) {
                        const Square s5 = Square::fromFR(5, 7), s6 = Square::fromFR(6, 7);
                        if (!squareAttacked(Square::fromFR(4, 7), ChessColor::White) && !squareAttacked(s5, ChessColor::White) &&
                            !squareAttacked(s6, ChessColor::White))
                            out.push_back(s6);
                    }
                    if (castleBQ_ && board_[7][1].empty() && board_[7][2].empty() && board_[7][3].empty() &&
                        board_[7][0].type == PieceType::Rook && board_[7][0].color == ChessColor::Black) {
                        const Square s2 = Square::fromFR(2, 7), s3 = Square::fromFR(3, 7);
                        if (!squareAttacked(Square::fromFR(4, 7), ChessColor::White) && !squareAttacked(s3, ChessColor::White) &&
                            !squareAttacked(s2, ChessColor::White))
                            out.push_back(s2);
                    }
                }
            }
            break;
        }
        default:
            break;
    }
}

void ChessModel::collectLegalMovesFrom(Square src, std::vector<Square>& out) const {
    std::vector<Square> tmp;
    collectPseudoLegal(src, tmp);
    out.clear();
    for (Square dst : tmp) {
        ChessModel copy = *this;
        copy.undoStack_.clear();
        const PieceType promo =
            (pieceAt(src).type == PieceType::Pawn && (dst.r == 7 || dst.r == 0)) ? PieceType::Queen : PieceType::None;
        if (!copy.applyMove(src, dst, promo)) continue;
        if (!copy.kingInCheck(side_)) out.push_back(dst);
        while (!copy.undoStack_.empty()) copy.undoMove();
    }
}

bool ChessModel::hasAnyLegalMove(ChessColor who) const {
    const ChessColor saveSide = side_;
    const_cast<ChessModel*>(this)->side_ = who;
    for (int r = 0; r < 8; ++r)
        for (int f = 0; f < 8; ++f) {
            const Piece p = board_[r][f];
            if (p.empty() || p.color != who) continue;
            std::vector<Square> leg;
            collectLegalMovesFrom(Square::fromFR(f, r), leg);
            if (!leg.empty()) {
                const_cast<ChessModel*>(this)->side_ = saveSide;
                return true;
            }
        }
    const_cast<ChessModel*>(this)->side_ = saveSide;
    return false;
}

void ChessModel::recomputeStatus() {
    const bool check = kingInCheck(side_);
    if (!hasAnyLegalMove(side_)) {
        if (check)
            // 轮到走棋的一方无子可动且被将军 → 对方获胜
            status_ = (side_ == ChessColor::White) ? GameStatus::CheckmateBlack : GameStatus::CheckmateWhite;
        else
            status_ = GameStatus::Stalemate;
    } else {
        status_ = GameStatus::Playing;
    }
}

std::string ChessModel::statusLine() const {
    std::string s = (side_ == ChessColor::White) ? "White to move" : "Black to move";
    if (status_ == GameStatus::CheckmateWhite) return "Checkmate — White wins";
    if (status_ == GameStatus::CheckmateBlack) return "Checkmate — Black wins";
    if (status_ == GameStatus::Stalemate) return "Stalemate — Draw";
    if (status_ == GameStatus::Draw) return "Draw";
    if (inCheck()) s += " (Check)";
    return s;
}

void ChessModel::handleBoardClick(int file, int rank) {
    if (status_ != GameStatus::Playing) return;
    const Square click = Square::fromFR(file, rank);
    if (!click.valid()) return;

    const Piece clicked = pieceAt(click);

    if (selected_.valid()) {
        const auto it = std::find(legalTargets_.begin(), legalTargets_.end(), click);
        if (it != legalTargets_.end()) {
            tryMove(selected_, click);
            return;
        }
    }

    if (!clicked.empty() && clicked.color == side_) {
        selectSquare(click);
        return;
    }

    clearSelection();
}

void ChessModel::tryMove(Square src, Square dst) {
    const Piece moving = pieceAt(src);
    PieceType promo = PieceType::None;
    if (moving.type == PieceType::Pawn && (dst.r == 0 || dst.r == 7)) promo = PieceType::Queen;
    if (!applyMove(src, dst, promo)) return;
    clearSelection();
    side_ = opposite(side_);
    recomputeStatus();
}

bool ChessModel::applyMove(Square src, Square dst, PieceType promoteTo) {
    const Piece me = pieceAt(src);
    if (me.empty()) return false;

    MoveUndo u{};
    u.fromSq = src;
    u.toSq = dst;
    u.mover = me;
    u.sideBefore = side_;
    u.castleWK = castleWK_;
    u.castleWQ = castleWQ_;
    u.castleBK = castleBK_;
    u.castleBQ = castleBQ_;
    u.epBefore = epTarget_;

    u.victim = pieceAt(dst);
    const bool epCapture = me.type == PieceType::Pawn && dst == epTarget_ && u.victim.empty();
    u.wasEnPassant = epCapture;
    if (epCapture) {
        const int capR = dst.r - sign(me.color);
        u.epRemoved = Square::fromFR(dst.f, capR);
        u.victim = pieceAt(u.epRemoved);
    }

    epTarget_ = {-1, -1};

    board_[src.r][src.f] = {};
    board_[dst.r][dst.f] = me;
    if (epCapture) board_[u.epRemoved.r][u.epRemoved.f] = {};

    if (me.type == PieceType::King) {
        if (me.color == ChessColor::White) {
            castleWK_ = castleWQ_ = false;
            if (src.f == 4 && src.r == 0 && dst.f == 6 && dst.r == 0) {
                board_[0][5] = board_[0][7];
                board_[0][7] = {};
            }
            if (src.f == 4 && src.r == 0 && dst.f == 2 && dst.r == 0) {
                board_[0][3] = board_[0][0];
                board_[0][0] = {};
            }
        } else {
            castleBK_ = castleBQ_ = false;
            if (src.f == 4 && src.r == 7 && dst.f == 6 && dst.r == 7) {
                board_[7][5] = board_[7][7];
                board_[7][7] = {};
            }
            if (src.f == 4 && src.r == 7 && dst.f == 2 && dst.r == 7) {
                board_[7][3] = board_[7][0];
                board_[7][0] = {};
            }
        }
    }

    if (me.type == PieceType::Rook) {
        if (me.color == ChessColor::White && src.r == 0) {
            if (src.f == 0) castleWQ_ = false;
            if (src.f == 7) castleWK_ = false;
        }
        if (me.color == ChessColor::Black && src.r == 7) {
            if (src.f == 0) castleBQ_ = false;
            if (src.f == 7) castleBK_ = false;
        }
    }

    if (!u.wasEnPassant && u.victim.type == PieceType::Rook) {
        if (dst.r == 0 && dst.f == 0) castleWQ_ = false;
        if (dst.r == 0 && dst.f == 7) castleWK_ = false;
        if (dst.r == 7 && dst.f == 0) castleBQ_ = false;
        if (dst.r == 7 && dst.f == 7) castleBK_ = false;
    }

    if (me.type == PieceType::Pawn && std::abs(static_cast<int>(dst.r) - static_cast<int>(src.r)) == 2)
        epTarget_ = Square::fromFR(src.f, static_cast<std::int8_t>((static_cast<int>(src.r) + static_cast<int>(dst.r)) / 2));

    if (promoteTo != PieceType::None && me.type == PieceType::Pawn && (dst.r == 0 || dst.r == 7)) board_[dst.r][dst.f].type = promoteTo;

    undoStack_.push_back(u);
    return true;
}

void ChessModel::undoMove() {
    if (undoStack_.empty()) return;
    const MoveUndo u = undoStack_.back();
    undoStack_.pop_back();

    castleWK_ = u.castleWK;
    castleWQ_ = u.castleWQ;
    castleBK_ = u.castleBK;
    castleBQ_ = u.castleBQ;
    epTarget_ = u.epBefore;
    side_ = u.sideBefore;

    if (u.mover.type == PieceType::King) {
        if (u.fromSq.f == 4 && u.fromSq.r == 0 && u.toSq.f == 6 && u.toSq.r == 0) {
            board_[0][7] = board_[0][5];
            board_[0][5] = {};
        }
        if (u.fromSq.f == 4 && u.fromSq.r == 0 && u.toSq.f == 2 && u.toSq.r == 0) {
            board_[0][0] = board_[0][3];
            board_[0][3] = {};
        }
        if (u.fromSq.f == 4 && u.fromSq.r == 7 && u.toSq.f == 6 && u.toSq.r == 7) {
            board_[7][7] = board_[7][5];
            board_[7][5] = {};
        }
        if (u.fromSq.f == 4 && u.fromSq.r == 7 && u.toSq.f == 2 && u.toSq.r == 7) {
            board_[7][0] = board_[7][3];
            board_[7][3] = {};
        }
    }

    if (u.wasEnPassant) {
        board_[u.toSq.r][u.toSq.f] = {};
        board_[u.epRemoved.r][u.epRemoved.f] = u.victim;
    } else {
        board_[u.toSq.r][u.toSq.f] = u.victim;
    }
    board_[u.fromSq.r][u.fromSq.f] = u.mover;
}
