#include "Renderer.h"
#include <cstdlib>
#include <algorithm>

float Renderer::perspY(float d) {
    return Config::VP_Y + Config::TRACK_LEN * powf(fmaxf(d, 0), Config::PERSP);
}
float Renderer::perspX(float hx, float d) {
    return Config::VP_X + (hx - Config::VP_X) * fmaxf(d, 0);
}
float Renderer::noteDepth(const Note& n, float t) {
    return 1.0f - (n.time - t) * Config::SCROLL_SPEED / Config::TRACK_LEN;
}

void Renderer::init() {
    petals_.resize(50);
    for (auto& p : petals_) {
        p.x = (float)(rand() % Config::SW);
        p.y = (float)(rand() % Config::SH);
        p.speed = 5 + (float)(rand() % 15);
        p.size = 2 + (float)(rand() % 100) / 50;
        p.phase = (float)(rand() % 100) / 10;
        p.amp = 15 + (float)(rand() % 30);
        p.tint = Config::PASTEL[rand() % 6];
    }
}
void Renderer::shutdown() {}

void Renderer::drawSparkle(Vector2 pos, float size, Color c) {
    DrawLineV({pos.x - size, pos.y}, {pos.x + size, pos.y}, c);
    DrawLineV({pos.x, pos.y - size}, {pos.x, pos.y + size}, c);
    float d = size * 0.5f;
    DrawLineV({pos.x - d, pos.y - d}, {pos.x + d, pos.y + d}, ColorAlpha(c, 0.4f));
    DrawLineV({pos.x + d, pos.y - d}, {pos.x - d, pos.y + d}, ColorAlpha(c, 0.4f));
}

void Renderer::drawPerspectiveLane(int lane, float flash) {
    const int SEG = 20;
    float lx = Config::FIELD_X + lane * Config::LANE_W;
    float rx = lx + Config::LANE_W;
    Color dim = Config::PASTEL_DIM[lane];
    Color pc = Config::PASTEL[lane];
    for (int s = 0; s < SEG; s++) {
        float d0 = (float)s / SEG, d1 = (float)(s + 1) / SEG;
        float y0 = perspY(d0), y1 = perspY(d1);
        float al0 = perspX(lx, d0), ar0 = perspX(rx, d0);
        float al1 = perspX(lx, d1), ar1 = perspX(rx, d1);
        float t = d1;
        float fr = dim.r + pc.r * 0.22f * t + flash * pc.r * 0.4f;
        float fg = dim.g + pc.g * 0.22f * t + flash * pc.g * 0.4f;
        float fb = dim.b + pc.b * 0.22f * t + flash * pc.b * 0.4f;
        Color c = {(unsigned char)fminf(255, fr), (unsigned char)fminf(255, fg),
                   (unsigned char)fminf(255, fb), 255};
        DrawTriangle({al0, y0}, {ar0, y0}, {al1, y1}, c);
        DrawTriangle({ar0, y0}, {ar1, y1}, {al1, y1}, c);
    }
}

void Renderer::beginFrame() { BeginDrawing(); }
void Renderer::endFrame() { EndDrawing(); }

void Renderer::drawBackground(float bgPhase, float dt) {
    ClearBackground(Config::BG_CREAM);
    for (auto& p : petals_) {
        p.y -= p.speed * dt;
        p.x += sinf(bgPhase + p.phase) * p.amp * dt;
        if (p.y < -10) { p.y = Config::SH + 10; p.x = (float)(rand() % Config::SW); }
        float a = 0.12f + sinf(bgPhase * 2 + p.phase) * 0.08f;
        DrawCircleV({p.x, p.y}, p.size * 1.5f, ColorAlpha(p.tint, a * 0.3f));
        DrawCircleV({p.x, p.y}, p.size, ColorAlpha(p.tint, a));
    }
    for (int ring = 0; ring < 2; ring++) {
        float br = 90 + ring * 55;
        int n = 6 + ring * 3;
        for (int i = 0; i < n; i++) {
            float ang = bgPhase * (0.12f + ring * 0.06f) + (float)i / n * PI * 2;
            float r = br + sinf(bgPhase + i + ring) * 10;
            float cx = Config::SW / 2 + cosf(ang) * r;
            float cy = Config::SH * 0.3f + sinf(ang) * r * 0.35f;
            DrawCircleLines((int)cx, (int)cy, 12 + ring * 8,
                            ColorAlpha(Config::PASTEL[(i + ring) % 6], 0.07f));
        }
    }
}

