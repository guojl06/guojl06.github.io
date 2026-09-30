#pragma once
#include "raylib.h"
#include <cstdint>

namespace Config {
    constexpr int SW = 960, SH = 640;
    constexpr int LANES = 6;

    constexpr int KEY_MAP[LANES] = {KEY_S, KEY_D, KEY_F, KEY_J, KEY_K, KEY_L};
    constexpr const char* KEY_LABEL[LANES] = {"S", "D", "F", "J", "K", "L"};

    constexpr float LANE_W = 120.0f;
    constexpr float FIELD_X = (SW - LANES * LANE_W) / 2.0f;

    constexpr float VP_X = SW / 2.0f;
    constexpr float VP_Y = 15.0f;
    constexpr float HIT_Y = 530.0f;
    constexpr float TRACK_LEN = HIT_Y - VP_Y;
    constexpr float PERSP = 1.55f;
    constexpr float SCROLL_SPEED = 500.0f;

    constexpr float BPM = 140.0f;
    constexpr float BEAT = 60.0f / BPM;

    constexpr float JW_PERFECT = 0.045f;
    constexpr float JW_GREAT   = 0.09f;
    constexpr float JW_GOOD    = 0.14f;

    constexpr Color PASTEL[6] = {
        {255, 80, 140, 255}, {60, 140, 255, 255},
        {255, 170, 30, 255}, {30, 200, 140, 255},
        {180, 100, 255, 255}, {255, 130, 80, 255},
    };
    constexpr Color PASTEL_LIGHT[6] = {
        {255, 210, 225, 255}, {210, 230, 255, 255},
        {255, 238, 200, 255}, {210, 250, 230, 255},
        {235, 215, 255, 255}, {255, 225, 210, 255},
    };
    constexpr Color PASTEL_DIM[6] = {
        {40, 20, 35, 255}, {18, 25, 50, 255},
        {45, 30, 10, 255}, {12, 38, 28, 255},
        {30, 18, 45, 255}, {45, 25, 15, 255},
    };

    constexpr Color BG_CREAM   = {250, 245, 238, 255};
    constexpr Color ROSE_GOLD  = {225, 160, 135, 255};
    constexpr Color INK        = {80, 60, 70, 255};
    constexpr Color INK_LIGHT  = {160, 140, 150, 255};
}

enum class JudgeResult : std::uint8_t { NONE, PERFECT, GREAT, GOOD, MISS };
enum class NoteType  : std::uint8_t { TAP, HOLD };
