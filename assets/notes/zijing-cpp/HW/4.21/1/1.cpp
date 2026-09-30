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
    void attack(Unit& target) override {
        if (!isAlive() || !target.isAlive()) return;
        if(target.getHp() > 50) target.takeDamage(10);
        target.takeDamage(atk);
    }
    // TODO: implement this class
};

class Mage : public Unit {
public:
    Mage(string name, int hp, int atk) : Unit(std::move(name), hp, atk) {}
    void attack(Unit& target) override {
        if (!isAlive() || !target.isAlive()) return;
        target.takeDamage(15+atk);
        this->takeDamage(min(hp,5));
    }
    // TODO: implement this class
};

class Tank : public Unit {
public:
    Tank(string name, int hp, int atk) : Unit(std::move(name), hp, atk) {}
    void attack(Unit& target) override {
        if (!isAlive() || !target.isAlive()) return;
        target.takeDamage(atk);
    }
    void takeDamage(int damage) {
        if (!isAlive()) return;
        hp -= int(damage*0.7);
        if (hp < 0) hp = 0;
    }
    // TODO: implement this class
};

class Healer : public Unit {
public:
    Healer(string name, int hp, int atk) : Unit(std::move(name), hp, atk) {}
    void attack(Unit& target) override {
        if (!isAlive() || !target.isAlive()) return;
        target.heal(atk);
    }
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