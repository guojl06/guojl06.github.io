#pragma once
#include <string>

class Weapon {
public:
    virtual float getScore(int level) = 0;
    virtual void enhance() = 0;
    virtual ~Weapon() {}
};

class Sword : public Weapon {
    float power;
public:
    Sword(float p) : power(p) {}
    float getScore(int level);
    void enhance();
};

class Staff : public Weapon {
    float magic;
public:
    Staff(float m) : magic(m) {}
    float getScore(int level);
    void enhance();
};

class Dagger : public Weapon {
public:
    Dagger(float v) {}
    float getScore(int level);
    void enhance();
};

class Tool {
public:
    virtual float getScore() = 0;
    virtual ~Tool() {}
};

class Torch : public Tool {
public:
    float getScore();
};

class Detector : public Tool {
public:
    float getScore();
};

class Toolkit : public Tool {
public:
    float getScore();
};

class Player {
    Weapon* weapon;
    Tool* tool;
    bool toolSealed;
public:
    Player(Weapon* w, Tool* t) : weapon(w), tool(t), toolSealed(false) {}
    virtual ~Player();
    float getWeaponScore(int level);
    float getToolScore();
    void sealTool();
    void enhanceWeapon();
};

class Dungeon {
protected:
    int level;
public:
    Dungeon(int l) : level(l) {}
    virtual ~Dungeon() {}
    virtual float startExplore(Player* player) = 0;
};

class NormalDungeon : public Dungeon {
public:
    NormalDungeon(int l) : Dungeon(l) {}
    float startExplore(Player* player);
};

class ToolSealDungeon : public Dungeon {
public:
    ToolSealDungeon(int l) : Dungeon(l) {}
    float startExplore(Player* player);
};

class WeaponEnhanceDungeon : public Dungeon {
public:
    WeaponEnhanceDungeon(int l) : Dungeon(l) {}
    float startExplore(Player* player);
};

Player* createPlayer(std::string weaponName, float weaponValue, std::string toolName);
Dungeon* createDungeon(std::string dungeonName, int level);
