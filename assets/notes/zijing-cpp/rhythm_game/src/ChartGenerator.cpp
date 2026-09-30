#include "ChartGenerator.h"
#include <aubio/aubio.h>
#include <cmath>
#include <algorithm>
#include <numeric>
#include <cstdlib>

struct OnsetInfo {
    float time;
    float energy;
    float centroid;    // spectral centroid (low=0, high=1)
    float bassRatio;   // low frequency energy ratio
};

static bool detectBPM(const std::string& path, float& bpm) {
    aubio_source_t* src = new_aubio_source(path.c_str(), 0, 1024);
    if (!src) return false;
    uint_t sr = aubio_source_get_samplerate(src);

    aubio_tempo_t* tempo = new_aubio_tempo("default", 1024, 512, sr);
    fvec_t* buf = new_fvec(1024);
    fvec_t* beatOut = new_fvec(2);

    bpm = 140;
    std::vector<float> beatTimes;

    uint_t read = 0;
    do {
        aubio_source_do(src, buf, &read);
        aubio_tempo_do(tempo, buf, beatOut);
        if (beatOut->data[0] != 0)
            beatTimes.push_back(aubio_tempo_get_last_s(tempo));
    } while (read == 1024);

    if (beatTimes.size() >= 4) {
        std::vector<float> intervals;
        for (size_t i = 1; i < beatTimes.size(); i++)
            intervals.push_back(beatTimes[i] - beatTimes[i - 1]);
        std::sort(intervals.begin(), intervals.end());
        float median = intervals[intervals.size() / 2];
        if (median > 0.1f) bpm = 60.0f / median;
    }
    bpm = fmaxf(60, fminf(300, bpm));

    del_fvec(buf);
    del_fvec(beatOut);
    del_aubio_tempo(tempo);
    del_aubio_source(src);
    return true;
}

static void detectOnsets(const std::string& path, std::vector<OnsetInfo>& out) {
    aubio_source_t* src = new_aubio_source(path.c_str(), 0, 512);
    if (!src) return;
    uint_t sr = aubio_source_get_samplerate(src);

    aubio_onset_t* od = new_aubio_onset("default", 512, 256, sr);
    fvec_t* buf = new_fvec(512);
    fvec_t* onsetOut = new_fvec(1);

    // FFT for spectral analysis
    aubio_fft_t* fft = new_aubio_fft(512);
    fvec_t* fftOut = new_fvec(256);
    cvec_t* fftC = new_cvec(512);

    uint_t read = 0;
    float lastOnset = -1;
    do {
        aubio_source_do(src, buf, &read);
        aubio_onset_do(od, buf, onsetOut);

        if (onsetOut->data[0] != 0) {
            float t = aubio_onset_get_last_s(od);
            if (t - lastOnset > 0.08f) {
                OnsetInfo info;
                info.time = t;

                // Compute spectral features at onset
                aubio_fft_do(fft, buf, fftC);

                float totalEnergy = 0, weightedFreq = 0, bassEnergy = 0;
                int bassBins = 256 / 8; // ~first octave
                for (int i = 0; i < 256; i++) {
                    float mag = fftC->norm[i];
                    totalEnergy += mag;
                    weightedFreq += mag * i;
                    if (i < bassBins) bassEnergy += mag;
                }
                info.energy = totalEnergy;
                info.centroid = (totalEnergy > 0) ? weightedFreq / totalEnergy / 256.0f : 0.5f;
                info.bassRatio = (totalEnergy > 0) ? bassEnergy / totalEnergy : 0.5f;

                out.push_back(info);
                lastOnset = t;
            }
        }
    } while (read == 512);

    del_fvec(buf);
    del_fvec(onsetOut);
    del_aubio_onset(od);
    del_aubio_fft(fft);
    del_fvec(fftOut);
    del_cvec(fftC);
    del_aubio_source(src);
}

