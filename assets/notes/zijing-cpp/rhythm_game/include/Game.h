#pragma once
#include "Chart.h"
#include "Judge.h"
#include "ParticleSystem.h"
#include "AudioManager.h"
#include "InputManager.h"
#include "Renderer.h"
#include "SongManager.h"
#include <vector>
#include <string>

enum class GameState { MENU, SELECT, IMPORTING, PLAYING, RESULT };

class Game {
public:
    void run();

private:
    void startGame();
    void tickMenu();
    void tickSelect();
    void tickImporting();
    void tickPlaying(float dt);
    void tickResult();

    Chart chart_;
    JudgeSystem judge_;
    ParticleSystem particles_;
    AudioManager audio_;
    InputManager input_;
    Renderer renderer_;
    SongManager songMgr_;

    GameState state_ = GameState::MENU;
    float gameTime_ = 0, bgPhase_ = 0;
    float laneFlash_[Config::LANES] = {};
    float comboScale_ = 1, screenFlash_ = 0, beatPulse_ = 0;
    float lastJudgeTime_ = -1;
    JudgeResult lastJudge_ = JudgeResult::NONE;
    bool keysDown_[Config::LANES] = {};
    std::string chartPath_;
    std::string audioPath_;

    int selectedSong_ = 0;
    float selectScroll_ = 0;
    bool selectJustEntered_ = false;

    // Import state
    std::string importStatus_;
    float importProgress_ = 0;
    bool musicStarted_ = false;
    bool autoplay_ = false;
};
