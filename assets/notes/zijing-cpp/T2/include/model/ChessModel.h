/*
 * =============================================================================
 * MVC — Model（模型层）
 * -----------------------------------------------------------------------------
 * 只描述“棋局状态”与规则：棋盘、棋子、轮到谁走、是否将军/将杀/和棋、
 * 合法走法生成与执行。不依赖 raylib，不知道屏幕坐标或鼠标。
 * 由 Controller 调用以响应输入；由 View 只读查询用于绘制。
 * =============================================================================
 */
#pragma once

#include <cstdint>
#include <string>
#include <vector>

enum class ChessColor : std::uint8_t { White, Black };

enum class PieceType : std::uint8_t { None, Pawn, Rook, Knight, Bishop, Queen, King };

struct Piece {
    PieceType type = PieceType::None;
    ChessColor color = ChessColor::White;

    bool empty() const { return type == PieceType::None; }
};

struct Square {
    std::int8_t f = -1;  // file 0..7 (a..h)
    std::int8_t r = -1;  // rank 0..7 (白方底线 rank0，黑方底线 rank7)

    bool valid() const { return f >= 0 && f < 8 && r >= 0 && r < 8; }
    int index() const { return static_cast<int>(r) * 8 + static_cast<int>(f); }

    static Square fromFR(int file, int rank) {
        return {static_cast<std::int8_t>(file), static_cast<std::int8_t>(rank)};
    }

    friend bool operator==(Square a, Square b) { return a.f == b.f && a.r == b.r; }
    friend bool operator!=(Square a, Square b) { return !(a == b); }
};

enum class GameStatus : std::uint8_t { Playing, CheckmateWhite, CheckmateBlack, Stalemate, Draw };

class ChessModel {
public:
    ChessModel() { reset(); }

    void reset();

    ChessColor sideToMove() const { return side_; }
    GameStatus status() const { return status_; }
    Piece pieceAt(Square s) const;
    Piece pieceAt(int file, int rank) const;

    Square selected() const { return selected_; }
    const std::vector<Square>& legalTargets() const { return legalTargets_; }

    bool inCheck() const;
    std::string statusLine() const;

    // 由 Controller 传入棋盘格子坐标（已由 View 从屏幕转换）
    void handleBoardClick(int file, int rank);

private:
    Piece board_[8][8]{};
    ChessColor side_ = ChessColor::White;
    GameStatus status_ = GameStatus::Playing;

    // 王车易位权利：白短/白长/黑短/黑长
    bool castleWK_ = true, castleWQ_ = true, castleBK_ = true, castleBQ_ = true;
    Square epTarget_{-1, -1};  // 过路兵目标格（若无则为 invalid）

    Square selected_{-1, -1};
    std::vector<Square> legalTargets_;

    void recomputeStatus();
    void clearSelection();
    void selectSquare(Square sq);
    void tryMove(Square src, Square dst);

    bool applyMove(Square src, Square dst, PieceType promoteTo);
    void undoMove();  // 用于检测“送王”时试探走子

    struct MoveUndo {
        Square fromSq{};  // 不用名 from：Windows 头文件可能将 from 定义为宏
        Square toSq{};
        Piece mover{};
        Piece victim{};
        bool wasEnPassant = false;
        Square epRemoved{-1, -1};
        bool castleWK = false, castleWQ = false, castleBK = false, castleBQ = false;
        Square epBefore{-1, -1};
        ChessColor sideBefore = ChessColor::White;
    };
    std::vector<MoveUndo> undoStack_;

    bool kingInCheck(ChessColor who) const;
    bool squareAttacked(Square sq, ChessColor byAttacker) const;
    void collectLegalMovesFrom(Square src, std::vector<Square>& out) const;
    void collectPseudoLegal(Square src, std::vector<Square>& out) const;
    bool hasAnyLegalMove(ChessColor who) const;

    static ChessColor opposite(ChessColor c) {
        return c == ChessColor::White ? ChessColor::Black : ChessColor::White;
    }
};
