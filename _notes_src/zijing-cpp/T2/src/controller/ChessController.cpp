/*
 * =============================================================================
 * MVC — Controller（控制层）实现
 * =============================================================================
 */

#include "controller/ChessController.h"

void ChessController::update() {
    if (!IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) return;
    int f = 0, r = 0;
    if (!view_.screenToBoard(GetMousePosition(), f, r)) return;
    model_.handleBoardClick(f, r);
}
