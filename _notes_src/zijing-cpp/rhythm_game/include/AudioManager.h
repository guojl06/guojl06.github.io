#pragma once
#include "Config.h"
#include <string>

class AudioManager {
public:
    void init();
    void cleanup();
    void resetBeat();

    void playLane(int lane);
    float updateBeat(float gameTime);

    bool loadMusic(const std::string& path);
    void playMusic();
    void stopMusic();
    void updateMusic();
    bool hasMusic() const;

private:
    Sound laneSnd_[Config::LANES];
    Sound kickSnd_, hatSnd_;
    float nextBeatTime_ = 0;
    int beatIdx_ = 0;
    Music bgMusic_ = {};
    bool musicLoaded_ = false;

    static Sound makeTone(float freq, float dur, float vol);
    static Sound makeKick();
    static Sound makeHat();
};