void Renderer::drawTrackBase(float beatPulse) {
    for (int i = 5; i >= 0; i--) {
        float r = 15 + i * 20;
        float a = 0.05f * (6 - i) * (0.5f + beatPulse * 0.3f);
        DrawCircleV({Config::VP_X, Config::VP_Y}, r, ColorAlpha(Config::ROSE_GOLD, a));
    }
    float margin = 8.0f;
    float bl = Config::FIELD_X - margin, br = Config::FIELD_X + Config::LANES * Config::LANE_W + margin;
    for (int s = 0; s < 16; s++) {
        float d0 = (float)s / 16, d1 = (float)(s + 1) / 16;
        float y0 = perspY(d0), y1 = perspY(d1);
        float l0 = perspX(bl, d0), r0 = perspX(br, d0);
        float l1 = perspX(bl, d1), r1 = perspX(br, d1);
        unsigned char a = (unsigned char)(40 + d1 * 50);
        DrawTriangle({l0, y0}, {r0, y0}, {l1, y1}, {20, 15, 25, a});
        DrawTriangle({r0, y0}, {r1, y1}, {l1, y1}, {20, 15, 25, a});
    }
}

void Renderer::drawLanes(const float laneFlash[], float beatPulse) {
    for (int i = 0; i < Config::LANES; i++)
        drawPerspectiveLane(i, laneFlash[i]);
    for (int i = 0; i <= Config::LANES; i++) {
        float ex = Config::FIELD_X + i * Config::LANE_W;
        DrawLineEx({Config::VP_X, Config::VP_Y}, {ex, Config::HIT_Y},
                   1.5f, ColorAlpha(Config::ROSE_GOLD, 0.45f));
    }
    float slx = Config::FIELD_X - 10, srx = Config::FIELD_X + Config::LANES * Config::LANE_W + 10;
    for (int i = 0; i < 5; i++) {
        float d = 0.2f + (float)i * 0.16f;
        if (d > 1) break;
        float y = perspY(d);
        DrawCircleV({perspX(slx, d), y}, 2.5f, ColorAlpha(Config::ROSE_GOLD, d * 0.15f));
        DrawCircleV({perspX(srx, d), y}, 2.5f, ColorAlpha(Config::ROSE_GOLD, d * 0.15f));
    }
}

void Renderer::drawBeatLines(float gameTime) {
    float bp = fmodf(gameTime, Config::BEAT) / Config::BEAT;
    for (int b = 0; b < 14; b++) {
        float d = bp + (float)b * 0.5f;
        if (d < 0.02f || d > 1) continue;
        float y = perspY(d);
        float lx = perspX(Config::FIELD_X, d);
        float rx = perspX(Config::FIELD_X + Config::LANES * Config::LANE_W, d);
        DrawLine((int)lx, (int)y, (int)rx, (int)y, ColorAlpha(Config::ROSE_GOLD, d * 0.08f));
    }
}

