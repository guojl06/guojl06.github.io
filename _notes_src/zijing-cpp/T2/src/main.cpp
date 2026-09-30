/*
 * 程序入口：组装 MVC（模型 / 视图 / 控制），并驱动 raylib 主循环。
 *
 * - Model:  ChessModel  — 棋局与规则
 * - View:   ChessView   — 绘制与坐标转换
 * - Controller: ChessController — 输入到模型的桥梁
 */

#include "controller/ChessController.h"
#include "model/ChessModel.h"
#include "view/ChessView.h"
#include "raylib.h"

int main() {
    const int winW = 1260;
    const int winH = 1400;
    InitWindow(winW, winH, "Chess — raylib + MVC");
    SetTargetFPS(60);

    ChessModel model;
    ChessView view;
    ChessController controller(model, view);

    while (!WindowShouldClose()) {
        controller.update();

        BeginDrawing();
        ClearBackground(Color{245, 245, 250, 255});
        view.draw(model);
        EndDrawing();
    }

    CloseWindow();
    return 0;
}
