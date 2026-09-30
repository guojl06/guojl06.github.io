/*
 * =============================================================================
 * MVC — View（视图层）
 * -----------------------------------------------------------------------------
 * 只负责“画出来”：棋盘、棋子、高亮、状态文字。只读 ChessModel，不修改规则数据。
 * 提供屏幕坐标到棋盘 file/rank 的转换，供 Controller 把鼠标事件交给 Model。
 * =============================================================================
 */
#pragma once

#include "raylib.h"
#include "model/ChessModel.h"

class ChessView {
public:
    ChessView() = default;

    void draw(const ChessModel& model) const;

    // 将屏幕像素映射到棋盘格子；false 表示点击在棋盘外
    bool screenToBoard(Vector2 screen, int& outFile, int& outRank) const;

private:
    //static constexpr float kMargin = 40.0f;
    static constexpr float kMargin = 60.0f;
    //static constexpr float kCell = 70.0f;
    static constexpr float kCell = 140.0f;
    static constexpr float kBoardSize = kCell * 8.0f;

    void drawBoardGeometry() const;
    void drawPiece(int file, int rank, Piece p) const;
    static Color raylibTintForPiece(Piece p);
    static const char* pieceLetter(PieceType t);
};