void Renderer::drawNotes(const std::vector<Note>& notes, float gameTime) {
    for (auto& n : notes) {
        if (n.finished()) continue;

        float depth = noteDepth(n, gameTime);
        if (depth < -0.1f) continue;

        float cd = fmaxf(0.01f, fminf(depth, 1.2f));
        float ncx = Config::FIELD_X + (n.lane + 0.5f) * Config::LANE_W;
        float nx = perspX(ncx, cd);
        float nw = Config::LANE_W * 0.85f * cd;
        float nh = fmaxf(2, 14 * cd);
        Color pc = Config::PASTEL[n.lane];
        float glow = cd * cd;

        if (n.type == NoteType::HOLD) {
            // ── Hold 音符 ──
            float endDepth = 1.0f - (n.endTime - gameTime) * Config::SCROLL_SPEED / Config::TRACK_LEN;
            float headD = fmaxf(0.01f, fminf(cd, 1.0f));
            float tailD = fmaxf(0.01f, fminf(endDepth, 1.0f));

            // 身体（渐变条带）
            int seg = 28;
            for (int s = 0; s < seg; s++) {
                float t0 = (float)s / seg, t1 = (float)(s + 1) / seg;
                float d0 = headD + (tailD - headD) * t0;
                float d1 = headD + (tailD - headD) * t1;
                if (d1 < 0.01f) continue;
                d0 = fmaxf(0.01f, d0); d1 = fmaxf(0.01f, d1);

                float y0 = perspY(d0), y1 = perspY(d1);
                float sx0 = perspX(ncx, d0), sx1 = perspX(ncx, d1);
                float w0 = nw * (1 - t0 * 0.6f), w1 = nw * (1 - t1 * 0.6f);

                float segAlpha = glow * 0.35f;
                // 正在按住时更亮
                if (n.holding) segAlpha = glow * 0.55f;

                Color bc = n.holding ?
                    ColorAlpha((Color){(unsigned char)fminf(255, pc.r + 60),
                                       (unsigned char)fminf(255, pc.g + 60),
                                       (unsigned char)fminf(255, pc.b + 60), 255}, segAlpha * 0.6f)
                    : ColorAlpha(pc, segAlpha * 0.5f);
                DrawTriangle({sx0 - w0 / 2, y0}, {sx0 + w0 / 2, y0}, {sx1 - w1 / 2, y1}, bc);
                DrawTriangle({sx0 + w0 / 2, y0}, {sx1 + w1 / 2, y1}, {sx1 - w1 / 2, y1}, bc);

                // 中心亮线
                float cw0 = w0 * 0.12f, cw1 = w1 * 0.12f;
                DrawTriangle({sx0 - cw0, y0}, {sx0 + cw0, y0}, {sx1 - cw1, y1},
                             ColorAlpha(WHITE, segAlpha * 0.6f));
                DrawTriangle({sx0 + cw0, y0}, {sx1 + cw1, y1}, {sx1 - cw1, y1},
                             ColorAlpha(WHITE, segAlpha * 0.6f));
            }

            // 头部（和 tap 一样）
            float hy = perspY(headD);
            float hx = perspX(ncx, headD);
            float hw = Config::LANE_W * 0.85f * headD;
            float hh = fmaxf(2, 14 * headD);
            for (int g = 5; g >= 0; g--) {
                float ew = hw + g * 8 * headD, eh = hh + g * 5 * headD;
                DrawRectangleRec({hx - ew / 2, hy - eh / 2, ew, eh},
                                 ColorAlpha(pc, glow * 0.04f * (6 - g)));
            }
            DrawRectangleRec({hx - hw * 0.5f, hy - hh * 0.5f, hw, hh}, ColorAlpha(pc, glow * 0.8f));
            DrawRectangleRec({hx - hw * 0.35f, hy - hh * 0.35f, hw * 0.7f, hh * 0.7f},
                             ColorAlpha(WHITE, glow * 0.6f));

            // 尾部标记
            if (tailD > 0.01f && tailD < 1.1f) {
                float ty = perspY(tailD);
                float tx = perspX(ncx, tailD);
                float tw = Config::LANE_W * 0.7f * tailD;
                DrawRectangleRec({tx - tw / 2, ty - 3, tw, 6},
                                 ColorAlpha(pc, glow * 0.7f));
                DrawRectangleRec({tx - tw * 0.15f, ty - 2, tw * 0.3f, 4},
                                 ColorAlpha(WHITE, glow * 0.9f));
            }
        } else {
            // ── Tap 音符 ──
            if (depth > 1.15f) continue;
            // 光带尾巴
            for (int s = 20; s >= 0; s--) {
                float prog = (float)s / 20;
                float sd = cd - prog * 0.18f;
                if (sd < 0.01f) continue;
                float sy = perspY(sd);
                float sx = perspX(ncx, sd) + sinf(prog * PI * 4 - gameTime * 10) * 3.0f * (1 - prog) * cd;
                float sw = nw * (1 - prog * 0.85f);
                float sh = fmaxf(1, 4 * sd);
                float sa = (1 - prog * prog) * glow * 0.5f;
                DrawRectangleRec({sx - sw * 0.9f, sy - sh, sw * 1.8f, sh * 2}, ColorAlpha(pc, sa * 0.25f));
                DrawRectangleRec({sx - sw * 0.2f, sy - sh * 0.3f, sw * 0.4f, sh * 0.6f}, ColorAlpha(WHITE, sa * 0.5f));
            }
            // 头部
            for (int g = 6; g >= 0; g--) {
                float ew = nw + g * 10 * cd, eh = nh + g * 7 * cd;
                DrawRectangleRec({nx - ew / 2, Config::HIT_Y - (Config::HIT_Y - perspY(cd)) - eh / 2, ew, eh},
                                 ColorAlpha(pc, glow * 0.05f * (7 - g)));
            }
            float ny2 = perspY(cd);
            for (int g = 6; g >= 0; g--) {
                float ew = nw + g * 10 * cd, eh = nh + g * 7 * cd;
                DrawRectangleRec({nx - ew / 2, ny2 - eh / 2, ew, eh}, ColorAlpha(pc, glow * 0.05f * (7 - g)));
            }
            DrawRectangleRec({nx - nw * 0.5f, ny2 - nh * 0.5f, nw, nh}, ColorAlpha(pc, glow * 0.8f));
            DrawRectangleRec({nx - nw * 0.35f, ny2 - nh * 0.35f, nw * 0.7f, nh * 0.7f}, ColorAlpha(WHITE, glow * 0.6f));
            float coreW = nw * 0.18f, coreH = nh * 0.85f;
            DrawRectangleRec({nx - coreW / 2, ny2 - coreH / 2, coreW, coreH}, ColorAlpha(WHITE, glow * 0.95f));
            float dotR = fmaxf(1, 3.5f * cd);
            DrawCircleV({nx - nw * 0.35f, ny2}, dotR, ColorAlpha(Config::ROSE_GOLD, glow * 0.5f));
            DrawCircleV({nx + nw * 0.35f, ny2}, dotR, ColorAlpha(Config::ROSE_GOLD, glow * 0.5f));
        }
    }
}

