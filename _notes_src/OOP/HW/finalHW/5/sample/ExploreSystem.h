#pragma once

#include <string>

class Player{
};

class Dungeon{
public:
    float startExplore(Player* player);
};

Player* createPlayer(std::string weaponName, float weaponValue, std::string toolName);
Dungeon* createDungeon(std::string dungeonName, int level);
