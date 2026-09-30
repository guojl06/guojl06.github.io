#pragma once
#include <string>
#include <vector>

struct GenNote {
    float time;
    int lane;
    bool isHold;
    float holdEnd;
};

struct AudioFeatures {
    float bpm;
    std::vector<GenNote> notes;
};

class ChartGenerator {
public:
    static bool analyze(const std::string& audioPath, AudioFeatures& out);

private:
    static std::string baseName(const std::string& path);
};