void Renderer::drawHitLine(float beatPulse, const float laneFlash[]) {
    float le = Config::FIELD_X, re = Config::FIELD_X + Config::LANES * Config::LANE_W;
    for (int g = 4; g >= 0; g--) {
        float ex = (float)(g + 1) * 3;
        float a = (0.3f + beatPulse * 0.3f) * 0.06f * (5 - g);
        DrawRectangle(le - ex, Config::HIT_Y - 1 - ex, re - le + ex * 2, 2 + ex * 2,
                      ColorAlpha(Config::ROSE_GOLD, a));
    }
    DrawRectangle(le, Config::HIT_Y - 1, re - le, 2, ColorAlpha(Config::ROSE_GOLD, 0.8f + beatPulse * 0.2f));
    DrawCircleV({le - 4, Config::HIT_Y}, 5, ColorAlpha(Config::ROSE_GOLD, 0.7f));
    DrawCircleV({re + 4, Config::HIT_Y}, 5, ColorAlpha(Config::ROSE_GOLD, 0.7f));
    for (int i = 0; i < Config::LANES; i++) {
        float cx = Config::FIELD_X + (i + 0.5f) * Config::LANE_W;
        DrawCircleV({cx, Config::HIT_Y}, 3, ColorAlpha(Config::PASTEL[i], 0.3f + laneFlash[i] * 0.4f));
    }
}

void Renderer::drawReceptors(const float laneFlash[], const bool keysDown[]) {
    for (int i = 0; i < Config::LANES; i++) {
        float cx = Config::FIELD_X + (i + 0.5f) * Config::LANE_W;
        float cy = Config::HIT_Y + 36;
        if (laneFlash[i] > 0.1f) {
            for (int g = 3; g >= 0; g--)
                DrawCircleV({cx, Config::HIT_Y}, (18 + g * 14) * laneFlash[i],
                            ColorAlpha(Config::PASTEL[i], laneFlash[i] * 0.12f * (4 - g)));
            DrawCircleV({cx, Config::HIT_Y}, 10 * laneFlash[i], ColorAlpha(WHITE, laneFlash[i] * 0.4f));
        }
        if (laneFlash[i] > 0)
            DrawCircleV({cx, cy}, 20, ColorAlpha(Config::PASTEL[i], laneFlash[i] * 0.2f));
        DrawCircleV({cx, cy}, 18, ColorAlpha(Config::PASTEL_LIGHT[i], 0.6f + laneFlash[i] * 0.3f));
        DrawCircleLines((int)cx, (int)cy, 18, ColorAlpha(Config::ROSE_GOLD, 0.35f + laneFlash[i] * 0.3f));
        DrawText(Config::KEY_LABEL[i], (int)(cx - 5), (int)(cy - 6), 15,
                 keysDown[i] ? Config::ROSE_GOLD : ColorAlpha(Config::INK_LIGHT, 0.4f));
    }
}

