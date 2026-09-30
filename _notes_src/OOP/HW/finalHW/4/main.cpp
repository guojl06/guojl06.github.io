#include <iostream>
#include "LegacySkill.h"
// 类和接口的声明都在 GameSkill.h 中
#include "GameSkill.h"

int main() {
    std::cout << "--- Game Skill System Test Start ---\n\n";

    // 1. 实例化上古技能 (Legacy Engine)
    LegacySkill* legacySkill = new LegacySkill();

    // 2. 将上古技能转换为 ISkill 接口
    ISkill* adapter = new LegacySkillAdapter(legacySkill);

    // 3. 叠加毒属性 Buff (+15 伤害)
    ISkill* poisonedSkill = new PoisonBuff(adapter);

    // 4. 叠加暴击 Buff (伤害 * 2)
    // 注意：嵌套顺序为 Crit(Poison(Adapter))
    ISkill* ultimateSkill = new CritBuff(poisonedSkill);

    // 5. 加入 MP 校验系统
    // 设定角色初始 MP 为 50，该技能每次释放消耗 20 MP
    ISkill* systemProxy = new MpChecker(ultimateSkill, 50, 20);

    // 第一次释放（此时 MP=50，充足）
    std::cout << ">> Cast 1:" << std::endl;
    int dmg1 = systemProxy->cast();
    std::cout << "Final Damage: " << dmg1 << "\n\n";

    // 第二次释放（此时 MP=30，依然充足）
    std::cout << ">> Cast 2:" << std::endl;
    int dmg2 = systemProxy->cast();
    std::cout << "Final Damage: " << dmg2 << "\n\n";

    // 第三次释放（此时 MP=10，不足，触发代理拦截）
    std::cout << ">> Cast 3:" << std::endl;
    int dmg3 = systemProxy->cast();
    std::cout << "Final Damage: " << dmg3 << "\n\n";

    // 内存清理（大家务必记得实现虚析构函数）
    delete systemProxy;
    
    std::cout << "--- Game Skill System Test End ---\n";
    return 0;
}