bool ChartGenerator::analyze(const std::string& audioPath, AudioFeatures& out) {
    if (!detectBPM(audioPath, out.bpm)) return false;

    std::vector<OnsetInfo> onsets;
    detectOnsets(audioPath, onsets);
    if (onsets.empty()) return false;

    // Normalize energy to 0-1 range
    float maxEnergy = 0;
    for (auto& o : onsets) if (o.energy > maxEnergy) maxEnergy = o.energy;
    if (maxEnergy > 0)
        for (auto& o : onsets) o.energy /= maxEnergy;

    float beatDur = 60.0f / out.bpm;
    int numLanes = 6;
    float lastGridTime = -1;
    int lastLane = -1;
    int noteIndex = 0;

    // Seed random from song characteristics
    unsigned int seed = (unsigned int)(out.bpm * 100) + (unsigned int)onsets.size();
    auto rng = [seed]() mutable { seed = seed * 1103515245 + 12345; return (seed >> 16) & 0x7fff; };

    for (size_t i = 0; i < onsets.size(); i++) {
        float t = onsets[i].time;
        if (t < 4.0f) continue;

        // Uniform grid: 1/2 beat
        float grid = roundf(t / (beatDur * 0.5f)) * beatDur * 0.5f;

        // Skip if too close to previous note
        if (fabsf(grid - lastGridTime) < beatDur * 0.4f) continue;
        lastGridTime = grid;

        // ── Lane assignment based on spectral features ──
        int lane;
        float centroid = onsets[i].centroid;
        float bass = onsets[i].bassRatio;
        float energy = onsets[i].energy;

        if (bass > 0.5f) {
            lane = (centroid < 0.15f) ? 0 : 1;
        } else if (centroid > 0.6f) {
            lane = (centroid > 0.75f) ? 5 : 4;
        } else {
            lane = (centroid > 0.35f) ? 3 : 2;
        }

        // Variation by section
        int section = (int)(t / (beatDur * 8));
        int variation = (rng() % 3) - 1;

        switch (section % 5) {
        case 0: break;
        case 1: lane += variation; break;
        case 2: lane = (noteIndex * 2 + 3) % numLanes; break;
        case 3: lane += (variation * 2); break;
        case 4: lane = numLanes - 1 - lane; break;
        }

        lane = fmaxf(0, fminf(numLanes - 1, lane));
        if (lane == lastLane) {
            int tries = 0;
            do { lane = (lane + 1 + rng() % (numLanes - 1)) % numLanes; tries++; }
            while (lane == lastLane && tries < 5);
        }
        lastLane = lane;

        // ── Hold notes for sustained sounds ──
        bool makeHold = false;
        float holdEnd = 0;
        if (energy < 0.4f && bass > 0.3f && noteIndex % 10 == 0) {
            makeHold = true;
            holdEnd = grid + beatDur * (1 + (rng() % 3));
        }

        out.notes.push_back({grid, lane, makeHold, holdEnd});
        noteIndex++;
    }

    // Post-process: remove taps that overlap with holds on the same lane
    // Sort by time
    std::sort(out.notes.begin(), out.notes.end(),
              [](const GenNote& a, const GenNote& b) {
                  return a.time < b.time || (a.time == b.time && a.lane < b.lane);
              });

    // Build hold occupancy ranges per lane
    struct HoldRange { float start; float end; int lane; };
    std::vector<HoldRange> holds;
    for (auto& n : out.notes) {
        if (n.isHold)
            holds.push_back({n.time, n.holdEnd, n.lane});
    }

    // Remove taps that fall inside any hold range on the same lane
    out.notes.erase(
        std::remove_if(out.notes.begin(), out.notes.end(),
            [&](const GenNote& n) {
                if (n.isHold) return false;
                for (auto& h : holds) {
                    if (n.lane == h.lane && n.time >= h.start - 0.01f && n.time <= h.end + 0.01f)
                        return true;
                }
                return false;
            }),
        out.notes.end());

    // Deduplicate same time+lane
    out.notes.erase(std::unique(out.notes.begin(), out.notes.end(),
                                [](const GenNote& a, const GenNote& b) {
                                    return fabsf(a.time - b.time) < 0.01f && a.lane == b.lane;
                                }),
                    out.notes.end());

    return !out.notes.empty();
}

std::string ChartGenerator::baseName(const std::string& path) {
    size_t slash = path.find_last_of("/\\");
    std::string name = (slash == std::string::npos) ? path : path.substr(slash + 1);
    size_t dot = name.find_last_of('.');
    return (dot == std::string::npos) ? name : name.substr(0, dot);
}