void Renderer::drawParticles(const std::vector<Particle>& particles) {
    for (auto& p : particles) {
        float a = p.life / p.maxLife;
        if (p.sparkle) {
            drawSparkle(p.pos, p.size * a * 1.5f, ColorAlpha(p.color, a * 0.85f));
        } else {
            DrawCircleV(p.pos, p.size * a * 2.2f, ColorAlpha(p.color, a * 0.12f));
            DrawCircleV(p.pos, p.size * a, ColorAlpha(p.color, a * 0.8f));
        }
    }
}

void Renderer::drawScreenFlash(float flash) {
    if (flash > 0.01f)
        DrawRectangle(0, 0, Config::SW, Config::SH, ColorAlpha(WHITE, flash * 0.08f));
}

void Renderer::drawJudgment(JudgeResult judge, float elapsed) {
    if (judge == JudgeResult::NONE || elapsed > 0.6f) return;
    float a = 1 - elapsed / 0.6f;
    float sc = elapsed < 0.07f ? 1 + (0.07f - elapsed) * 8 : 1;
    const char* txt = "";
    Color jc = WHITE;
    if (judge == JudgeResult::PERFECT)      { txt = "PERFECT"; jc = {255, 150, 180, 255}; }
    else if (judge == JudgeResult::GREAT)    { txt = "GREAT";   jc = {130, 200, 255, 255}; }
    else if (judge == JudgeResult::GOOD)     { txt = "GOOD";    jc = {180, 220, 160, 255}; }
    else if (judge == JudgeResult::MISS)     { txt = "MISS";    jc = {220, 160, 160, 255}; }
    int fs = (int)(28 * sc);
    int tw = MeasureText(txt, fs);
    DrawText(txt, Config::SW / 2 - tw / 2 + 1, (int)(Config::HIT_Y - 80 - elapsed * 40) + 1, fs,
             ColorAlpha(Config::ROSE_GOLD, a * 0.2f));
    DrawText(txt, Config::SW / 2 - tw / 2, (int)(Config::HIT_Y - 80 - elapsed * 40), fs, ColorAlpha(jc, a));
}

void Renderer::drawUI(int score, int combo, float comboScale, float progress) {
    DrawText(TextFormat("SCORE  %08d", score), 15, 12, 20, Config::INK);
    if (combo > 2) {
        int fs = (int)(30 * comboScale);
        const char* ct = TextFormat("%d", combo);
        int tw = MeasureText(ct, fs);
        int cx = Config::SW / 2 - tw / 2, cy = (int)(Config::HIT_Y - 140);
        Color cc = combo > 50 ? (Color){255, 160, 185, 255}
                  : combo > 20 ? (Color){225, 160, 135, 255} : (Color){160, 140, 150, 255};
        DrawText(ct, cx - 1, cy - 1, fs, ColorAlpha(cc, 0.15f * comboScale));
        DrawText(ct, cx, cy, fs, cc);
        int cw = MeasureText("COMBO", 11);
        DrawText("COMBO", Config::SW / 2 - cw / 2, cy + fs + 2, 11, ColorAlpha(Config::ROSE_GOLD, 0.45f));
    }
    DrawRectangle(0, Config::SH - 3, (int)(Config::SW * progress), 3, ColorAlpha(Config::ROSE_GOLD, 0.5f));
}

void Renderer::drawCountdown(int count) {
    if (count <= 0) return;
    const char* txt;
    if (count >= 4)      txt = "READY";
    else if (count == 3) txt = "3";
    else if (count == 2) txt = "2";
    else                 txt = "1";

    float frac = fmodf(GetTime(), 1.0f);
    float scale = 1.0f + (1.0f - frac) * 0.3f;
    float alpha = 0.6f + (1.0f - frac) * 0.4f;
    int fs = (int)(80 * scale);
    int tw = MeasureText(txt, fs);
    int cx = Config::SW / 2 - tw / 2;
    int cy = Config::SH / 2 - fs / 2 - 40;

    DrawCircleV({(float)Config::SW / 2, (float)Config::SH / 2 - 40}, 100,
                ColorAlpha(Config::PASTEL[0], 0.08f));
    DrawText(txt, cx + 2, cy + 2, fs, ColorAlpha(Config::INK, 0.1f));
    DrawText(txt, cx, cy, fs, ColorAlpha(Config::ROSE_GOLD, alpha));
}

