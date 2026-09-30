#include "ExploreSystem.h"

#include <iomanip>
#include <iostream>

void test_sample1() {
    std::cout << "Test Sample 1:" << std::endl;

    Player* player = createPlayer("sword", 20, "torch");
    Dungeon* dungeon = createDungeon("normal", 5);

    float reward = dungeon->startExplore(player);
    std::cout << "Reward: " << reward << std::endl;

    delete player;
    delete dungeon;
}

void test_sample2() {
    std::cout << "Test Sample 2:" << std::endl;

    Player* player = createPlayer("staff", 8, "torch");
    Dungeon* dungeon = createDungeon("weaponenhance", 10);

    for (int i = 0; i < 4; i++) {
        float reward = dungeon->startExplore(player);
        std::cout << "Round " << i << " reward: " << reward << std::endl;
    }

    delete player;
    delete dungeon;
}

int main() {
    std::cout << std::fixed << std::setprecision(2);
    test_sample1();
    test_sample2();
    return 0;
}
