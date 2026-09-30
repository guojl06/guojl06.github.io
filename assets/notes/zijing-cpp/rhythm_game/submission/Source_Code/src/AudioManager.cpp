#include "AudioManager.h"
#include <cmath>
#include <cstdlib>

Sound AudioManager::makeTone(float freq, float dur, float vol) {
    const int SR = 44100;
    int n = (int)(SR * dur);
    short* buf = (short*)MemAlloc(n * sizeof(short));
    for (int i = 0; i < n; i++) {
        float t = (float)i / SR;
        buf[i] = (short)(sinf(2 * PI * freq * t) * vol * powf(1 - t / dur, 2) * 32767);
    }
    Wave w = {(unsigned)n, (unsigned)SR, 16, 1, buf};
    Sound s = LoadSoundFromWave(w);
    UnloadWave(w);
    return s;
}

Sound AudioManager::makeKick() {
    const int SR = 44100;
    float dur = 0.15f;
    int n = (int)(SR * dur);
    short* buf = (short*)MemAlloc(n * sizeof(short));
    for (int i = 0; i < n; i++) {
        float t = (float)i / SR;
        buf[i] = (short)(sinf(2 * PI * (150 * expf(-t * 20) + 40) * t) *
                         0.3f * powf(1 - t / dur, 3) * 32767);
    }
    Wave w = {(unsigned)n, (unsigned)SR, 16, 1, buf};
    Sound s = LoadSoundFromWave(w);
    UnloadWave(w);
    return s;
}

Sound AudioManager::makeHat() {
    const int SR = 44100;
    float dur = 0.04f;
    int n = (int)(SR * dur);
    short* buf = (short*)MemAlloc(n * sizeof(short));
    for (int i = 0; i < n; i++) {
        float t = (float)i / SR;
        buf[i] = (short)(((float)rand() / RAND_MAX * 2 - 1) *
                         0.1f * powf(1 - t / dur, 6) * 32767);
    }
    Wave w = {(unsigned)n, (unsigned)SR, 16, 1, buf};
    Sound s = LoadSoundFromWave(w);
    UnloadWave(w);
    return s;
}

void AudioManager::init() {
    float freqs[Config::LANES] = {440, 494, 523, 587, 659, 784};
    for (int i = 0; i < Config::LANES; i++)
        laneSnd_[i] = makeTone(freqs[i], 0.15f, 0.2f);
    kickSnd_ = makeKick();
    hatSnd_ = makeHat();
}

void AudioManager::cleanup() {
    for (int i = 0; i < Config::LANES; i++) UnloadSound(laneSnd_[i]);
    UnloadSound(kickSnd_);
    UnloadSound(hatSnd_);
    stopMusic();
    CloseAudioDevice();
}

void AudioManager::resetBeat() {
    nextBeatTime_ = 0;
    beatIdx_ = 0;
}

void AudioManager::playLane(int lane) {
    if (lane >= 0 && lane < Config::LANES) PlaySound(laneSnd_[lane]);
}

float AudioManager::updateBeat(float gameTime) {
    float pulse = 0;
    if (!musicLoaded_) {
        while (gameTime >= nextBeatTime_) {
            if (beatIdx_ % 2 == 0) PlaySound(kickSnd_);
            PlaySound(hatSnd_);
            nextBeatTime_ += Config::BEAT * 0.5f;
            beatIdx_++;
            pulse = 1.0f;
        }
    } else {
        // Sync beat pulse to music beats
        while (gameTime >= nextBeatTime_) {
            nextBeatTime_ += Config::BEAT * 0.5f;
            beatIdx_++;
            pulse = 1.0f;
        }
    }
    return pulse;
}

bool AudioManager::loadMusic(const std::string& path) {
    if (musicLoaded_) stopMusic();
    if (path.empty()) return false;
    bgMusic_ = LoadMusicStream(path.c_str());
    musicLoaded_ = true;
    SetMusicVolume(bgMusic_, 0.7f);
    return true;
}

void AudioManager::playMusic() {
    if (musicLoaded_) PlayMusicStream(bgMusic_);
}

void AudioManager::stopMusic() {
    if (musicLoaded_) {
        StopMusicStream(bgMusic_);
        UnloadMusicStream(bgMusic_);
        musicLoaded_ = false;
    }
}

void AudioManager::updateMusic() {
    if (musicLoaded_) UpdateMusicStream(bgMusic_);
}

bool AudioManager::hasMusic() const {
    return musicLoaded_;
}