void Renderer::drawDemoOverlay(const std::string& title, float bgPhase) {
    // DEMO badge top-right
    float a = 0.6f + sinf(bgPhase * 6) * 0.3f;
    DrawRectangle(Config::SW - 140, 8, 132, 30, ColorAlpha(Config::PASTEL[0], 0.2f));
    DrawText("AUTO DEMO", Config::SW - 135, 13, 18, ColorAlpha(Config::PASTEL[0], a));

    // Song title bar at bottom
    int tw = MeasureText(title.c_str(), 20);
    DrawRectangle(Config::SW / 2 - tw / 2 - 15, Config::SH - 65, tw + 30, 28,
                  ColorAlpha(Config::INK, 0.15f));
    DrawText(title.c_str(), Config::SW / 2 - tw / 2, Config::SH - 62, 20,
             ColorAlpha(Config::ROSE_GOLD, 0.7f));

    // ESC hint
    DrawText("ESC to stop", Config::SW / 2 - 45, Config::SH - 35, 14,
             ColorAlpha(Config::INK_LIGHT, 0.3f));
}

void Renderer::drawMenu(float bgPhase) {
    ClearBackground(Config::BG_CREAM);
    for (auto& p : petals_) {
        float a = 0.2f + sinf(bgPhase * 2 + p.phase) * 0.15f;
        DrawCircleV({p.x, p.y}, p.size, ColorAlpha(p.tint, a));
    }
    for (int ring = 0; ring < 2; ring++) {
        float br = 100 + ring * 50;
        int n = 6 + ring * 3;
        for (int i = 0; i < n; i++) {
            float ang = bgPhase * (0.15f + ring * 0.08f) + (float)i / n * PI * 2;
            float r = br + sinf(bgPhase * 1.2f + i + ring) * 12;
            DrawCircleLines((int)(Config::SW / 2 + cosf(ang) * r),
                            (int)(Config::SH * 0.4f + sinf(ang) * r * 0.35f),
                            12 + ring * 6, ColorAlpha(Config::PASTEL[(i + ring) % 6], 0.12f));
        }
    }
    DrawText("aeacrA", Config::SW / 2 - 85, 140, 50, Config::PASTEL[0]);
    DrawText("aeacrA", Config::SW / 2 - 83, 138, 50, ColorAlpha(WHITE, 0.4f));
    DrawLineBezier({Config::SW / 2 - 200, 200}, {Config::SW / 2 + 200, 200}, 1, ColorAlpha(Config::ROSE_GOLD, 0.3f));
    DrawText("Keys:  S  D  F  J  K  L", Config::SW / 2 - 130, 310, 24, Config::INK_LIGHT);
    float a = 0.3f + sinf(bgPhase * 4) * 0.3f;
    DrawText("Press ENTER to start", Config::SW / 2 - 120, 390, 22, ColorAlpha(Config::ROSE_GOLD, a));
}

void Renderer::drawSelect(float bgPhase, const std::vector<SongEntry>& songs,
                          int selected, float scrollY, bool hasImport) {
    ClearBackground(Config::BG_CREAM);
    DrawText("SELECT SONG", Config::SW / 2 - 130, 40, 42, Config::ROSE_GOLD);

    float listTop = 120;
    int itemH = 70;

    for (int i = 0; i < (int)songs.size(); i++) {
        float y = listTop + i * itemH - scrollY;
        if (y + itemH < listTop || y > Config::SH - 80) continue;
        bool sel = (i == selected);
        Color accent = Config::PASTEL[i % 6];

        if (sel) {
            DrawRectangle(80, (int)(y + 4), Config::SW - 160, itemH - 8,
                          ColorAlpha(accent, 0.15f));
            DrawRectangleLinesEx({80, y + 4, (float)(Config::SW - 160), (float)(itemH - 8)},
                                 2, ColorAlpha(accent, 0.5f));
            DrawText(">", 70, (int)(y + 22), 20, accent);
        }

        DrawText(songs[i].title.c_str(), sel ? 120 : 110, (int)(y + 16),
                 sel ? 24 : 20, sel ? accent : ColorAlpha(Config::INK_LIGHT, 0.7f));
        DrawText(TextFormat("BPM %.0f", songs[i].bpm),
                 sel ? 120 : 110, (int)(y + 44), 13,
                 ColorAlpha(Config::INK_LIGHT, 0.45f));
    }

    float a = 0.3f + sinf(bgPhase * 4) * 0.3f;
    if (hasImport) {
        DrawText("ENTER play  A auto-demo  I import  UP/DOWN select  ESC back",
                 Config::SW / 2 - 270, Config::SH - 40, 17, ColorAlpha(Config::ROSE_GOLD, a));
    } else {
        DrawText("UP/DOWN select  ENTER play  ESC back",
                 Config::SW / 2 - 190, Config::SH - 40, 17, ColorAlpha(Config::ROSE_GOLD, a));
    }
}

