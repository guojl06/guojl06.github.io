#include "Game.h"
#include "FilePicker.h"
#include <cmath>
#include <cstring>
#include <algorithm>

void Game::run() {
    InitWindow(Config::SW, Config::SH, "aeacrA");
    InitAudioDevice();
    SetTargetFPS(60);

    audio_.init();
    renderer_.init();
    songMgr_.scanSongs();

    while (!WindowShouldClose()) {
        float dt = GetFrameTime();
        bgPhase_ += dt * 0.5f;
        audio_.updateMusic();

        switch (state_) {
        case GameState::MENU:     tickMenu(); break;
        case GameState::SELECT:   tickSelect(); break;
        case GameState::IMPORTING: tickImporting(); break;
        case GameState::PLAYING:  tickPlaying(dt); break;
        case GameState::RESULT:   tickResult(); break;
        }
    }

    renderer_.shutdown();
    audio_.cleanup();
    CloseWindow();
}

void Game::startGame() {
    state_ = GameState::PLAYING;
    gameTime_ = 0;
    memset(laneFlash_, 0, sizeof(laneFlash_));
    comboScale_ = 1; screenFlash_ = 0; beatPulse_ = 0;
    lastJudgeTime_ = -1; lastJudge_ = JudgeResult::NONE;
    judge_.reset();
    particles_.clear();

    audio_.stopMusic();

    if (!chart_.loadFromFile(chartPath_))
        chart_.generate();

    std::string ap;
    for (auto& s : songMgr_.songs()) {
        if (s.filePath == chartPath_) { ap = s.audioPath; break; }
    }
    if (ap.empty()) ap = songMgr_.audioPathFor({"", chartPath_, 0, ""});
    if (!ap.empty()) audio_.loadMusic(ap);
    musicStarted_ = false;

    audio_.resetBeat();
}

void Game::tickMenu() {
    renderer_.beginFrame();
    renderer_.drawMenu(bgPhase_);
    renderer_.endFrame();
    if (input_.enterPressed()) {
        state_ = GameState::SELECT;
        selectedSong_ = 0;
        selectScroll_ = 0;
        selectJustEntered_ = true;
    }
}

void Game::tickSelect() {
    if (selectJustEntered_) {
        selectJustEntered_ = false;
        renderer_.beginFrame();
        renderer_.drawSelect(bgPhase_, songMgr_.songs(), selectedSong_, selectScroll_, true);
        renderer_.endFrame();
        return;
    }

    if (input_.escapePressed()) { state_ = GameState::MENU; return; }

    if (IsKeyPressed(KEY_I)) {
        state_ = GameState::IMPORTING;
        importStatus_ = "";
        importProgress_ = 0;
        return;
    }

    if (IsKeyPressed(KEY_UP) || IsKeyPressed(KEY_W)) {
        selectedSong_ = (selectedSong_ - 1 + (int)songMgr_.songs().size()) % (int)songMgr_.songs().size();
    }
    if (IsKeyPressed(KEY_DOWN) || IsKeyPressed(KEY_S)) {
        selectedSong_ = (selectedSong_ + 1) % (int)songMgr_.songs().size();
    }
    selectScroll_ += (selectedSong_ * 70.0f - selectScroll_) * 0.2f;

    if (input_.enterPressed()) {
        chartPath_ = songMgr_.songs()[selectedSong_].filePath;
        autoplay_ = false;
        startGame();
        return;
    }

    // Press A for auto-demo of selected song
    if (IsKeyPressed(KEY_A)) {
        chartPath_ = songMgr_.songs()[selectedSong_].filePath;
        autoplay_ = true;
        startGame();
        return;
    }

    renderer_.beginFrame();
    renderer_.drawSelect(bgPhase_, songMgr_.songs(), selectedSong_, selectScroll_, true);
    renderer_.endFrame();
}

