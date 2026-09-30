#pragma once
#include "Config.h"
#include "Chart.h"
#include "Judge.h"
#include "ParticleSystem.h"
#include "SongEntry.h"
#include <vector>

class Renderer {
public:
    void init();
    void shutdown();

    // 菜单/结算
    void drawMenu(float bgPhase);
    void drawSelect(float bgPhase, const std::vector<SongEntry>& songs,
                    int selected, float scrollY, bool hasImport);
    void drawImport(float bgPhase, const char* status, float progress);
    void drawResults(float bgPhase, int score, int maxCombo,
                     const int counts[4], size_t totalNotes);

    // 游戏帧
    void beginFrame();
    void drawBackground(float bgPhase, float dt);
    void drawTrackBase(float beatPulse);
    void drawLanes(const float laneFlash[], float beatPulse);
    void drawBeatLines(float gameTime);
    void drawNotes(const std::vector<Note>& notes, float gameTime);
    void drawHitLine(float beatPulse, const float laneFlash[]);
    void drawReceptors(const float laneFlash[], const bool keysDown[]);
    void drawParticles(const std::vector<Particle>& particles);
    void drawScreenFlash(float flash);
    void drawJudgment(JudgeResult judge, float elapsed);
    void drawUI(int score, int combo, float comboScale, float progress);
    void drawCountdown(int count);
    void drawDemoOverlay(const std::string& title, float bgPhase);
    void endFrame();

private:
    struct Petal {
        float x, y, speed, size, phase, amp;
        Color tint;
    };
    std::vector<Petal> petals_;

    static float perspY(float d);
    static float perspX(float hx, float d);
    static float noteDepth(const Note& n, float t);
    static void drawSparkle(Vector2 pos, float size, Color c);
    void drawPerspectiveLane(int lane, float flash);
};