void Renderer::drawImport(float bgPhase, const char* status, float progress) {
    ClearBackground(Config::BG_CREAM);
    for (auto& p : petals_)
        DrawCircleV({p.x, p.y}, p.size, ColorAlpha(p.tint, 0.06f));

    DrawText("IMPORT SONG", Config::SW / 2 - 130, 60, 42, Config::ROSE_GOLD);

    // Status text
    int tw = MeasureText(status, 22);
    DrawText(status, Config::SW / 2 - tw / 2, 220, 22, Config::INK);

    // Progress bar
    if (progress > 0) {
        float barW = 400, barH = 16;
        float bx = (Config::SW - barW) / 2;
        float by = 280;
        DrawRectangle((int)bx, (int)by, (int)barW, (int)barH,
                       ColorAlpha(Config::ROSE_GOLD, 0.2f));
        float fill = fminf(progress, 1.0f) * barW;
        Color barColor = progress >= 1.0f ? (Color){100, 200, 130, 255} : Config::PASTEL[1];
        DrawRectangle((int)bx, (int)by, (int)fill, (int)barH, barColor);
    } else if (progress < 0) {
        // Error state
        DrawText("Failed", Config::SW / 2 - 30, 280, 22, (Color){220, 100, 100, 255});
    }

    float a = 0.3f + sinf(bgPhase * 4) * 0.3f;
    DrawText("ESC to cancel", Config::SW / 2 - 55, Config::SH - 50, 17,
             ColorAlpha(Config::ROSE_GOLD, a));
}

void Renderer::drawResults(float bgPhase, int score, int maxCombo,
                           const int counts[4], size_t totalNotes) {
    ClearBackground(Config::BG_CREAM);
    for (auto& p : petals_) { DrawCircleV({p.x, p.y}, p.size, ColorAlpha(p.tint, 0.1f)); }
    DrawText("RESULTS", Config::SW / 2 - 100, 35, 38, Config::ROSE_GOLD);
    const char* lb[] = {"PERFECT", "GREAT", "GOOD", "MISS"};
    Color lc[] = {{255, 150, 180, 255}, {130, 200, 255, 255}, {180, 220, 160, 255}, {220, 160, 160, 255}};
    for (int i = 0; i < 4; i++)
        DrawText(TextFormat("%s : %d", lb[i], counts[i]), Config::SW / 2 - 90, 110 + i * 40, 24, lc[i]);
    DrawText(TextFormat("Score: %d", score), Config::SW / 2 - 90, 300, 32, Config::INK);
    DrawText(TextFormat("Max Combo: %d", maxCombo), Config::SW / 2 - 105, 345, 24, Config::ROSE_GOLD);
    int mx = (int)totalNotes * 350;
    float r = mx > 0 ? (float)score / mx : 0;
    const char* g = r > 0.95f ? "S" : r > 0.85f ? "A" : r > 0.7f ? "B" : r > 0.5f ? "C" : "D";
    Color gc = r > 0.95f ? (Color){255, 180, 200, 255} : r > 0.85f ? (Color){150, 210, 255, 255} : Config::INK;
    DrawText(g, Config::SW / 2 - 25, 395, 64, gc);
    float a2 = 0.3f + sinf(bgPhase * 4) * 0.3f;
    DrawText("Press ENTER", Config::SW / 2 - 65, 510, 20, ColorAlpha(Config::ROSE_GOLD, a2));
}