void Game::tickImporting() {
    renderer_.beginFrame();
    renderer_.drawImport(bgPhase_, importStatus_.c_str(), importProgress_);
    renderer_.endFrame();

    if (importStatus_.empty()) {
        importStatus_ = "Opening file dialog...";
        importProgress_ = 0.1f;
        renderer_.beginFrame();
        renderer_.drawImport(bgPhase_, importStatus_.c_str(), importProgress_);
        renderer_.endFrame();

        std::string path = openAudioFileDialog();
        if (path.empty()) {
            importStatus_ = "Cancelled. Press any key...";
            importProgress_ = -1;
            return;
        }

        importStatus_ = "Analyzing audio...";
        importProgress_ = 0.3f;
        renderer_.beginFrame();
        renderer_.drawImport(bgPhase_, importStatus_.c_str(), importProgress_);
        renderer_.endFrame();

        std::string outChart;
        if (songMgr_.importAudio(path, outChart)) {
            importStatus_ = "Import complete! Press ENTER.";
            importProgress_ = 1.0f;
            songMgr_.scanSongs();
            auto& songs = songMgr_.songs();
            for (size_t i = 0; i < songs.size(); i++) {
                if (songs[i].filePath == outChart) {
                    selectedSong_ = (int)i;
                    break;
                }
            }
        } else {
            importStatus_ = "Import failed! Press any key.";
            importProgress_ = -1;
        }
        return;
    }

    if (importProgress_ >= 1.0f) {
        if (input_.enterPressed()) {
            selectJustEntered_ = true;
            state_ = GameState::SELECT;
        }
    } else if (importProgress_ < 0) {
        if (input_.enterPressed() || input_.escapePressed()) {
            selectJustEntered_ = true;
            state_ = GameState::SELECT;
        }
    }
}

void Game::tickResult() {
    renderer_.beginFrame();
    renderer_.drawResults(bgPhase_, judge_.score(), judge_.maxCombo(),
                          std::array<int,4>{judge_.count(JudgeResult::PERFECT),
                                            judge_.count(JudgeResult::GREAT),
                                            judge_.count(JudgeResult::GOOD),
                                            judge_.count(JudgeResult::MISS)}.data(),
                          chart_.size());
    renderer_.endFrame();
    if (input_.enterPressed()) state_ = GameState::MENU;
}

