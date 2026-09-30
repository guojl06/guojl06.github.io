#pragma once
#include "Config.h"
#include <vector>

class InputManager {
public:
    std::vector<int> pressedLanes() const;
    std::vector<int> releasedLanes() const;
    bool isKeyDown(int lane) const;
    bool enterPressed() const;
    bool escapePressed() const;
    bool quitRequested() const;
};
