#include "Judge.h"

void JudgeSystem::reset() {
    score_ = 0; combo_ = 0; maxCombo_ = 0;
    counts_[0] = counts_[1] = counts_[2] = counts_[3] = 0;
}

JudgeResult JudgeSystem::judge(float diff) const {
    if (diff <= Config::JW_PERFECT) return JudgeResult::PERFECT;
    if (diff <= Config::JW_GREAT)   return JudgeResult::GREAT;
    if (diff <= Config::JW_GOOD)    return JudgeResult::GOOD;
    return JudgeResult::NONE;
}

static int idx(JudgeResult j) {
    return (j == JudgeResult::PERFECT) ? 0 :
           (j == JudgeResult::GREAT)   ? 1 :
           (j == JudgeResult::GOOD)    ? 2 : 3;
}

static int pts(JudgeResult j) {
    if (j == JudgeResult::PERFECT) return 350;
    if (j == JudgeResult::GREAT)   return 200;
    if (j == JudgeResult::GOOD)    return 100;
    return 0;
}

void JudgeSystem::apply(JudgeResult j) {
    counts_[idx(j)]++;
    score_ += pts(j);
    if (j == JudgeResult::MISS) { combo_ = 0; }
    else { combo_++; if (combo_ > maxCombo_) maxCombo_ = combo_; }
}

void JudgeSystem::applyHold(JudgeResult head, JudgeResult tail) {
    // 头部判定
    apply(head);
    // 尾部加分（hold 的额外奖励）
    if (head != JudgeResult::MISS && tail != JudgeResult::MISS) {
        counts_[idx(tail)]++;
        score_ += pts(tail);
        combo_++; if (combo_ > maxCombo_) maxCombo_ = combo_;
    }
}

int JudgeSystem::count(JudgeResult j) const { return counts_[idx(j)]; }
