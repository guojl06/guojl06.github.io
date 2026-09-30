#pragma once
#include <string>

struct SongEntry {
    std::string filePath;     // chart.json path
    std::string title;
    float bpm;
    std::string audioPath;    // full path to audio file (empty if none)
};
