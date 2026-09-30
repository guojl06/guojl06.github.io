#include "SongManager.h"
#include "ChartGenerator.h"
#include "JsonParser.h"
#include <dirent.h>
#include <sys/stat.h>
#include <fstream>
#include <sstream>
#include <algorithm>

std::string SongManager::songsDir() { return "songs"; }
std::string SongManager::chartsDir() { return "charts"; }

static std::string findAudioInDir(const std::string& dir) {
    const char* exts[] = {".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac"};
    DIR* d = opendir(dir.c_str());
    if (!d) return "";
    struct dirent* ent;
    while ((ent = readdir(d)) != nullptr) {
        std::string name = ent->d_name;
        for (auto ext : exts) {
            if (name.size() > strlen(ext) &&
                name.substr(name.size() - strlen(ext)) == ext) {
                closedir(d);
                return dir + "/" + name;
            }
        }
    }
    closedir(d);
    return "";
}

static std::string dirOf(const std::string& filePath) {
    size_t slash = filePath.find_last_of("/\\");
    return (slash != std::string::npos) ? filePath.substr(0, slash) : ".";
}

void SongManager::scanSongs() {
    songs_.clear();
    songs_.push_back({"", "Random (Generated)", 140, ""});

    // Scan charts/ folder
    DIR* dir = opendir(chartsDir().c_str());
    if (dir) {
        struct dirent* ent;
        while ((ent = readdir(dir)) != nullptr) {
            std::string name = ent->d_name;
            if (name.size() > 5 && name.substr(name.size() - 5) == ".json") {
                SongEntry se;
                se.filePath = chartsDir() + "/" + name;
                Chart c;
                se.title = (c.loadFromFile(se.filePath)) ? c.title()
                         : name.substr(0, name.size() - 5);
                se.bpm = 140;
                std::ifstream f(se.filePath);
                if (f.is_open()) {
                    std::stringstream ss;
                    ss << f.rdbuf();
                    JsonValue root = parseJson(ss.str());
                    if (root["bpm"].type == JsonType::Number)
                        se.bpm = (float)root["bpm"].asNum();
                }
                songs_.push_back(se);
            }
        }
        closedir(dir);
    }

    // Scan songs/ folder (imported)
    dir = opendir(songsDir().c_str());
    if (dir) {
        struct dirent* ent;
        while ((ent = readdir(dir)) != nullptr) {
            std::string name = ent->d_name;
            if (name == "." || name == "..") continue;

            struct stat st;
            std::string fullPath = songsDir() + "/" + name;
            if (stat(fullPath.c_str(), &st) != 0 || !S_ISDIR(st.st_mode)) continue;

            std::string chartPath = fullPath + "/chart.json";
            SongEntry se;
            se.filePath = chartPath;
            se.audioPath = findAudioInDir(fullPath);

            Chart c;
            se.title = (c.loadFromFile(chartPath)) ? c.title() : name;

            se.bpm = 140;
            std::ifstream f(chartPath);
            if (f.is_open()) {
                std::stringstream ss;
                ss << f.rdbuf();
                JsonValue root = parseJson(ss.str());
                if (root["bpm"].type == JsonType::Number)
                    se.bpm = (float)root["bpm"].asNum();
            }
            songs_.push_back(se);
        }
        closedir(dir);
    }

    std::sort(songs_.begin() + 1, songs_.end(),
              [](const SongEntry& a, const SongEntry& b) { return a.title < b.title; });
}

bool SongManager::importAudio(const std::string& audioPath, std::string& outChartPath) {
    // Extract base name
    size_t slash = audioPath.find_last_of("/\\");
    std::string fileName = (slash == std::string::npos) ? audioPath : audioPath.substr(slash + 1);
    size_t dot = fileName.find_last_of('.');
    std::string baseName = (dot != std::string::npos) ? fileName.substr(0, dot) : fileName;
    std::string ext = (dot != std::string::npos) ? fileName.substr(dot) : "";

    // Create songs/<name>/ directory
    std::string dir = songsDir() + "/" + baseName;
    mkdir(songsDir().c_str(), 0755);
    mkdir(dir.c_str(), 0755);

    // Copy audio file
    std::string destAudio = dir + "/audio" + ext;
    {
        std::ifstream src(audioPath, std::ios::binary);
        std::ofstream dst(destAudio, std::ios::binary);
        if (!src.is_open() || !dst.is_open()) return false;
        dst << src.rdbuf();
    }

    // Analyze audio
    AudioFeatures features;
    if (!ChartGenerator::analyze(audioPath, features)) return false;

    // Write chart JSON
    outChartPath = dir + "/chart.json";
    std::ofstream cf(outChartPath);
    if (!cf.is_open()) return false;

    cf << "{\n";
    cf << "  \"title\": \"" << baseName << "\",\n";
    cf << "  \"bpm\": " << (int)features.bpm << ",\n";
    cf << "  \"audio\": \"audio" << ext << "\",\n";
    cf << "  \"notes\": [\n";
    for (size_t i = 0; i < features.notes.size(); i++) {
        auto& n = features.notes[i];
        cf << "    {\"time\": " << n.time << ", \"lane\": " << n.lane;
        if (n.isHold)
            cf << ", \"type\": \"hold\", \"end\": " << n.holdEnd;
        cf << "}";
        if (i + 1 < features.notes.size()) cf << ",";
        cf << "\n";
    }
    cf << "  ]\n}\n";

    return true;
}

std::string SongManager::audioPathFor(const SongEntry& song) const {
    // Direct path from SongEntry
    if (!song.audioPath.empty()) return song.audioPath;
    // Fallback: scan directory for audio files
    return findAudioInDir(dirOf(song.filePath));
}
