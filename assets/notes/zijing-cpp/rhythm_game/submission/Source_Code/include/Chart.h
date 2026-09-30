#pragma once
#include "Config.h"
#include <vector>
#include <string>

struct Note {
    float time;
    int lane;
    NoteType type = NoteType::TAP;
    float endTime = 0;           // hold 结束时间
    JudgeResult result = JudgeResult::NONE;      // 头部判定
    JudgeResult holdResult = JudgeResult::NONE;   // hold 尾部判定
    bool holding = false;        // 是否正在按住

    float duration() const { return type == NoteType::HOLD ? endTime - time : 0; }
    bool resolved() const {
        if (type == NoteType::TAP) return result != JudgeResult::NONE;
        return result != JudgeResult::NONE && holdResult != JudgeResult::NONE;
    }
    bool finished() const {
        if (type == NoteType::TAP) return result != JudgeResult::NONE;
        return result == JudgeResult::MISS || holdResult != JudgeResult::NONE;
    }
};

class Chart {
public:
    void generate();
    bool loadFromFile(const std::string& path);
    bool saveToFile(const std::string& path) const;
    void reset();

    const std::vector<Note>& notes() const { return notes_; }
    Note& note(size_t i) { return notes_[i]; }
    size_t size() const { return notes_.size(); }
    bool allDone() const;
    int doneCount() const;

    const std::string& title() const { return title_; }
    const std::string& audioFile() const { return audioFile_; }

private:
    std::vector<Note> notes_;
    std::string title_ = "Generated";
    std::string audioFile_;
};
