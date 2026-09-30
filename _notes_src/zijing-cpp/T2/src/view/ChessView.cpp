/*
 * =============================================================================
 * MVC — View（视图层）实现：raylib 绘制
 * =============================================================================
 */

#include "view/ChessView.h"

void ChessView::draw(const ChessModel& model) const {
    drawBoardGeometry();

    for (int r = 0; r < 8; ++r)
        for (int f = 0; f < 8; ++f) {
            const Piece p = model.pieceAt(f, r);
            if (!p.empty()) drawPiece(f, r, p);
        }

    if (model.selected().valid()) {
        const Square sel = model.selected();
        const float x = kMargin + static_cast<float>(sel.f) * kCell;
        const float y = kMargin + static_cast<float>(7 - sel.r) * kCell;
        DrawRectangleLinesEx(Rectangle{x - 2, y - 2, kCell + 4, kCell + 4}, 4.0f, GOLD);
    }

    for (Square t : model.legalTargets()) {
        const float cx = kMargin + static_cast<float>(t.f) * kCell + kCell * 0.5f;
        const float cy = kMargin + static_cast<float>(7 - t.r) * kCell + kCell * 0.5f;
        DrawCircleV(Vector2{cx, cy}, kCell * 0.18f, Color{80, 200, 120, 160});
    }

    const float textY = kMargin + kBoardSize + 16.0f;
    DrawText(model.statusLine().c_str(), static_cast<int>(kMargin), static_cast<int>(textY), 22, DARKGRAY);
    DrawText("Click piece then destination. Pawn promotes to Queen.", static_cast<int>(kMargin),
             static_cast<int>(textY + 28), 18, GRAY);
}

bool ChessView::screenToBoard(Vector2 screen, int& outFile, int& outRank) const {
    const float x = screen.x - kMargin;
    const float y = screen.y - kMargin;
    if (x < 0 || y < 0 || x >= kBoardSize || y >= kBoardSize) return false;
    outFile = static_cast<int>(x / kCell);
    outRank = 7 - static_cast<int>(y / kCell);
    return outFile >= 0 && outFile < 8 && outRank >= 0 && outRank < 8;
}

void ChessView::drawBoardGeometry() const {
    for (int displayRow = 0; displayRow < 8; ++displayRow)
        for (int f = 0; f < 8; ++f) {
            const int r = 7 - displayRow;
            const bool light = ((f + r) % 2) == 0;
            const Color c = light ? Color{240, 217, 181, 255} : Color{181, 136, 99, 255};
            const float x = kMargin + static_cast<float>(f) * kCell;
            const float y = kMargin + static_cast<float>(displayRow) * kCell;
            DrawRectangleV(Vector2{x, y}, Vector2{kCell, kCell}, c);
        }
}

Color ChessView::raylibTintForPiece(Piece p) {
    return p.color == ChessColor::White ? RAYWHITE : Color{40, 40, 40, 255};
}

const char* ChessView::pieceLetter(PieceType t) {
    switch (t) {
        case PieceType::King:
            return "K";
        case PieceType::Queen:
            return "Q";
        case PieceType::Rook:
            return "R";
        case PieceType::Bishop:
            return "B";
        case PieceType::Knight:
            return "N";
        case PieceType::Pawn:
            return "P";
        default:
            return "?";
    }
}

void ChessView::drawPiece(int file, int rank, Piece p) const {
    const float x = kMargin + static_cast<float>(file) * kCell;
    const float y = kMargin + static_cast<float>(7 - rank) * kCell;
    const int fs = static_cast<int>(kCell * 0.62f);
    const char* ch = pieceLetter(p.type);
    const Color col = raylibTintForPiece(p);
    const Color outline = p.color == ChessColor::White ? BLACK : RAYWHITE;
    DrawText(ch, static_cast<int>(x + kCell * 0.28f), static_cast<int>(y + kCell * 0.18f), fs, outline);
    DrawText(ch, static_cast<int>(x + kCell * 0.26f), static_cast<int>(y + kCell * 0.16f), fs, col);
}