void Game::tickPlaying(float dt) {
    audio_.updateMusic();
    gameTime_ += dt;

    if (!musicStarted_ && gameTime_ >= 4.0f && audio_.hasMusic()) {
        audio_.playMusic();
        musicStarted_ = true;
    }

    float pulse = audio_.updateBeat(gameTime_);
    if (pulse > 0) beatPulse_ = pulse;

    for (int i = 0; i < Config::LANES; i++)
        laneFlash_[i] *= powf(0.005f, dt);
    comboScale_ = fmaxf(1, comboScale_ + (1 - comboScale_) * (1 - powf(0.02f, dt)));
    screenFlash_ *= powf(0.01f, dt);
    beatPulse_ *= powf(0.02f, dt);

    particles_.update(dt);

    // ── Miss expired notes ──
    for (size_t i = 0; i < chart_.size(); i++) {
        Note& n = chart_.note(i);
        if (n.result != JudgeResult::NONE) continue;
        if (n.type == NoteType::TAP && gameTime_ > n.time + Config::JW_GOOD) {
            n.result = JudgeResult::MISS;
            judge_.apply(JudgeResult::MISS);
            lastJudge_ = JudgeResult::MISS;
            lastJudgeTime_ = gameTime_;
        } else if (n.type == NoteType::HOLD && gameTime_ > n.time + Config::JW_GOOD) {
            n.result = JudgeResult::MISS;
            n.holdResult = JudgeResult::MISS;
            judge_.applyHold(JudgeResult::MISS, JudgeResult::MISS);
            lastJudge_ = JudgeResult::MISS;
            lastJudgeTime_ = gameTime_;
        }
    }

    // ── Auto-complete held notes past end time ──
    for (size_t i = 0; i < chart_.size(); i++) {
        Note& n = chart_.note(i);
        if (n.type != NoteType::HOLD || !n.holding || n.holdResult != JudgeResult::NONE) continue;
        if (gameTime_ >= n.endTime) {
            float tailDiff = fabsf(gameTime_ - n.endTime);
            JudgeResult tailJ = judge_.judge(tailDiff);
            if (tailJ == JudgeResult::NONE) tailJ = JudgeResult::GOOD;
            n.holdResult = tailJ;
            n.holding = false;
            judge_.applyHold(n.result, tailJ);
            comboScale_ = 1.5f;
            if (tailJ == JudgeResult::PERFECT) screenFlash_ = 0.5f;
            float hx = Config::FIELD_X + (n.lane + 0.5f) * Config::LANE_W;
            particles_.spawnExplosion(hx, Config::HIT_Y, n.lane);
        }
    }

    // ── Input handling: autoplay or manual ──
    if (autoplay_) {
        for (size_t i = 0; i < chart_.size(); i++) {
            Note& n = chart_.note(i);
            if (n.result != JudgeResult::NONE) continue;
            float diff = n.time - gameTime_;

            // Tap note: auto-hit at perfect timing
            if (n.type == NoteType::TAP && diff <= 0.005f && diff > -Config::JW_PERFECT) {
                n.result = JudgeResult::PERFECT;
                judge_.apply(JudgeResult::PERFECT);
                comboScale_ = 1.8f; lastJudge_ = JudgeResult::PERFECT;
                lastJudgeTime_ = gameTime_; screenFlash_ = 1;
                laneFlash_[n.lane] = 1; keysDown_[n.lane] = true;
                audio_.playLane(n.lane);
                float hx = Config::FIELD_X + (n.lane + 0.5f) * Config::LANE_W;
                particles_.spawnExplosion(hx, Config::HIT_Y, n.lane);
                particles_.spawnSpiral(hx, Config::HIT_Y, gameTime_, n.lane);
                if (judge_.combo() > 10) particles_.spawnFire(hx, Config::HIT_Y);
            }

            // Hold head: auto-hit
            if (n.type == NoteType::HOLD && !n.holding && n.holdResult == JudgeResult::NONE
                && diff <= 0.005f && diff > -Config::JW_PERFECT) {
                n.result = JudgeResult::PERFECT; n.holding = true;
                judge_.apply(JudgeResult::PERFECT);
                comboScale_ = 1.8f; lastJudge_ = JudgeResult::PERFECT;
                lastJudgeTime_ = gameTime_; screenFlash_ = 1;
                laneFlash_[n.lane] = 1; keysDown_[n.lane] = true;
                audio_.playLane(n.lane);
                float hx = Config::FIELD_X + (n.lane + 0.5f) * Config::LANE_W;
                particles_.spawnExplosion(hx, Config::HIT_Y, n.lane);
                particles_.spawnSpiral(hx, Config::HIT_Y, gameTime_, n.lane);
                if (judge_.combo() > 10) particles_.spawnFire(hx, Config::HIT_Y);
            }

            // Hold tail: auto-release at perfect timing
            if (n.type == NoteType::HOLD && n.holding && n.holdResult == JudgeResult::NONE
                && gameTime_ >= n.endTime - 0.005f) {
                n.holdResult = JudgeResult::PERFECT; n.holding = false;
                keysDown_[n.lane] = false;
                judge_.applyHold(n.result, JudgeResult::PERFECT);
                comboScale_ = 1.5f; screenFlash_ = 0.5f;
                float hx = Config::FIELD_X + (n.lane + 0.5f) * Config::LANE_W;
                particles_.spawnExplosion(hx, Config::HIT_Y, n.lane);
            }
        }

        // Release auto-held keys no longer needed
        for (int i = 0; i < Config::LANES; i++) {
            bool needed = false;
            for (size_t j = 0; j < chart_.size(); j++)
                if (chart_.note(j).lane == i && chart_.note(j).holding) { needed = true; break; }
            if (!needed) keysDown_[i] = false;
        }
    } else {
        // Manual play
        for (int lane : input_.pressedLanes()) {
            laneFlash_[lane] = 1;
            Note* best = nullptr;
            float bd = 999;
            for (size_t i = 0; i < chart_.size(); i++) {
                Note& n = chart_.note(i);
                if (n.lane != lane || n.result != JudgeResult::NONE) continue;
                float d = fabsf(gameTime_ - n.time);
                if (d < bd && d < Config::JW_GOOD) { best = &n; bd = d; }
            }
            if (best) {
                JudgeResult j = judge_.judge(bd);
                best->result = j;
                if (best->type == NoteType::HOLD) best->holding = true;
                judge_.apply(j);
                comboScale_ = 1.8f;
                lastJudge_ = j; lastJudgeTime_ = gameTime_;
                if (j == JudgeResult::PERFECT) screenFlash_ = 1;
                audio_.playLane(lane);
                float hx = Config::FIELD_X + (lane + 0.5f) * Config::LANE_W;
                particles_.spawnExplosion(hx, Config::HIT_Y, lane);
                particles_.spawnSpiral(hx, Config::HIT_Y, gameTime_, lane);
                if (judge_.combo() > 10) particles_.spawnFire(hx, Config::HIT_Y);
            } else {
                judge_.apply(JudgeResult::MISS);
                lastJudge_ = JudgeResult::MISS;
                lastJudgeTime_ = gameTime_;
                comboScale_ = 1.2f;
            }
        }

        for (int lane : input_.releasedLanes()) {
            Note* activeHold = nullptr;
            for (size_t i = 0; i < chart_.size(); i++) {
                Note& n = chart_.note(i);
                if (n.type == NoteType::HOLD && n.lane == lane && n.holding && n.holdResult == JudgeResult::NONE) {
                    activeHold = &n; break;
                }
            }
            if (activeHold) {
                float tailDiff = fabsf(gameTime_ - activeHold->endTime);
                JudgeResult tailJ = tailDiff < Config::JW_GOOD ? judge_.judge(tailDiff) : JudgeResult::MISS;
                activeHold->holdResult = tailJ;
                activeHold->holding = false;
                judge_.applyHold(activeHold->result, tailJ);
                comboScale_ = 1.5f;
                if (tailJ == JudgeResult::PERFECT) screenFlash_ = 0.5f;
                lastJudge_ = tailJ; lastJudgeTime_ = gameTime_;
                float hx = Config::FIELD_X + (lane + 0.5f) * Config::LANE_W;
                particles_.spawnExplosion(hx, Config::HIT_Y, lane);
            }
        }

        for (int i = 0; i < Config::LANES; i++)
            keysDown_[i] = input_.isKeyDown(i);
    }

    if (input_.escapePressed()) { audio_.stopMusic(); autoplay_ = false; state_ = GameState::MENU; return; }
    if (chart_.allDone()) { audio_.stopMusic(); autoplay_ = false; state_ = GameState::RESULT; return; }

    float progress = chart_.size() > 0 ? (float)chart_.doneCount() / (float)chart_.size() : 1;

    renderer_.beginFrame();
    renderer_.drawBackground(bgPhase_, dt);
    renderer_.drawTrackBase(beatPulse_);
    renderer_.drawLanes(laneFlash_, beatPulse_);
    renderer_.drawBeatLines(gameTime_);
    renderer_.drawNotes(chart_.notes(), gameTime_);
    renderer_.drawHitLine(beatPulse_, laneFlash_);
    renderer_.drawReceptors(laneFlash_, keysDown_);
    renderer_.drawParticles(particles_.particles());
    renderer_.drawScreenFlash(screenFlash_);
    renderer_.drawJudgment(lastJudge_, gameTime_ - lastJudgeTime_);
    renderer_.drawUI(judge_.score(), judge_.combo(), comboScale_, progress);
    if (gameTime_ < 4.0f) {
        int count = (int)(4.0f - gameTime_);
        if (count > 4) count = 4;
        renderer_.drawCountdown(count);
    }
    if (autoplay_)
        renderer_.drawDemoOverlay(chart_.title(), bgPhase_);
    renderer_.endFrame();
}
