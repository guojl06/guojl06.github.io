#include "Chart.h"
#include "JsonParser.h"
#include <cstdlib>
#include <algorithm>
#include <fstream>
#include <sstream>

void Chart::reset() { notes_.clear(); }

void Chart::generate() {
    notes_.clear();
    title_ = "Generated";
    float t = 4.0f;
    auto add = [&](float time, int lane) {
        notes_.push_back({time, lane, NoteType::TAP, 0});
    };
    auto hold = [&](float time, int lane, float dur) {
        notes_.push_back({time, lane, NoteType::HOLD, time + dur});
    };

    for (int b = 0; b < 18; b++) { add(t + b * Config::BEAT, b % 6); }
    t += 18 * Config::BEAT;
    for (int rep = 0; rep < 3; rep++) {
        for (int i = 0; i < 6; i++) add(t + i * Config::BEAT * 0.25f, i);
        t += Config::BEAT * 1.5f;
        for (int i = 5; i >= 0; i--) add(t + (5 - i) * Config::BEAT * 0.25f, i);
        t += Config::BEAT * 1.5f;
    }
    for (int b = 0; b < 16; b++) {
        add(t, b % 3); add(t, 3 + b % 3);
        t += Config::BEAT * 0.5f;
    }
    for (int b = 0; b < 8; b++) {
        add(t, 0); add(t, 2); add(t, 5); t += Config::BEAT;
        add(t, 1); add(t, 3); add(t, 4); t += Config::BEAT;
    }
    for (int b = 0; b < 48; b++) { add(t, b % 6); t += Config::BEAT * 0.25f; }
    for (int b = 0; b < 24; b++) { add(t, rand() % 6); t += Config::BEAT * 0.5f; }
    for (int b = 0; b < 30; b++) {
        if (b % 4 == 0) { add(t, 0); add(t, 5); }
        else if (b % 4 == 2) { add(t, 2); add(t, 3); }
        else add(t, b % 6);
        t += Config::BEAT * 0.5f;
    }
    for (int b = 0; b < 16; b++) {
        add(t, b % 3); add(t + Config::BEAT * 0.25f, 3 + b % 3);
        t += Config::BEAT * 0.5f;
    }
    for (int b = 0; b < 6; b++) { add(t, b); t += Config::BEAT * 0.5f; }
    add(t, 0); add(t, 1); add(t, 2); add(t, 3); add(t, 4); add(t, 5);
}

bool Chart::loadFromFile(const std::string& path) {
    std::ifstream file(path);
    if (!file.is_open()) return false;

    std::stringstream ss;
    ss << file.rdbuf();
    std::string text = ss.str();

    JsonValue root = parseJson(text);
    if (root.type != JsonType::Object) return false;

    title_ = root["title"].asStr();
    if (title_.empty()) title_ = path;
    audioFile_ = root["audio"].asStr();

    float bpm = (float)root["bpm"].asNum(Config::BPM);
    float beatDur = 60.0f / bpm;

    const JsonValue& arr = root["notes"];
    if (arr.type != JsonType::Array) return false;

    notes_.clear();
    for (size_t i = 0; i < arr.size(); i++) {
        const JsonValue& n = arr[i];
        float time;
        int lane;
        NoteType type = NoteType::TAP;
        float endTime = 0;

        if (n.type == JsonType::Object) {
            // time 或 beat
            if (n["beat"].type == JsonType::Number)
                time = (float)n["beat"].asNum() * beatDur;
            else
                time = (float)n["time"].asNum();
            lane = (int)n["lane"].asNum(-1);

            // hold: 检查 type/end/duration/endBeat
            const JsonValue& jt = n["type"];
            if (jt.type == JsonType::String && jt.str == "hold") {
                type = NoteType::HOLD;
                if (n["end"].type == JsonType::Number)
                    endTime = (float)n["end"].asNum();
                else if (n["endBeat"].type == JsonType::Number)
                    endTime = (float)n["endBeat"].asNum() * beatDur;
                else if (n["duration"].type == JsonType::Number)
                    endTime = time + (float)n["duration"].asNum();
                else if (n["dur"].type == JsonType::Number)
                    endTime = time + (float)n["dur"].asNum() * beatDur;
                if (endTime <= time) endTime = time + beatDur;
            }
        } else if (n.type == JsonType::Array && n.size() >= 2) {
            time = (float)n[(size_t)0].asNum();
            lane = (int)n[(size_t)1].asNum(-1);
            if (n.size() >= 3 && n[(size_t)2].asNum() > 0) {
                type = NoteType::HOLD;
                endTime = time + (float)n[(size_t)2].asNum();
            }
        } else {
            continue;
        }

        if (lane >= 0 && lane < Config::LANES)
            notes_.push_back({time, lane, type, endTime});
    }

    if (notes_.empty()) return false;
    std::sort(notes_.begin(), notes_.end(),
              [](const Note& a, const Note& b) { return a.time < b.time; });
    return true;
}

bool Chart::saveToFile(const std::string& path) const {
    std::ofstream file(path);
    if (!file.is_open()) return false;

    file << "{\n  \"title\": \"" << title_ << "\",\n";
    file << "  \"bpm\": " << Config::BPM << ",\n";
    file << "  \"notes\": [\n";
    for (size_t i = 0; i < notes_.size(); i++) {
        const Note& n = notes_[i];
        file << "    {\"time\": " << n.time << ", \"lane\": " << n.lane;
        if (n.type == NoteType::HOLD)
            file << ", \"type\": \"hold\", \"end\": " << n.endTime;
        file << "}";
        if (i + 1 < notes_.size()) file << ",";
        file << "\n";
    }
    file << "  ]\n}\n";
    return true;
}

bool Chart::allDone() const {
    for (auto& n : notes_)
        if (!n.resolved()) return false;
    return !notes_.empty();
}

int Chart::doneCount() const {
    int c = 0;
    for (auto& n : notes_) if (n.resolved()) c++;
    return c;
}
