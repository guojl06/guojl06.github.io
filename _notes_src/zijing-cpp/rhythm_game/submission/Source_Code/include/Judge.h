#pragma once
#include "Config.h"

class JudgeSystem {
public:
    void reset();
    JudgeResult judge(float timeDiff) const;
    void apply(JudgeResult j);
    void applyHold(JudgeResult head, JudgeResult tail);

    int score() const { return score_; }
    int combo() const { return combo_; }
    int maxCombo() const { return maxCombo_; }
    int count(JudgeResult j) const;

private:
    int score_ = 0, combo_ = 0, maxCombo_ = 0;
    int counts_[4] = {};
};
