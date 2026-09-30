/*
 * =============================================================================
 * MVC — Controller（控制层）
 * -----------------------------------------------------------------------------
 * 处理输入（鼠标），调用 Model 修改状态，并驱动 View 所需的一帧流程。
 * 不直接绘制；不包含走子规则（规则在 Model）。
 * =============================================================================
 */
#pragma once

#include "raylib.h"
#include "model/ChessModel.h"
#include "view/ChessView.h"

class ChessController {
public:
    ChessController(ChessModel& model, ChessView& view) : model_(model), view_(view) {}

    // 每帧：读取输入并交给 Model
    void update();

private:
    ChessModel& model_;
    ChessView& view_;
};
