#pragma once
#include "SongEntry.h"
#include "Chart.h"
#include <vector>
#include <string>

class SongManager {
public:
    void scanSongs();
    const std::vector<SongEntry>& songs() const { return songs_; }

    bool importAudio(const std::string& audioPath, std::string& outChartPath);
    std::string audioPathFor(const SongEntry& song) const;

private:
    std::vector<SongEntry> songs_;
    static std::string songsDir();
    static std::string chartsDir();
};
