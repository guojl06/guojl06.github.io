#include "ParticleSystem.h"
#include <cstdlib>
#include <algorithm>

void ParticleSystem::clear() { particles_.clear(); }

void ParticleSystem::update(float dt) {
    for (auto& p : particles_) {
        p.pos.x += p.vel.x * dt;
        p.pos.y += p.vel.y * dt;
        p.vel.y += 400.0f * dt;
        p.vel.x *= 0.97f;
        p.life -= dt;
    }
    particles_.erase(
        std::remove_if(particles_.begin(), particles_.end(),
                       [](const Particle& p) { return p.life <= 0; }),
        particles_.end());
}

void ParticleSystem::spawnExplosion(float x, float y, int lane) {
    for (int i = 0; i < 25; i++) {
        float ang = (float)rand() / RAND_MAX * PI * 2;
        float spd = 50 + (float)rand() / RAND_MAX * 350;
        Color pc = (i % 3 == 0) ? (Color){255, 255, 255, 255}
                   : (i % 3 == 1) ? Config::PASTEL[rand() % 6]
                                  : Config::PASTEL[lane];
        particles_.push_back({{x, y},
                              {cosf(ang) * spd, sinf(ang) * spd - 260},
                              pc,
                              0.35f + (float)(rand() % 30) / 100,
                              0.65f,
                              1.5f + (float)(rand() % 40) / 10,
                              i % 3 == 0});
    }
}

void ParticleSystem::spawnSpiral(float x, float y, float time, int lane) {
    for (int i = 0; i < 8; i++) {
        float ang = (float)i / 8 * PI * 2 + time * 4;
        float spd = 100 + (float)rand() / RAND_MAX * 150;
        particles_.push_back({{x, y},
                              {cosf(ang) * spd, sinf(ang) * spd - 130},
                              Config::PASTEL[(lane + i) % 6],
                              0.5f + (float)(rand() % 20) / 100,
                              0.6f,
                              2.5f + (float)(rand() % 30) / 10,
                              false});
    }
}

void ParticleSystem::spawnFire(float x, float y) {
    for (int i = 0; i < 6; i++) {
        float a = -PI / 2 + ((float)(rand() % 100) / 100 - 0.5f) * 0.4f;
        float s = 180 + (float)(rand() % 180);
        particles_.push_back({{x + (float)(rand() % 60 - 30), y},
                              {cosf(a) * s, sinf(a) * s},
                              Config::PASTEL[rand() % 6],
                              0.3f + (float)(rand() % 20) / 100,
                              0.45f,
                              3 + (float)(rand() % 30) / 10,
                              true});
    }
}
