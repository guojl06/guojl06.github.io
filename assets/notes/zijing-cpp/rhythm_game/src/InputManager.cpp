#include "InputManager.h"

std::vector<int> InputManager::pressedLanes() const {
    std::vector<int> lanes;
    for (int i = 0; i < Config::LANES; i++)
        if (IsKeyPressed(Config::KEY_MAP[i])) lanes.push_back(i);
    return lanes;
}

std::vector<int> InputManager::releasedLanes() const {
    std::vector<int> lanes;
    for (int i = 0; i < Config::LANES; i++)
        if (IsKeyReleased(Config::KEY_MAP[i])) lanes.push_back(i);
    return lanes;
}

bool InputManager::isKeyDown(int lane) const {
    return lane >= 0 && lane < Config::LANES && IsKeyDown(Config::KEY_MAP[lane]);
}

bool InputManager::enterPressed() const { return IsKeyPressed(KEY_ENTER); }
bool InputManager::escapePressed() const { return IsKeyPressed(KEY_ESCAPE); }
bool InputManager::quitRequested() const { return WindowShouldClose(); }
