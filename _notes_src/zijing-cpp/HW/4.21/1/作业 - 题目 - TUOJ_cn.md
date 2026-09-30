# 战斗单位模拟器

## 背景

在**永恒竞技场**的世界中，玩家指挥一支由不同战斗职业单位组成的队伍。每个职业都有其独特的能力和战斗风格。

有些单位擅长近战，有些则专注于远程攻击、魔法伤害、防御或治疗盟友。理解每个职业的行为是掌控战场的关键。

给定一组描述单位之间战斗的命令序列。你的任务是完成不同单位类的实现，并正确模拟整个系统。

---

## 单位类型

游戏中共有五种单位：

### 战士（Warrior）

* 对目标造成恰好 `atk` 点伤害。

### 弓箭手（Archer）

* 造成 `atk` 点伤害。
* 如果目标当前 HP **大于 50**，额外造成 `10` 点伤害。

### 法师（Mage）

* 造成 `atk + 15` 点伤害。
* 攻击后，法师自身损失 `5` 点 HP。
* HP 不会低于 `0`。

### 坦克（Tank）

* 造成 `atk` 点伤害。
* 受到伤害时，只承受其 **70%**，向下取整。

### 治疗者（Healer）

* 不造成伤害。
* 而是恢复目标 `atk` 点 HP。
* HP 不能超过目标的最大 HP。

---

## 规则

* 单位 HP 变为 `0` 时视为**死亡**。
* 死亡单位：
  + 不能攻击
  + 不能被治疗
* 如果攻击者或目标已死亡，操作无效。
* 每个单位的最大 HP 等于其初始 HP。

---

## 输入格式

第一行包含一个整数 `Q` —— 操作数量。

接下来 `Q` 行，每行为以下命令之一：

### 创建单位

```
CREATE type name hp atk
```

* `type` 为以下之一：`Warrior`、`Archer`、`Mage`、`Tank`、`Healer`
* `name` 是唯一字符串

---

### 攻击或治疗

```
ATTACK attacker target
```

* 如果攻击者是 `Healer`，此操作改为治疗目标而非造成伤害。

---

### 查询当前 HP

```
STATUS name
```

---

### 查询存活状态

```
ALIVE name
```

---

## 输出格式

* 对于每个 `STATUS` 操作，输出当前 HP。
* 对于每个 `ALIVE` 操作：
  + 如果单位存活，输出 `YES`
  + 否则输出 `NO`

---

## 数据范围

* `1 ≤ Q ≤ 2 × 10^5`
* `1 ≤ hp, atk ≤ 10^4`
* 所有单位名称唯一。
* 保证所有查询或被攻击的单位名称在之前已创建。

---

## 样例输入

```
12
CREATE Warrior A 100 20
CREATE Archer B 80 15
CREATE Mage C 70 25
CREATE Tank D 120 10
CREATE Healer E 60 12
ATTACK A D
STATUS D
ATTACK B D
STATUS D
ATTACK C A
STATUS C
STATUS A
```

---

## 样例输出

```
106
89
65
60
```

---

## 解释

* 战士造成 20 点伤害 → 坦克承受 `floor(20 × 0.7) = 14`
* 弓箭手造成 15 + 10（加成）= 25 → 坦克承受 17
* 法师造成 40 点伤害并损失 5 HP

---

## 提供的代码

以下是评测系统提供的代码。你必须**保持所有提供的代码不变**，只完成缺失的派生类实现。
请注意，战士的代码已经完成，供你参考。

```
#include <bits/stdc++.h>
using namespace std;

class Unit {
protected:
    string name;
    int hp;
    int maxHp;
    int atk;

public:
    Unit(string name, int hp, int atk)
        : name(std::move(name)), hp(hp), maxHp(hp), atk(atk) {}

    virtual ~Unit() = default;

    string getName() const { return name; }
    int getHp() const { return hp; }
    int getAtk() const { return atk; }
    bool isAlive() const { return hp > 0; }

    virtual void attack(Unit& target) = 0;

    virtual void takeDamage(int damage) {
        if (!isAlive()) return;
        hp -= damage;
        if (hp < 0) hp = 0;
    }

    void heal(int val) {
        if (!isAlive()) return;
        hp = min(maxHp, hp + val);
    }
};

class Warrior : public Unit {
public:
    Warrior(string name, int hp, int atk) : Unit(std::move(name), hp, atk) {}

    void attack(Unit& target) override {
        if (!isAlive() || !target.isAlive()) return;
        target.takeDamage(atk);
    }
};

class Archer : public Unit {
public:
    Archer(string name, int hp, int atk) : Unit(std::move(name), hp, atk) {}

    // TODO: implement this class
};

class Mage : public Unit {
public:
    Mage(string name, int hp, int atk) : Unit(std::move(name), hp, atk) {}

    // TODO: implement this class
};

class Tank : public Unit {
public:
    Tank(string name, int hp, int atk) : Unit(std::move(name), hp, atk) {}

    // TODO: implement this class
};

class Healer : public Unit {
public:
    Healer(string name, int hp, int atk) : Unit(std::move(name), hp, atk) {}

    // TODO: implement this class
};

class BattleField {
private:
    unordered_map<string, unique_ptr<Unit>> units;

public:
    void createUnit(const string& type, const string& name, int hp, int atk) {
        if (type == "Warrior") {
            units[name] = make_unique<Warrior>(name, hp, atk);
        } else if (type == "Archer") {
            units[name] = make_unique<Archer>(name, hp, atk);
        } else if (type == "Mage") {
            units[name] = make_unique<Mage>(name, hp, atk);
        } else if (type == "Tank") {
            units[name] = make_unique<Tank>(name, hp, atk);
        } else if (type == "Healer") {
            units[name] = make_unique<Healer>(name, hp, atk);
        }
    }

    void attack(const string& attacker, const string& target) {
        auto itA = units.find(attacker);
        auto itB = units.find(target);
        if (itA == units.end() || itB == units.end()) return;
        itA->second->attack(*itB->second);
    }

    int status(const string& name) const {
        auto it = units.find(name);
        if (it == units.end()) return 0;
        return it->second->getHp();
    }

    bool alive(const string& name) const {
        auto it = units.find(name);
        if (it == units.end()) return false;
        return it->second->isAlive();
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int Q;
    cin >> Q;

    BattleField bf;

    while (Q--) {
        string op;
        cin >> op;

        if (op == "CREATE") {
            string type, name;
            int hp, atk;
            cin >> type >> name >> hp >> atk;
            bf.createUnit(type, name, hp, atk);
        } else if (op == "ATTACK") {
            string a, b;
            cin >> a >> b;
            bf.attack(a, b);
        } else if (op == "STATUS") {
            string name;
            cin >> name;
            cout << bf.status(name) << '\n';
        } else if (op == "ALIVE") {
            string name;
            cin >> name;
            cout << (bf.alive(name) ? "YES" : "NO") << '\n';
        }
    }

    return 0;
}
```

---

## 你需要提交的内容

战士已经作为示例完整实现。
你只需完成以下四个派生类中缺失的部分：

* `Archer`
* `Mage`
* `Tank`
* `Healer`

换言之，在所有提供的代码中，你唯一需要实现的只有这些派生类各自特有的行为。

---

## 重要注意事项

* 你必须使用从 `Unit` **继承**。
* 你必须通过**重写虚函数**来实现行为。
* 不要修改 `Unit`、`BattleField` 或 `main`。
* 不要添加全局逻辑来绕过类设计。
* 你的实现必须完全符合指定的行为。
* 评测使用 C++14 或更高版本。

---

## 目标

补全这些派生类的缺失实现，使整个程序正确运行。
