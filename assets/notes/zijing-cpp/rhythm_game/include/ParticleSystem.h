#pragma once
#include "Config.h"
#include <vector>

struct Particle {
    Vector2 pos, vel;
    Color color;
    float life, maxLife, size;
    bool sparkle;
};

class ParticleSystem {
public:
    void update(float dt);
    void clear();

    void spawnExplosion(float x, float y, int lane);
    void spawnSpiral(float x, float y, float time, int lane);
    void spawnFire(float x, float y);

    const std::vector<Particle>& particles() const { return particles_; }

private:
    std::vector<Particle> particles_;
};
