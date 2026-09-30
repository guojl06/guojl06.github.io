# Battle Unit Simulator

## Background

In the world of **Eternal Arena**, players command a team of units from different combat classes. Each class has its own unique abilities and combat style.

Some units excel in direct melee combat, while others specialize in ranged attacks, magic damage, defense, or healing allies. Understanding how each class behaves is essential to mastering the battlefield.

You are given a sequence of commands describing battles between units. Your task is to complete the implementation of different unit classes and simulate the system correctly.

---

## Unit Classes

There are five types of units in the game:

### Warrior

* Deals exactly `atk` damage to the target.

### Archer

* Deals `atk` damage.
* If the target's current HP is **greater than 50**, deals an additional `10` damage.

### Mage

* Deals `atk + 15` damage.
* After attacking, the Mage loses `5` HP.
* HP cannot go below `0`.

### Tank

* Deals `atk` damage.
* When receiving damage, only takes **70% of it**, rounded down.

### Healer

* Does not deal damage.
* Instead, restores `atk` HP to the target.
* HP cannot exceed the target's maximum HP.

---

## Rules

* A unit is considered **dead** if its HP becomes `0`.
* Dead units:
  + Cannot attack
  + Cannot be healed
* If either the attacker or the target is dead, the operation has no effect.
* Each unit's maximum HP is equal to its initial HP.

---

## Input Format

The first line contains an integer `Q` — the number of operations.

Each of the next `Q` lines is one of the following commands:

### Create a unit

```
CREATE type name hp atk
```

* `type` is one of: `Warrior`, `Archer`, `Mage`, `Tank`, `Healer`
* `name` is a unique string

---

### Attack or heal

```
ATTACK attacker target
```

* If the attacker is a `Healer`, this operation heals the target instead of dealing damage.

---

### Query current HP

```
STATUS name
```

---

### Query alive status

```
ALIVE name
```

---

## Output Format

* For each `STATUS` operation, output the current HP.
* For each `ALIVE` operation:
  + Output `YES` if the unit is alive
  + Output `NO` otherwise

---

## Constraints

* `1 ≤ Q ≤ 2 × 10^5`
* `1 ≤ hp, atk ≤ 10^4`
* All unit names are unique.
* It is guaranteed that every queried or attacked unit name has been created before.

---

## Sample Input

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

## Sample Output

```
106
89
65
60
```

---

## Explanation

* Warrior deals 20 damage → Tank receives `floor(20 × 0.7) = 14`
* Archer deals 15 + 10 (bonus) → 25 → Tank receives 17
* Mage deals 40 damage and loses 5 HP

---

## Provided Code

The following code is provided by the judge. You must **keep all provided code unchanged** and only complete the missing derived-class implementations.
Please note that the code for the warrior has already been completed for your reference.

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

## What You Need to Submit

Warrior has already been fully implemented as an example.
You only need to complete the missing parts in the following four derived classes:

* `Archer`
* `Mage`
* `Tank`
* `Healer`

In other words, among all the provided code, the only parts left for you to implement are the class-specific behaviors of these five derived classes.

---

## Important Notes

* You must use **inheritance** from `Unit`.
* You must implement behavior through **overriding virtual functions**.
* Do not modify `Unit`, `BattleField`, or `main`.
* Do not add global logic to bypass the class design.
* Your implementation must match the specified behavior exactly.
* The judge uses C++14 or later.

---

## Goal

Fill in the missing implementations of the five derived classes so that the whole program works correctly.
