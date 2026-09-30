# Chapter11\_Polymorphism

# Chapter 11: Polymorphism \& Virtual Functions

**Prerequisites:** Classes, inheritance, pointers/references, basic raylib game loop
**Next chapter preview:** Smart pointers, rule\-of\-five, and integrating polymorphic chess into a full game engine

> **Bridge from earlier chapters:** In previous chapters you learned **classes** \(blueprints for data \+ behavior\) and **inheritance** \(`class Pawn : public Piece` — "a Pawn *is a* Piece"\)\. This chapter adds **polymorphism**: one base\-class interface, many derived\-class behaviors — chosen at **runtime**\.

### Reading Map

|Section|Content|Priority|
|---|---|---|
|§0|Inheritance review via card game design|**Review** \(read first if rusty\)|
|§1|Why games need polymorphism|**Essential**|
|§2|`virtual` functions and syntax|**Essential**|
|§3|Pure virtual / abstract classes|**Essential**|
|§4|Chess \+ raylib lab|**Lab** \(build in phases\)|
|§5|Multi\-layer UI lab|**Lab** \(optional second project\)|
|§6|Summary and common mistakes|**Review**|

### Before You Read — Quick Recap

|Topic|One\-line reminder|Tiny example|
|---|---|---|
|**Inheritance**|Derived class gets base class members|`class MonsterCard : public Card { ... };` — see **§0**|
|**Pointer**|Stores an address; can point at different object types|`Piece* p = new Pawn(...);`|
|**Reference**|Alias for an object; also enables polymorphism|`Piece& ref = pawn;`|
|**Compile time**|When the compiler translates your code to an executable|Error messages appear here|
|**Runtime**|When the program actually runs|Virtual calls resolved here|
|**raylib**|A C library for 2D games \(window, drawing, input\)|`InitWindow(...)`, `DrawText(...)`|

> **Plain English — polymorphism:** One remote control \(`Piece*`\), many devices \(Pawn, Rook, Knight\)\. Press "move" and the *correct* device responds — you don't need a separate remote for each type\.

> **Plain English — vtable:** When you call `obj->update()`, C\+\+ looks up a small **vtable** \(virtual table\) attached to the real object and runs the matching function \(e\.g\. `Enemy::update`, not `GameObject::update`\)\.

---

## Bilingual Reference Tables

### Table 1: Core Concepts

|Chinese \(中文\)|English|Description|
|---|---|---|
|多态|Polymorphism|One interface, many implementations; the correct behavior is chosen at runtime\.|
|虚函数|Virtual function|A member function marked `virtual` that can be overridden in derived classes\.|
|重写|Override|Provide a new implementation of a virtual function in a subclass\.|
|纯虚函数|Pure virtual function|A virtual function with no base implementation; forces subclasses to define it\.|
|抽象类|Abstract class|A class with at least one pure virtual function; cannot be instantiated directly\.|
|动态绑定|Dynamic binding<br>|The program calls the function belonging to the *actual object type*, not the pointer type\.|
|静态绑定|Static binding|The compiler picks the function at compile time \(non\-virtual calls\)\.|
|基类指针|Base class pointer|`Piece*` can point to `Pawn`, `Rook`, etc\., enabling uniform treatment\.|
|接口|Interface|A set of operations \(often an abstract class\) that concrete types must implement\.|
|vtable|Virtual table|Compiler\-generated table mapping virtual calls to the correct function\.|

### Table 2: Symbols \& Keywords

|Symbol / Keyword|English Name|Chinese \(中文\)|Usage / Meaning|
|---|---|---|---|
|`virtual`|Virtual specifier|虚|Declares a function that derived classes may override\.|
|`= 0`|Pure virtual suffix|纯虚标记|After a virtual declaration, makes the function pure virtual\.|
|`override`|Override specifier|重写标记|Documents intent; compiler checks that a base virtual is overridden\.|
|`final`|Final specifier|最终|Prevents further overriding of a virtual function\.|
|`->`|Arrow operator|箭头运算符|Dereference pointer and access member: `ptr->draw()`\.|
|`*`|Dereference|解引用|Access object through pointer: `(*ptr).draw()`\.|
|`delete`|Delete operator|释放|`delete ptr` frees memory allocated with `new`\.|
|`virtual ~Class()`|Virtual destructor|虚析构函数|Ensures derived destructors run when deleting through base pointer\.|

### Table 3: Chapter\-Specific Terms

|English|Chinese \(中文\)|Explanation|
|---|---|---|
|Runtime polymorphism|运行时多态|Behavior depends on the real object type when calling through a base pointer/reference\.|
|Abstract base class \(ABC\)|抽象基类|Defines common interface; subclasses fill in details\.|
|Uniform collection|统一容器|`std::vector<Piece*>` holds different piece types together\.|
|Game screen stack|界面栈|UI layers \(menu, settings, gameplay\) managed polymorphically\.|
|Slicing|对象切片|Copying derived object into base variable loses derived data — avoid for polymorphism\.|
|Upcasting|向上转型|`Pawn*` → `Piece*` is safe and common\.|
|Base class|基类|Common blueprint shared by derived types; e\.g\. `Card`\.|
|Derived class|派生类|Specialized subclass; e\.g\. `MonsterCard : public Card`\.|
|Virtual base class|虚基类|`virtual public` inheritance to ensure one shared base in a diamond\.|
|Friend|友元|Trusted class or function granted access to private members\.|

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MWFhODk4ZTFmZDQ0NzQzZGNjNjY3MjM3MDIxNzc4NDJfNWI3OTQ5YzhhNTA2NGFlZWRhNjJmMGFiNDQ3Y2JlOTlfSUQ6NzY0MTgzMjE3OTE4NTU1MjU5NF8xNzgxMDYwMTgzOjE3ODExNDY1ODNfVjM)



---

## 0\. Review: Inheritance Through Card Game Design

> **Purpose of this section:** We review **inheritance** from earlier chapters — base class, derived class, access control, `friend`, and **virtual base class** \(虚基类\) — using one coherent **card battle game** design\. Runtime polymorphism and `virtual` **member functions** \(虚函数\) are introduced starting in §1–§2, not here\.

### The Problem: Modeling Many Card Types Without Chaos

You are designing a simplified **trading card battle game** \(a classroom TCG prototype\)\. The game has:

- **Monster cards** — attack/defense, fight on the field

- **Spell cards** — one\-shot effects when played from hand

- **Trap cards** — hidden until triggered

- A **deck** \(draw pile\), **hand** \(playable cards\), and **field** \(cards in play\)

A naive design stores everything as one struct:

```C++
struct RawCard {
    int type;       // 0=monster, 1=spell, 2=trap — magic numbers!
    string name;
    int cost;
    int attack;     // meaningless for spells
    int defense;
    string effectText;
};
```

**Problems:**

1. **No type safety** — `attack` on a spell compiles but is nonsense\.

2. **Giant ****`switch(type)`** — play, draw, and resolve effects all branch on `type`\.

3. **Hard to extend** — new card kinds touch every switch\.

4. **Duplicated fields** — every card has `name` and `cost`, copy\-pasted per type\.

> **Opening Question**: How do we express "every card is a card, but each *kind* has different fields and methods" in C\+\+ using class hierarchy alone?

**Answer:** **Inheritance** — a **base class** defines what all cards share; **derived classes** add specialized data and behavior\.

```Plaintext
classDiagram
    class Card {
        #id_: int
        #name_: string
        #cost_: int
        +getName() string
        +getCost() int
        +printSummary() void
    }
    class MonsterCard {
        -attack_: int
        -defense_: int
        +describe() void
        +fight(other) void
    }
    class SpellCard {
        -effectId_: int
        +describe() void
        +cast(target) void
    }
    class TrapCard {
        -triggerCondition_: string
        +describe() void
        +reveal() void
    }
    class Deck {
        -cards_: Card*
        +draw() Card*
        +shuffle() void
    }
    class Hand {
        -cards_: Card*
        +play(index) void
    }
    Card <|-- MonsterCard
    Card <|-- SpellCard
    Card <|-- TrapCard
    Deck o-- Card : holds
    Hand o-- Card : holds
```

*Figure 0A: Card game hierarchy — inheritance for card types, aggregation for deck/hand\.*

---

### 0\.1 Base Class `Card` — The Common Blueprint

A **base class** \(基类\) captures what **every** card has\.

|Role|In the card game|C\+\+ idea|
|---|---|---|
|**Identity**|Card ID, display name|Member variables in base|
|**Economy**|Mana cost to play|Shared `cost_`|
|**Shared behavior**|Print name and cost|Method in base \(e\.g\. `printSummary()`\)|

```C++
// cards/card.h — base class for all card types
#ifndef CARD_H
#define CARD_H

#include <string>
#include <iostream>

class Card {
public:
    Card(int id, const std::string& name, int cost)
        : id_(id), name_(name), cost_(cost) {}

    ~Card() = default;

    int getId() const { return id_; }
    const std::string& getName() const { return name_; }
    int getCost() const { return cost_; }

    void printSummary() const {
        std::cout << "[" << id_ << "] " << name_
                  << " (cost " << cost_ << ")\n";
    }

protected:
    int id_;
    std::string name_;
    int cost_;
};

#endif
```

> **Plain English — base class:** `Card` is the **family name**\. Monster, Spell, and Trap are **family members** sharing the address book \(`id_`, `name_`, `cost_`\) but each has a specialty\.

**Key syntax:**

```C++
class Derived : public Base { ... };
//            ^^^^^^ usually public for "is-a" relationships
```

|Inheritance keyword|Meaning|Card game usage|
|---|---|---|
|`public`|Public base members stay public in derived|`MonsterCard` **is a** `Card`|
|`protected`|Base `protected` → `protected` in derived|`cost_` visible to subclasses, not `main()`|
|`private` inheritance|Rare; implementation detail|Not used for card subtypes|

---

### 0\.2 Derived Classes — Specialized Card Types

A **derived class** \(派生类\) **extends** the base: inherits members and adds its own\.

#### Example 1: Minimal — `MonsterCard`

```C++
// cards/monster_card.h
#ifndef MONSTER_CARD_H
#define MONSTER_CARD_H

#include "card.h"

class MonsterCard : public Card {
public:
    MonsterCard(int id, const std::string& name, int cost,
                int attack, int defense)
        : Card(id, name, cost), attack_(attack), defense_(defense) {}

    void describe() const {
        printSummary();
        std::cout << "  Monster ATK/DEF: " << attack_ << "/" << defense_ << "\n";
    }

    void fight(MonsterCard& opponent) {
        std::cout << name_ << " attacks " << opponent.name_ << "!\n";
        opponent.defense_ -= attack_;
    }

private:
    int attack_;
    int defense_;
};

#endif
```

#### Example 2: Basic — `SpellCard` and `TrapCard`

```C++
// cards/spell_card.h
class SpellCard : public Card {
public:
    SpellCard(int id, const std::string& name, int cost, int effectId)
        : Card(id, name, cost), effectId_(effectId) {}

    void describe() const {
        printSummary();
        std::cout << "  Spell effect #" << effectId_ << "\n";
    }

    void cast(int targetPlayerId) {
        std::cout << "Casting " << name_ << " on player "
                  << targetPlayerId << "\n";
    }

private:
    int effectId_;
};

// cards/trap_card.h
class TrapCard : public Card {
public:
    TrapCard(int id, const std::string& name, int cost,
             const std::string& trigger)
        : Card(id, name, cost), trigger_(trigger), faceDown_(true) {}

    void describe() const {
        if (faceDown_)
            std::cout << "[Hidden trap]\n";
        else {
            printSummary();
            std::cout << "  Trap when: " << trigger_ << "\n";
        }
    }

    void reveal() { faceDown_ = false; }

private:
    std::string trigger_;
    bool faceDown_;
};
```

#### Example 3: Structured — store by base pointer, use shared base API

```C++
#include <vector>
#include "card.h"
#include "monster_card.h"
#include "spell_card.h"
#include "trap_card.h"

int main() {
    // Upcasting: each derived object can be stored as Card*
    std::vector<Card*> hand;
    hand.push_back(new MonsterCard(1, "Fire Dragon", 5, 4, 3));
    hand.push_back(new SpellCard(2, "Lightning", 2, 101));
    hand.push_back(new TrapCard(3, "Counter", 1, "opponent attacks"));

    // Through Card*, only Card members are available (no describe() on base)
    for (Card* c : hand)
        c->printSummary();

    // Type-specific behavior: call on the concrete object (or cast when you know the type)
    static_cast<MonsterCard*>(hand[0])->describe();
    static_cast<SpellCard*>(hand[1])->describe();
    static_cast<TrapCard*>(hand[2])->describe();

    for (Card* c : hand)
        delete c;
    return 0;
}
```

> **Constructor order:** Base first \(`Card`\), then derived body\. **Destructor order:** Reverse — `~TrapCard` then `~Card`\.

|Concept|Chinese|Card game example|
|---|---|---|
|**Is\-a**|是一个|`MonsterCard` **is a** `Card`|
|**Member init list**|成员初始化列表|`: Card(id, name, cost), attack_(attack)`|
|**Upcasting**|向上转型|`MonsterCard* m` → `Card* c = m` is safe|
|**Slicing**|对象切片|`Card c = *m;` copies only the `Card` part — use pointers or references|

---

### 0\.3 Access Control — Who Can Touch Card Data?

|Access|Chinese|Who can access?|Card game example|
|---|---|---|---|
|`public`|公有|Everyone|`getName()`, `getCost()`|
|`protected`|保护|This class \+ derived classes|`name_`, `cost_` in `MonsterCard::fight`|
|`private`|私有|Only this class|`TrapCard::faceDown_`|
|`friend`|友元|Declared allies only|`Deck` shuffles internal state \(§0\.5\)|

```C++
class Card {
protected:
    int cost_;   // subclasses may use in their logic
private:
    int secretSerial_;  // ONLY Card — subclasses cannot see this
public:
    int getCost() const { return cost_; }
};
```

**Design rules:**

|Location|Examples|
|---|---|
|`protected` in `Card`|`id_`, `name_`, `cost_` — all subtypes need them|
|`private` in derived|`faceDown_`, `effectId_` — subtype\-only secrets|
|`public` getters|`getName()`, `getCost()` — safe API for UI|

> **Common mistake:** Making all fields `public` so `Deck` can shuffle\. Prefer **`friend`** or methods like `swapAt(i, j)` instead of exposing internals\.

---

### 0\.4 Composition — Deck and Hand *Have* Cards

Not every relationship is inheritance\.

|Relationship|UML|C\+\+|Card game|
|---|---|---|---|
|**Inheritance** \(is\-a\)|Hollow triangle ▷|`: public Card`|`MonsterCard` is a `Card`|
|**Composition** \(strong has\-a\)|Filled diamond ◆|`vector<Card*> cards_`|`Deck` owns the draw pile|
|**Aggregation** \(weak has\-a\)|Hollow diamond ◇|`Card*` borrowed|UI shows a card owned by `Hand`|

```C++
// cards/deck.h (simplified)
class Deck {
public:
    void add(Card* c) { cards_.push_back(c); }

    Card* draw() {
        if (cards_.empty()) return nullptr;
        Card* top = cards_.back();
        cards_.pop_back();
        return top;
    }

private:
    std::vector<Card*> cards_;
};
```

- Use **inheritance** when the specialized type **is a** more general type\.

- Use **composition** when one object **has** another \(`Deck` **has** `Card*`\)\.

---

### 0\.5 Friend Classes — Trusted Allies \(`Deck` and `Hand`\)

Sometimes another class must work closely with private details without opening them to the whole program\.

**Analogy:** `Card` is a house with a **private** storage room\. You do not leave the door open \(`public`\), and **family** \(derived classes\) use `protected`\. You give a **spare key** only to the trusted **deck manager** \(`friend class Deck`\)\.

```C++
class Card {
    friend class Deck;
    friend class Hand;

public:
    Card(int id, const std::string& name, int cost, int ownerId)
        : id_(id), name_(name), cost_(cost), ownerId_(ownerId) {}

    int getCost() const { return cost_; }

private:
    int id_;
    std::string name_;
    int cost_;
    int ownerId_;   // which player owns this card
};

class Hand {
    friend class Deck;  // Deck may read ownerId_ when transferring cards

public:
    explicit Hand(int ownerId) : ownerId_(ownerId) {}

    void addInternal(Card* c) { cards_.push_back(c); }

private:
    int ownerId_;
    std::vector<Card*> cards_;
};

class Deck {
public:
    void transferTopTo(Hand& hand) {
        if (cards_.empty()) return;
        Card* c = cards_.back();
        cards_.pop_back();
        c->ownerId_ = hand.ownerId_;  // OK: Deck is friend of Card and Hand
        hand.addInternal(c);
    }

private:
    std::vector<Card*> cards_;
};
```

|Friend fact|Chinese|Meaning|
|---|---|---|
|**Not a member**|不是成员|`Deck::transferTopTo` is a `Deck` method, not a `Card` method|
|**Not inherited**|不能继承|`MonsterCard` does **not** pass friendship to its friends|
|**Not symmetric**|不对称|`Card` befriending `Deck` does **not** make `Deck` grant `Card` access|
|**Use sparingly**|谨慎使用|Prefer small `friend` surface; a `friend` function is often enough|

```C++
class Card {
    friend void logCardToConsole(const Card& c);
private:
    int id_;
};

void logCardToConsole(const Card& c) {
    std::cout << "Log card id=" << c.id_ << "\n";
}
```

> **When to use ****`friend`****:** `Deck` / `Hand` need efficient zone transfers \(draw, play\) without making `ownerId_` public to all UI code\.

---

### 0\.6 Virtual Base Class — Fixing the Diamond Problem

#### The problem: one monster, two paths to `GameEntity`

Advanced designs mix **roles**:

- `GameEntity` — anything in the match \(`matchId_`, `ownerId_`\)

- `BattleUnit` — can fight \(attack/defense\) — **is a** `GameEntity`

- `ZoneOccupant` — sits on a board zone — **also is a** `GameEntity`

- `MonsterCard` — **both** fights **and** occupies a zone

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NTg0YTMzMDRmODg2MWZiNGNlZWVlZmIxODkwOTlkOTdfNTlkYzQ5ZjUxMTE5MWU2NzI1M2UzMTI5ZTRhODMxNWNfSUQ6NzY0MTgzMjY4MDg1Nzk2MzQ2M18xNzgxMDYwMTg0OjE3ODExNDY1ODRfVjM)

Without care, `MonsterCard` contains **two copies** of `GameEntity` — the **diamond problem** \(菱形继承\):

```Plaintext
GameEntity
       /          \
BattleUnit    ZoneOccupant
       \          /
        MonsterCard
```

```C++
class BattleUnit : public GameEntity { /* ... */ };
class ZoneOccupant : public GameEntity { /* ... */ };
class MonsterCard : public BattleUnit, public ZoneOccupant { };

MonsterCard dragon(/*...*/);
// dragon.ownerId_;   // ERROR: ambiguous — which GameEntity?
```

#### The solution: `virtual public` inheritance

A **virtual base class** \(虚基类\) ensures **only one** shared `GameEntity` inside `MonsterCard`\.

```C++
class GameEntity {
public:
    GameEntity(int matchId, int ownerId)
        : matchId_(matchId), ownerId_(ownerId) {}
protected:
    int matchId_;
    int ownerId_;
};

class BattleUnit : virtual public GameEntity {
public:
    BattleUnit(int matchId, int ownerId, int atk, int def)
        : GameEntity(matchId, ownerId), attack_(atk), defense_(def) {}
protected:
    int attack_, defense_;
};

class ZoneOccupant : virtual public GameEntity {
public:
    ZoneOccupant(int matchId, int ownerId, int zone)
        : GameEntity(matchId, ownerId), zoneIndex_(zone) {}
protected:
    int zoneIndex_;
};

class MonsterCard : public BattleUnit, public ZoneOccupant {
public:
    MonsterCard(int matchId, int ownerId, int atk, int def, int zone)
        : GameEntity(matchId, ownerId)
        , BattleUnit(matchId, ownerId, atk, def)
        , ZoneOccupant(matchId, ownerId, zone) {}
};
```

|Topic|Without `virtual`|With `virtual public`|
|---|---|---|
|`GameEntity` copies in `MonsterCard`|2|**1**|
|`ownerId_` access|Ambiguous|Unambiguous|
|Who constructs `GameEntity`?|Both middle classes try|**Most derived** \(`MonsterCard`\)|

> **Plain English:** Virtual inheritance means only **one** registration desk per monster, even if the monster is both a **fighter** and a **board piece**\.

|Scenario|Use virtual base?|
|---|---|
|Single inheritance `MonsterCard : public Card`|No|
|Multiple inheritance, no shared base|No|
|Diamond: two paths to same base|**Yes**|
|Mixin interfaces sharing one root|Often yes|

> **Note on the word ****`virtual`**** in §0\.6:** Here, `virtual public` means **virtual base class** inheritance \(虚基类\) only\. Do not read it as “virtual member function” — that topic starts in §2\.

---

### 0\.7 What Comes Next

|You learned in §0|Covered later in this chapter|
|---|---|
|`class MonsterCard : public Card`|§1: one interface, many behaviors through `Card*`|
|`protected name_, cost_`|Same fields; shared hooks in the base class|
|`Deck` holds `Card*`|§1–§2: uniform loops without `switch(type)`|
|`friend` for zone management|Stays as\-is — independent of polymorphism|
|`virtual public` for diamond|Stays in §0\.6 — fixes duplicate base subobjects|

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NDBiYTY1YTI5MmY0OGUyMmQ5MjI4ZDA5ZTAxNTUxM2JfOWExMjIwMTBkOWQxMmM2NjBmYTIxM2UxNjAwMDJlMWRfSUQ6NzY0MTgzMjkzODcwMjkzMjkzMl8xNzgxMDYwMTgzOjE3ODExNDY1ODNfVjM)

### Step 4: Practice

#### Try It Yourself 0\.1: Spot Relationships *\(Basic\)*

Label each pair as **is\-a**, **has\-a \(composition\)**, or **has\-a \(aggregation\)**: `MonsterCard`–`Card`, `Deck`–`Card`, `Hand`–`Card`\.

> **Sample answer:** `MonsterCard`–`Card` = is\-a; `Deck`–`Card` = has\-a \(composition if deck owns cards\); `Hand`–`Card` = has\-a\.

#### Try It Yourself 0\.2: Access Design *\(Basic\)*

Should `TrapCard::faceDown_` be `public`, `protected`, or `private`? Should `cost_` be `protected` or `private` with `getCost()`?

> **Sample answer:** `faceDown_` → `private`\. `cost_` → `private` \+ `getCost()` for stricter encapsulation, or `protected` if every subclass manipulates cost directly\.

## 1\. Why Polymorphism Matters in Game Design

### The Problem: Every Object Type Needs Different Behavior

Imagine you are building a 2D game with raylib\. Your world contains:

- **Enemies** that chase the player

- **Coins** that spin and disappear when collected

- **Projectiles** that move in a straight line

- **Chess pieces** that each move according to different rules

Your game loop must update and draw **all** of these every frame:

```C++
// Naive approach: separate lists and duplicated logic
void GameLoop() {
    for (auto& enemy : enemies)    { enemy.move(); enemy.draw(); }  // auto& = reference to each element
    for (auto& coin : coins)        { coin.spin(); coin.draw(); }
    for (auto& bullet : bullets)    { bullet.fly(); bullet.draw(); }
    for (auto& piece : pawns)       { piece.tryMove(); piece.draw(); }
    for (auto& piece : rooks)       { piece.tryMove(); piece.draw(); }
    // ... more piece types ...
}
```





**Problems with this approach:**

1. **Explosion of loops** — every new entity type adds another loop in `GameLoop`\.

2. **No shared interface** — you cannot write `for (auto& obj : allObjects) obj.update()` because each type has differently named methods\.

3. **Collision handling becomes a nightmare** — "what happens when A hits B?" requires type\-checking spaghetti\.

4. **UI screens have the same pain** — Main Menu, Settings, Pause overlay, and Gameplay each need `update()` and `draw()`, but you end up with giant `if (state == MENU) ... else if (state == GAME) ...`\.

> **Opening Question**: How can we treat *different* game objects through *one* common interface, so the game loop stays simple even as we add new types?

### Step 1: Exploring the Problem

> **Exploration Questions**:

- What do enemies, coins, and chess pieces have in common? \(They all update and draw each frame\.\)

- What is different? \(The *details* of update, draw, and collision rules\.\)

- Can inheritance alone solve this? \(Partially — but without `virtual`, the base pointer calls the *base* version, not the derived one\.\)

> **Key distinction:** **Inheritance** shares structure \("is\-a" relationship\)\. **`virtual`** shares *behavior at runtime* through a base pointer\.

Consider inheritance without virtual functions:

```C++
class GameObject {
public:
    void update() { /* generic stub */ }
    void draw()   { /* generic stub */ }
};

class Enemy : public GameObject {
public:
    void update() { /* chase player */ }
    void draw()   { /* draw monster sprite */ }
};

GameObject* obj = new Enemy();
obj->update();  // Calls GameObject::update — NOT Enemy::update! (without virtual)
delete obj;     // Every new needs a matching delete
```

Without polymorphism, the pointer type \(`GameObject*`\) decides which function runs — not the actual object \(`Enemy`\)\. That breaks the game design we want\.

> **Why use a base\-class pointer?** One variable type \(`GameObject*`\) can point to many derived types \(Enemy, Coin, Pawn\)\. That lets you store them in one list and call one loop — the core idea behind polymorphism\.

### Step 2: The Solution — Polymorphism

> **The "Aha" Moment**: Declare common operations in a **base class** as **virtual functions**\. Store **pointers to the base class** pointing at **derived objects**\. At runtime, C\+\+ calls the **correct overridden function** for each object\.

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MmIwOGU1NmI3ZmI0Mzc1ZjkwNTg5NGU2NTIwZGYyZjRfNzQ2NmRiNjhlMWM4MWU3YWM1MTliOWNlMGVjZWZhODlfSUQ6NzY0MTgzMzUxNjg5MjA5NzcxNF8xNzgxMDYwMTgzOjE3ODExNDY1ODNfVjM)

*Figure 2: Comparison of game loop approaches: without polymorphism \(multiple separate loops\) vs with polymorphism \(single unified loop with virtual dispatch\)*

**Real game design benefits:**

|Design need|Without polymorphism|With polymorphism|
|---|---|---|
|Game loop|N separate loops|One loop over `GameObject*`|
|Add new enemy type|Edit game loop, collision code, save system|Subclass \+ push into vector|
|Chess piece rules|Giant `switch(pieceType)`|Each piece class overrides `getLegalMoves()`|
|UI screens|`switch(currentScreen)` everywhere|`Screen*` stack calls `update()` / `draw()`|
|Unit testing|Hard to mock raylib draw calls|Mock `View` interface, test `Model` logic|

---

## 2\. Virtual Functions — Syntax and Behavior

### The Problem: Overridden Functions Are Invisible Through Base Pointers

You already know inheritance lets a `Pawn` *be* a `Piece`\. But when you write:

```C++
Piece* p = new Pawn();
p->move();  // Which move()? Piece::move or Pawn::move?
```

The answer depends on whether `move()` is **virtual**\.

> **Compile time vs runtime:** **Static binding** = the compiler picks the function when you build the program\. **Dynamic binding** = the program picks the function when it runs, based on the *real* object type\.

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MDE3YmMwMmI1ZjMxNjE0ZjViODgyMGUxMjZlZWZiNDFfNWUyNTE1YWQxOTA0NTNiYjM2YzYzOTY4NzY3Y2IwMmJfSUQ6NzY0MTgzMzcwMTEyMjQyNzg1Nl8xNzgxMDYwMTg0OjE3ODExNDY1ODRfVjM)


*Figure 3: Static binding \(compile\-time\) calls the base class function through the pointer type, while dynamic binding \(runtime\) uses the vtable to call the actual object's overridden function*

### Step 1: The Solution — The `virtual` Keyword

#### Minimal Example

```C++
#include <iostream>

class Animal {
public:
    virtual void speak() { std::cout << "...\n"; }
};

class Dog : public Animal {
public:
    void speak() override { std::cout << "Woof!\n"; }
};

int main() {
    Animal* a = new Dog();
    a->speak();   // Output: Woof!  (dynamic binding)
    delete a;
    return 0;
}
```

**How to run:** Save as `animal_demo.cpp`, then compile and run:

```Bash
g++ animal_demo.cpp -o animal_demo
./animal_demo          # Linux / macOS
animal_demo.exe        # Windows
```

Expected output: `Woof!`

> **Compile vs run:** `g++` **compiles** your source into an executable\. Running the executable is **runtime** — that is when `a->speak()` resolves to `Dog::speak`\.

#### Basic Chess Application — Design Evolution \(Version 1\)

> **Note:** The `Piece` class evolves across this chapter\. **Version 1** \(below\) uses `virtual` with a *default* `symbol()`\. In §3 we upgrade to **Version 2** \(pure virtual interface\)\. In §4 we add **Version 3** \(raylib `draw()`\)\.

```C++
// chess/piece.h
#ifndef CHESS_PIECE_H
#define CHESS_PIECE_H

enum PieceColor { WHITE, BLACK };

class Piece {
public:
    Piece(PieceColor color, int row, int col)
        : color_(color), row_(row), col_(col) {}

    virtual ~Piece() = default;

    virtual void moveTo(int row, int col) {
        row_ = row;
        col_ = col;
    }

    virtual char symbol() const { return '?'; }

    PieceColor color() const { return color_; }
    int row() const { return row_; }
    int col() const { return col_; }

protected:
    PieceColor color_;
    int row_, col_;
};

#endif
```

```C++
// chess/pawn.h
#ifndef CHESS_PAWN_H
#define CHESS_PAWN_H

#include "piece.h"

class Pawn : public Piece {
public:
    Pawn(PieceColor color, int row, int col) : Piece(color, row, col) {}

    char symbol() const override { return color_ == WHITE ? 'P' : 'p'; }

    void moveTo(int row, int col) override {
        // Pawn-specific logic could go here (en passant, promotion check)
        Piece::moveTo(row, col);
    }
};

#endif
```

```C++
// demo_virtual.cpp
#include <iostream>
#include "chess/piece.h"
#include "chess/pawn.h"

int main() {
    Piece* pieces[2];
    pieces[0] = new Pawn(WHITE, 1, 0);
    pieces[1] = new Pawn(BLACK, 6, 0);

    for (int i = 0; i < 2; ++i)
        std::cout << pieces[i]->symbol() << ' ';  // P p

    for (int i = 0; i < 2; ++i)
        delete pieces[i];

    return 0;
}
```

### Key Rules for Virtual Functions

|Rule|Explanation|
|---|---|
|Use `virtual` in the **base** class|Derived overrides inherit virtuality automatically\.|
|Prefer `override` in derived classes|Compiler error if you misspell or mismatch signature\.|
|Always give polymorphic base classes a **virtual destructor**|`delete basePtr` must destroy the full derived object\.|
|Virtual call has small runtime cost|One indirection through vtable — negligible for games\.|
|Constructors are **not** virtual|Construction runs base → derived; no dynamic binding during ctor\.|
|Call through pointer or reference|Value slicing \(`Piece p = Pawn(...)`\) loses polymorphism\.|

#### Object Slicing — Shown in Code

```C++
Pawn pawn(WHITE, 1, 0);

// WRONG — slices off Pawn data; polymorphism lost
Piece p = pawn;
std::cout << p.symbol();        // '?' (base default), not 'P'

// CORRECT — pointer keeps full Pawn object
Piece* ptr = new Pawn(WHITE, 1, 0);
std::cout << ptr->symbol();     // 'P'
delete ptr;
```

### Virtual Destructor — Critical for Games

```C++
// WRONG — base destructor not virtual
class BaseBad {
public:
    ~BaseBad() { /* only BaseBad cleanup */ }
};
class DerivedBad : public BaseBad {
    int* data_;
public:
    DerivedBad() : data_(new int[100]) {}
    ~DerivedBad() { delete[] data_; }  // may NOT run when deleted via BaseBad*
};

BaseBad* b = new DerivedBad();
delete b;  // Undefined behavior / leak — only ~BaseBad runs

// CORRECT — virtual destructor
class BaseGood {
public:
    virtual ~BaseGood() = default;
};
class DerivedGood : public BaseGood {
    int* data_;
public:
    DerivedGood() : data_(new int[100]) {}
    ~DerivedGood() { delete[] data_; }  // runs correctly
};

BaseGood* g = new DerivedGood();
delete g;  // ~DerivedGood then ~BaseGood
```

> **Rule of thumb:** If you ever `delete` through a base pointer, give the base a `virtual ~Base() = default;`\.

```C++
class Piece {
public:
    virtual ~Piece() = default;  // REQUIRED when deleting via Piece*
};

// Safe:
Piece* p = new Rook(BLACK, 0, 0);
delete p;  // Calls ~Rook then ~Piece
```

### Module\-Ready Pattern: Uniform Piece Container

```C++
// chess/board.h (fragment — draw() added in §4 Version 3)
#include <vector>
#include "piece.h"

class Board {
public:
    void addPiece(Piece* piece) { pieces_.push_back(piece); }

    void drawAll(/* raylib context */) const {
        for (Piece* p : pieces_)
            p->draw();  // Requires virtual draw() on Piece (see §4)
    }

private:
    std::vector<Piece*> pieces_;
};
```

---

## 3\. Pure Virtual Functions and Abstract Classes

### The Problem: The Base Class Should Not Be Instantiated

`Piece` is a **concept** — there is no "generic piece" on a real chessboard\. Every piece on the board is *specifically* a pawn, rook, knight, etc\.

If `Piece::symbol()` returns `'?'`, that is a placeholder, not real behavior\. We want to **force** every subclass to implement `symbol()` and `legalMoves()`\.

### Step 1: The Solution — Pure Virtual Functions \(`= 0`\)

A **pure virtual function** has no implementation in the base class\. Writing `= 0` after the declaration means *"no default implementation"* — it is **not** assigning the number zero\.

> **Common compiler errors:**

- `cannot declare variable 'Piece p' to be of abstract type 'Piece'` — you tried to create an abstract class\.

- `'void Derived::foo()' marked 'override', but does not override` — function signature does not match the base \(check `const`, parameters\)\.

A class with at least one pure virtual function is an **abstract class** — you **cannot** create objects of that type\.

#### Syntax Reference

```C++
class AbstractBase {
public:
    // Pure virtual — no body, or = 0 in declaration
    virtual ReturnType functionName(ParamList) = 0;

    // Can still have concrete functions
    void helperFunction() { /* shared code */ }

    // Virtual destructor still required
    virtual ~AbstractBase() = default;
};

// ERROR: AbstractBase obj;  // Cannot instantiate abstract class

class Concrete : public AbstractBase {
public:
    ReturnType functionName(ParamList) override {
        // MUST implement every pure virtual function
    }
};
```

#### Comparison Table

|Feature|Ordinary virtual|Pure virtual \(`= 0`\)|
|---|---|---|
|Base class implementation|Optional|None \(or empty stub not allowed as pure\)|
|Derived class|May override|**Must** override|
|Instantiate base class|Allowed|**Forbidden**|
|Purpose|Provide default \+ allow override|Define **interface** / contract|

#### Abstract Piece — Design Evolution \(Version 2\)

> **Upgrade from Version 1:** `symbol()` and `legalMoves()` are now **pure virtual** \(`= 0`\)\. The base `Piece` can no longer be instantiated — only `Pawn`, `Rook`, etc\. can\.

```C++
// chess/piece.h — abstract base (Version 2)
#ifndef CHESS_PIECE_H
#define CHESS_PIECE_H

#include <vector>

enum PieceColor { WHITE, BLACK };
const int BOARD_SIZE = 8;

struct Square { int row, col; };

class Piece {
public:
    Piece(PieceColor color, int row, int col)
        : color_(color), row_(row), col_(col) {}

    virtual ~Piece() = default;

    // Pure virtual — every piece MUST implement
    virtual char symbol() const = 0;
    virtual std::vector<Square> legalMoves(const char board[BOARD_SIZE][BOARD_SIZE]) const = 0;

    // Concrete — shared by all pieces
    void moveTo(int row, int col) {
        row_ = row;
        col_ = col;
    }

    PieceColor color() const { return color_; }
    int row() const { return row_; }
    int col() const { return col_; }

protected:
    PieceColor color_;
    int row_, col_;
};

#endif
```

```C++
// chess/rook.h
#ifndef CHESS_ROOK_H
#define CHESS_ROOK_H

#include "piece.h"

class Rook : public Piece {
public:
    Rook(PieceColor color, int row, int col) : Piece(color, row, col) {}

    char symbol() const override {
        return color_ == WHITE ? 'R' : 'r';
    }

    std::vector<Square> legalMoves(const char board[BOARD_SIZE][BOARD_SIZE]) const override {
        std::vector<Square> moves;
        // Simplified: horizontal and vertical rays (detailed in full example below)
        const int dr[] = {-1, 1, 0, 0};
        const int dc[] = {0, 0, -1, 1};
        for (int d = 0; d < 4; ++d) {
            for (int step = 1; step < BOARD_SIZE; ++step) {
                int nr = row_ + dr[d] * step;
                int nc = col_ + dc[d] * step;
                if (nr < 0 || nr >= BOARD_SIZE || nc < 0 || nc >= BOARD_SIZE) break;
                if (board[nr][nc] != '.') {
                    // lowercase letter on board = black piece; uppercase = white piece
                    if ((board[nr][nc] >= 'a') != (color_ == WHITE)) moves.push_back({nr, nc});
                    break;
                }
                moves.push_back({nr, nc});
            }
        }
        return moves;
    }
};

#endif
```

### When to Use Abstract Classes in Game Design

|Use abstract class when…|Example|
|---|---|
|Base type is incomplete conceptually|`Piece`, `Screen`, `GameState`|
|You need a **contract** all subclasses fulfill|`draw()`, `update()`, `handleInput()`|
|You store heterogeneous objects in one container|`std::vector<Piece*>`|
|You want compile\-time enforcement|Forgetting `legalMoves()` → compile error|

---

## Quick Reference Card

```C++
// Abstract interface
class Base {
public:
    virtual ~Base() = default;
    virtual void doWork() = 0;           // pure virtual — must override
    virtual void optionalHook() {}        // virtual with default
};

// Concrete type
class Derived : public Base {
public:
    void doWork() override { /* ... */ }
};

// Polymorphic usage
Base* obj = new Derived();
obj->doWork();   // Derived::doWork
delete obj;      // ~Derived then ~Base (virtual destructor)
```

**Remember:** Polymorphism is not magic — it is a disciplined way to keep your game loop and UI manager **stable** while your content \(pieces, enemies, screens\) **grows**\.

---

## 4\. Example 1 — International Chess with raylib \(Detailed\)

This example shows a **modular chess project** using polymorphism: each piece type knows how to draw itself and compute legal moves\. The **board** and **game loop** treat all pieces uniformly through `Piece*`\.

> **Build in phases:** Start with the console demo below \(no raylib\), then add raylib drawing in Phase 2, then mouse input in Phase 3\.

### Phase 0 — Console Demo \(No raylib, \~25 lines\)

Run this **before** the full project to verify polymorphism works:

```C++
// console_polymorphism.cpp — single file, no raylib
#include <iostream>
#include <vector>

struct Square { int row, col; };

class Piece {
public:
    virtual ~Piece() = default;
    virtual char symbol() const = 0;
    virtual void printMoves() const = 0;
};

class Pawn : public Piece {
public:
    char symbol() const override { return 'P'; }
    void printMoves() const override { std::cout << "Pawn: forward 1\n"; }
};

class Rook : public Piece {
public:
    char symbol() const override { return 'R'; }
    void printMoves() const override { std::cout << "Rook: straight lines\n"; }
};

int main() {
    std::vector<Piece*> pieces = { new Pawn(), new Rook() };
    for (Piece* p : pieces) {
        std::cout << p->symbol() << ": ";
        p->printMoves();   // polymorphic — each piece prints its own rules
    }
    for (Piece* p : pieces) delete p;
    return 0;
}
```

```Bash
g++ console_polymorphism.cpp -o console_demo && ./console_demo
# Expected: P: Pawn: forward 1   R: Rook: straight lines
```

### Design Evolution \(Version 3\) — Full raylib Project

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YzRjMWJhNjI0NjQ5YjFjZDUxY2ZiNWM5NTEzMDI5NDhfYzNjMjE0ZDQwMjMxMmE1MjQ5YjA4OThkOGEzYTVjNTdfSUQ6NzY0MTgzMzgzMzQ2NTcyODIxMF8xNzgxMDYwMTgzOjE3ODExNDY1ODNfVjM)


*Figure 4: UML class diagram showing the abstract Piece base class with pure virtual methods, concrete piece types \(Pawn, Rook, Knight\), and the Board class holding a polymorphic collection*

### Project Layout

```Plaintext
chess_raylib/
├── main.cpp
├── chess/
│   ├── piece.h          # Abstract Piece (Version 3 — adds draw())
│   ├── pawn.h / pawn.cpp
│   ├── rook.h / rook.cpp
│   └── board.h / board.cpp
└── assets/
    └── (optional piece textures)
```

> **Header files \(****`.h`****\):** Declarations and `#ifndef` **include guards** prevent double\-inclusion\.
**Source files \(****`.cpp`****\):** Implementations\. The compiler links all `.cpp` files into one executable\.

### Build Order

1. Create folders: `chess_raylib/` and `chess_raylib/chess/`

2. Write `chess/piece.h` \(abstract interface \+ default `draw()`\)

3. Write `chess/pawn.h`, `pawn.cpp`, `rook.h`, `rook.cpp`

4. Write `chess/board.h`, `board.cpp`

5. Write `main.cpp`

6. Compile \(see Build Hint at end of §4\)

### 4\.1 Abstract Piece Interface \(Version 3\)

```C++
// chess/piece.h
#ifndef CHESS_PIECE_H
#define CHESS_PIECE_H

#include "raylib.h"
#include <vector>

enum PieceColor { WHITE, BLACK };
const int BOARD_SIZE = 8;
const int CELL_SIZE  = 64;

struct Square { int row, col; };

class Piece {
public:
    Piece(PieceColor color, int row, int col)
        : color_(color), row_(row), col_(col) {}

    virtual ~Piece() = default;

    virtual char symbol() const = 0;
    virtual std::vector<Square> legalMoves(const char board[BOARD_SIZE][BOARD_SIZE]) const = 0;

    virtual void draw(int boardOffsetX, int boardOffsetY) const {
        // Default: draw letter on square (override for sprites later)
        int x = boardOffsetX + col_ * CELL_SIZE + CELL_SIZE / 4;
        int y = boardOffsetY + row_ * CELL_SIZE + CELL_SIZE / 4;
        Color c = (color_ == WHITE) ? RAYWHITE : DARKGRAY;
        DrawText(TextFormat("%c", symbol()), x, y, 40, c);
    }

    void moveTo(int row, int col) { row_ = row; col_ = col; }

    PieceColor color() const { return color_; }
    int row() const { return row_; }
    int col() const { return col_; }

protected:
    PieceColor color_;
    int row_, col_;
};

#endif
```

### 4\.2 Pawn Implementation

```C++
// chess/pawn.h
#ifndef CHESS_PAWN_H
#define CHESS_PAWN_H

#include "piece.h"

class Pawn : public Piece {
public:
    Pawn(PieceColor color, int row, int col);

    char symbol() const override;
    std::vector<Square> legalMoves(const char board[BOARD_SIZE][BOARD_SIZE]) const override;
};

#endif
```

```C++
// chess/pawn.cpp
#include "pawn.h"

Pawn::Pawn(PieceColor color, int row, int col) : Piece(color, row, col) {}

char Pawn::symbol() const {
    return color_ == WHITE ? 'P' : 'p';
}

std::vector<Square> Pawn::legalMoves(const char board[BOARD_SIZE][BOARD_SIZE]) const {
    std::vector<Square> moves;
    int dir = (color_ == WHITE) ? -1 : 1;
    int startRow = (color_ == WHITE) ? 6 : 1;

    int oneStep = row_ + dir;
    if (oneStep >= 0 && oneStep < BOARD_SIZE && board[oneStep][col_] == '.')
        moves.push_back({oneStep, col_});

    if (row_ == startRow) {
        int twoStep = row_ + 2 * dir;
        if (board[oneStep][col_] == '.' && board[twoStep][col_] == '.')
            moves.push_back({twoStep, col_});
    }

    for (int dc : {-1, 1}) {
        int nr = row_ + dir;
        int nc = col_ + dc;
        if (nr >= 0 && nr < BOARD_SIZE && nc >= 0 && nc < BOARD_SIZE) {
            char target = board[nr][nc];
            if (target != '.' && ((target >= 'a') != (color_ == WHITE)))  // lowercase = black
                moves.push_back({nr, nc});
        }
    }
    return moves;
}
```

### 4\.3 Rook Implementation

```C++
// chess/rook.h
#ifndef CHESS_ROOK_H
#define CHESS_ROOK_H

#include "piece.h"

class Rook : public Piece {
public:
    Rook(PieceColor color, int row, int col);

    char symbol() const override;
    std::vector<Square> legalMoves(const char board[BOARD_SIZE][BOARD_SIZE]) const override;
};

#endif
```

```C++
// chess/rook.cpp
#include "rook.h"

Rook::Rook(PieceColor color, int row, int col) : Piece(color, row, col) {}

char Rook::symbol() const {
    return color_ == WHITE ? 'R' : 'r';
}

static void addRayMoves(std::vector<Square>& moves,
                        const char board[BOARD_SIZE][BOARD_SIZE],
                        int row, int col, PieceColor color,
                        int dr, int dc) {
    for (int step = 1; step < BOARD_SIZE; ++step) {
        int nr = row + dr * step;
        int nc = col + dc * step;
        if (nr < 0 || nr >= BOARD_SIZE || nc < 0 || nc >= BOARD_SIZE) break;
        char target = board[nr][nc];
        if (target == '.') {
            moves.push_back({nr, nc});
        } else {
            if ((target >= 'a') != (color == WHITE))  // capture enemy piece only
                moves.push_back({nr, nc});
            break;
        }
    }
}

std::vector<Square> Rook::legalMoves(const char board[BOARD_SIZE][BOARD_SIZE]) const {
    std::vector<Square> moves;
    addRayMoves(moves, board, row_, col_, color_, -1, 0);
    addRayMoves(moves, board, row_, col_, color_,  1, 0);
    addRayMoves(moves, board, row_, col_, color_,  0,-1);
    addRayMoves(moves, board, row_, col_, color_,  0, 1);
    return moves;
}
```

### 4\.4 Board — Polymorphic Container

```C++
// chess/board.h
#ifndef CHESS_BOARD_H
#define CHESS_BOARD_H

#include "piece.h"
#include <vector>

class Board {
public:
    Board();
    ~Board();

    void setupStartingPosition();
    void syncBoardArray();
    void draw(int offsetX, int offsetY) const;
    Piece* pieceAt(int row, int col) const;
    bool movePiece(Piece* piece, int toRow, int toCol);
    std::vector<Square> legalMovesFor(Piece* piece) const;

    const char (*boardArray() const)[BOARD_SIZE] { return board_; }

private:
    char board_[BOARD_SIZE][BOARD_SIZE];
    std::vector<Piece*> pieces_;

    void clearPieces();
    void placePiece(Piece* piece);
};

#endif
```

```C++
// chess/board.cpp
#include "board.h"
#include "pawn.h"
#include "rook.h"
#include <algorithm>  // for std::remove

Board::Board() {
    for (int r = 0; r < BOARD_SIZE; ++r)
        for (int c = 0; c < BOARD_SIZE; ++c)
            board_[r][c] = '.';
}

Board::~Board() { clearPieces(); }

void Board::clearPieces() {
    for (Piece* p : pieces_) delete p;
    pieces_.clear();
}

void Board::placePiece(Piece* piece) {
    pieces_.push_back(piece);
    board_[piece->row()][piece->col()] = piece->symbol();
}

void Board::setupStartingPosition() {
    clearPieces();
    for (int c = 0; c < BOARD_SIZE; ++c) {
        placePiece(new Pawn(WHITE, 6, c));
        placePiece(new Pawn(BLACK, 1, c));
    }
    placePiece(new Rook(WHITE, 7, 0));
    placePiece(new Rook(WHITE, 7, 7));
    placePiece(new Rook(BLACK, 0, 0));
    placePiece(new Rook(BLACK, 0, 7));
    syncBoardArray();
}

void Board::syncBoardArray() {
    for (int r = 0; r < BOARD_SIZE; ++r)
        for (int c = 0; c < BOARD_SIZE; ++c)
            board_[r][c] = '.';
    for (Piece* p : pieces_)
        board_[p->row()][p->col()] = p->symbol();
}

Piece* Board::pieceAt(int row, int col) const {
    for (Piece* p : pieces_)
        if (p->row() == row && p->col() == col) return p;
    return nullptr;
}

std::vector<Square> Board::legalMovesFor(Piece* piece) const {
    if (!piece) return {};
    return piece->legalMoves(board_);  // Polymorphic call — Pawn vs Rook
}

bool Board::movePiece(Piece* piece, int toRow, int toCol) {
    auto moves = legalMovesFor(piece);
    for (const Square& sq : moves) {
        if (sq.row == toRow && sq.col == toCol) {
            Piece* captured = pieceAt(toRow, toCol);
            if (captured) {
                pieces_.erase(std::remove(pieces_.begin(), pieces_.end(), captured),
                              pieces_.end());
                delete captured;
            }
            piece->moveTo(toRow, toCol);
            syncBoardArray();
            return true;
        }
    }
    return false;
}

void Board::draw(int offsetX, int offsetY) const {
    for (int r = 0; r < BOARD_SIZE; ++r) {
        for (int c = 0; c < BOARD_SIZE; ++c) {
            Color cellColor = ((r + c) % 2 == 0) ? BEIGE : BROWN;
            DrawRectangle(offsetX + c * CELL_SIZE, offsetY + r * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE, cellColor);
        }
    }
    for (Piece* p : pieces_)
        p->draw(offsetX, offsetY);  // Polymorphic draw
}
```

### 4\.5 Game Loop — main\.cpp

```C++
// main.cpp
#include "raylib.h"
#include "chess/board.h"
#include <vector>

int main() {
    const int screenW = BOARD_SIZE * CELL_SIZE + 100;
    const int screenH = BOARD_SIZE * CELL_SIZE + 100;
    const int offsetX = 50;
    const int offsetY = 50;

    InitWindow(screenW, screenH, "Chess — Polymorphism Demo");
    SetTargetFPS(60);

    Board board;
    board.setupStartingPosition();

    Piece* selected = nullptr;
    std::vector<Square> highlights;

    while (!WindowShouldClose()) {
        // Input: click to select / move
        if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
            Vector2 mouse = GetMousePosition();
            int col = (mouse.x - offsetX) / CELL_SIZE;
            int row = (mouse.y - offsetY) / CELL_SIZE;

            if (row >= 0 && row < BOARD_SIZE && col >= 0 && col < BOARD_SIZE) {
                Piece* clicked = board.pieceAt(row, col);
                if (selected == nullptr && clicked != nullptr) {
                    selected = clicked;
                    highlights = board.legalMovesFor(selected);
                } else if (selected != nullptr) {
                    if (board.movePiece(selected, row, col)) {
                        selected = nullptr;
                        highlights.clear();
                    } else if (clicked == selected) {
                        selected = nullptr;
                        highlights.clear();
                    } else if (clicked != nullptr) {
                        selected = clicked;
                        highlights = board.legalMovesFor(selected);
                    }
                }
            }
        }

        BeginDrawing();
        ClearBackground(RAYWHITE);

        board.draw(offsetX, offsetY);

        // Highlight legal moves
        for (const Square& sq : highlights) {
            DrawCircle(offsetX + sq.col * CELL_SIZE + CELL_SIZE / 2,
                       offsetY + sq.row * CELL_SIZE + CELL_SIZE / 2,
                       10, Fade(GREEN, 0.5f));
        }

        DrawText("Click piece, then destination. Polymorphic legalMoves().",
                 10, 10, 16, DARKGRAY);

        EndDrawing();
    }

    CloseWindow();
    return 0;
}
```

### Why This Design Works

1. **Adding Bishop or Knight** — create new `.h/.cpp`, push into `pieces_`; no changes to `Board::draw` or the game loop\.

2. **`legalMovesFor`** — one line delegates to the correct piece logic via virtual dispatch\.

3. **Testing without raylib** — compile `pawn.cpp` \+ `rook.cpp` with a console test harness; `draw()` is the only raylib\-dependent function\.

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YjFhNzVkOTBjYWEwZjEwY2FlYTQ5YzA3ZjJhYWJkYTVfNTBlNzJhZDMwYzAyOTI2NWI3NDc0ZTQ0ZGZlOTYyMjVfSUQ6NzY0MTgzNDIzMDk1NTI0ODgzOF8xNzgxMDYwMTg0OjE3ODExNDY1ODRfVjM)

### 

## 5\. Example 2 — Multi\-Layer UI Design with Polymorphism

Games rarely have a single screen\. You typically stack **layers**: Main Menu → Settings → Back to Menu, or Gameplay with a **Pause overlay** on top\. Polymorphism lets each screen implement the same interface while the **UI manager** holds a stack of `Screen*`\.

### The Problem: Giant `switch` on Screen State

```C++
enum AppState { MENU, SETTINGS, PLAYING, PAUSE };

void update(AppState state) {
    if (state == MENU)      { /* 50 lines */ }
    else if (state == SETTINGS) { /* 40 lines */ }
    else if (state == PLAYING)  { /* 100 lines */ }
    else if (state == PAUSE)    { /* 30 lines */ }
}
```

Every new screen inflates this function\. Transitions \(fade, push/pop\) become entangled with screen logic\.

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NjE4OTg3NzZlMTA0MTY5YTFlZWY0Y2NiN2I2MzM0MzhfYWU4MTg1ZWE4MzFiN2Y3NmZmMmE5ZDUwOWQzMTMzOWVfSUQ6NzY0MTgzMzk2OTQ4Njg1OTQ2OV8xNzgxMDYwMTgzOjE3ODExNDY1ODNfVjM)


*Figure 5: UI screen stack visualization showing MenuScreen at bottom, GameplayScreen in middle, and PauseScreen as semi\-transparent overlay on top\. Push adds a screen; pop removes the top screen\.*

### The Solution: Abstract `Screen` Class \+ Stack

> **Ownership rule:** Whoever calls `new` must call `delete`\. Here, `ScreenManager` **owns** all screens — it `delete`s them in its destructor and when popping the stack\.

> **Syntax sidebar \(used in §5 code\):**

- `(void)dt;` — silences "unused parameter" warnings when a screen does not need delta time yet\.

- `mutable bool pop_` — allows changing `pop_` inside a `const` method \(`requestPop() const`\)\.

- `explicit ScreenManager(Screen* initial)` — prevents accidental implicit conversion from `Screen*` to `ScreenManager`\.

```C++
// ui/screen.h
#ifndef UI_SCREEN_H
#define UI_SCREEN_H

#include "raylib.h"

class Screen {
public:
    virtual ~Screen() = default;

    // Pure virtual — every screen MUST implement
    virtual void update(float dt) = 0;
    virtual void draw() const = 0;

    // Optional hooks with default behavior
    virtual void onEnter() {}
    virtual void onExit()  {}

    // Return true to pop this screen (e.g. Back button)
    virtual bool requestPop() const { return false; }

    // Return non-null to push a new screen (transfer ownership to manager)
    virtual Screen* requestPush() { return nullptr; }
};

#endif
```

```C++
// ui/settings_screen.h — minimal stub so MenuScreen compiles
#ifndef UI_SETTINGS_SCREEN_H
#define UI_SETTINGS_SCREEN_H

#include "screen.h"

class SettingsScreen : public Screen {
public:
    void update(float dt) override { (void)dt; }
    void draw() const override {
        DrawText("SETTINGS (stub)", 300, 280, 32, DARKGRAY);
        DrawText("Press Esc to go back (implement requestPop)", 220, 330, 18, GRAY);
    }
    bool requestPop() const override { return IsKeyPressed(KEY_ESCAPE); }
};

#endif
```

```C++
// ui/menu_screen.h
#ifndef UI_MENU_SCREEN_H
#define UI_MENU_SCREEN_H

#include "screen.h"

class MenuScreen : public Screen {
public:
    void update(float dt) override;
    void draw() const override;
    Screen* requestPush() override;

private:
    int selectedIndex_ = 0;
    bool startRequested_ = false;
};

#endif
```

```C++
// ui/menu_screen.cpp
#include "menu_screen.h"
#include "gameplay_screen.h"
#include "settings_screen.h"

void MenuScreen::update(float dt) {
    (void)dt;
    if (IsKeyPressed(KEY_DOWN)) selectedIndex_ = (selectedIndex_ + 1) % 3;
    if (IsKeyPressed(KEY_UP))   selectedIndex_ = (selectedIndex_ + 2) % 3;
    if (IsKeyPressed(KEY_ENTER)) {
        if (selectedIndex_ == 0) startRequested_ = true;
        if (selectedIndex_ == 1) { /* push settings handled via requestPush */ }
    }
}

void MenuScreen::draw() const {
    const char* items[] = {"Start Game", "Settings", "Quit"};
    DrawText("MAIN MENU", 300, 150, 40, DARKBLUE);
    for (int i = 0; i < 3; ++i) {
        Color c = (i == selectedIndex_) ? RED : GRAY;
        DrawText(items[i], 320, 250 + i * 50, 24, c);
    }
}

Screen* MenuScreen::requestPush() {
    if (selectedIndex_ == 0 && startRequested_) {
        startRequested_ = false;
        return new GameplayScreen();
    }
    if (selectedIndex_ == 1 && IsKeyPressed(KEY_ENTER))
        return new SettingsScreen();
    return nullptr;
}
```

```C++
// ui/gameplay_screen.h
#ifndef UI_GAMEPLAY_SCREEN_H
#define UI_GAMEPLAY_SCREEN_H

#include "screen.h"
#include "../chess/board.h"

class GameplayScreen : public Screen {
public:
    GameplayScreen();
    ~GameplayScreen() override = default;

    void update(float dt) override;
    void draw() const override;
    Screen* requestPush() override;

private:
    Board board_;
    bool pauseRequested_ = false;
};

#endif
```

```C++
// ui/gameplay_screen.cpp
#include "gameplay_screen.h"
#include "pause_screen.h"

GameplayScreen::GameplayScreen() {
    board_.setupStartingPosition();
}

void GameplayScreen::update(float dt) {
    (void)dt;
    if (IsKeyPressed(KEY_ESCAPE))
        pauseRequested_ = true;
    // ... chess input ...
}

void GameplayScreen::draw() const {
    DrawText("GAMEPLAY (Esc = Pause)", 10, 10, 20, DARKGRAY);
    board_.draw(50, 80);
}

Screen* GameplayScreen::requestPush() {
    if (pauseRequested_) {
        pauseRequested_ = false;
        return new PauseScreen();  // Overlay on stack
    }
    return nullptr;
}
```

```C++
// ui/pause_screen.h — semi-transparent overlay
#ifndef UI_PAUSE_SCREEN_H
#define UI_PAUSE_SCREEN_H

#include "screen.h"

class PauseScreen : public Screen {
public:
    void update(float dt) override;
    void draw() const override;
    bool requestPop() const override;

private:
    mutable bool pop_ = false;
};

#endif
```

```C++
// ui/pause_screen.cpp
#include "pause_screen.h"

void PauseScreen::update(float dt) {
    (void)dt;
    if (IsKeyPressed(KEY_ESCAPE) || IsKeyPressed(KEY_ENTER))
        pop_ = true;
}

void PauseScreen::draw() const {
    DrawRectangle(0, 0, GetScreenWidth(), GetScreenHeight(),
                  Fade(BLACK, 0.6f));
    DrawText("PAUSED", 350, 280, 40, RAYWHITE);
    DrawText("Esc or Enter to resume", 300, 340, 20, LIGHTGRAY);
}

bool PauseScreen::requestPop() const {
    return pop_;
}
```

### Screen Manager — Polymorphic Stack

```C++
// ui/screen_manager.h
#ifndef UI_SCREEN_MANAGER_H
#define UI_SCREEN_MANAGER_H

#include "screen.h"
#include <vector>

class ScreenManager {
public:
    explicit ScreenManager(Screen* initial);
    ~ScreenManager();

    void update(float dt);
    void draw() const;

private:
    std::vector<Screen*> stack_;

    void processRequests();
};

#endif
```

```C++
// ui/screen_manager.cpp
#include "screen_manager.h"

ScreenManager::ScreenManager(Screen* initial) {
    stack_.push_back(initial);
    stack_.back()->onEnter();
}

ScreenManager::~ScreenManager() {
    for (Screen* s : stack_) delete s;
}

void ScreenManager::update(float dt) {
    if (stack_.empty()) return;
    stack_.back()->update(dt);
    processRequests();
}

void ScreenManager::draw() const {
    // Draw all layers bottom-to-top (menu under pause overlay)
    for (Screen* s : stack_)
        s->draw();
}

void ScreenManager::processRequests() {
    if (stack_.empty()) return;

    Screen* top = stack_.back();

    if (Screen* pushed = top->requestPush()) {
        stack_.push_back(pushed);
        pushed->onEnter();
    }

    if (top->requestPop()) {
        top->onExit();
        delete stack_.back();
        stack_.pop_back();
        if (!stack_.empty())
            stack_.back()->onEnter();
    }
}
```

### UI Main Entry

```C++
// ui_main.cpp
#include "raylib.h"
#include "ui/screen_manager.h"
#include "ui/menu_screen.h"

int main() {
    InitWindow(800, 600, "Multi-Layer UI — Polymorphism");
    SetTargetFPS(60);

    ScreenManager manager(new MenuScreen());

    while (!WindowShouldClose()) {
        float dt = GetFrameTime();
        manager.update(dt);

        BeginDrawing();
        ClearBackground(RAYWHITE);
        manager.draw();
        EndDrawing();
    }

    CloseWindow();
    return 0;
}
```

### Layer Stack Visualization

```Plaintext
Stack bottom → top:

[ MenuScreen ]                    ← only menu visible
[ MenuScreen, GameplayScreen ]    ← game replaces or covers menu
[ MenuScreen, GameplayScreen, PauseScreen ]  ← pause draws on top (semi-transparent)

draw():  Menu.draw(); Gameplay.draw(); Pause.draw();
update(): only top->update()  (or update all if you need background simulation)
```

|Design choice|Recommendation|
|---|---|
|Who receives input?|Usually **top screen only** \(`stack_.back()->update`\)|
|Who gets drawn?|**All screens** in stack for overlay effect, or only top for full\-screen swap|
|Ownership|Manager **owns** screens; `new` on push, `delete` on pop|
|Adding Help screen|Subclass `Screen`, no change to `ScreenManager`|

> **Checkpoint — After §5 you should be able to:**

- Describe how a screen stack replaces a giant `switch` on game state\.

- Explain why `update()` runs on the top screen only, but `draw()` may run on all layers\.

---

## 6\. Chapter Summary

### Key Concepts Review

- **Inheritance \(§0\)** — `Card` base, `MonsterCard` / `SpellCard` / `TrapCard` derived; `friend` for `Deck`/`Hand`; `virtual public` for diamond inheritance when roles share `GameEntity`\.

- **Polymorphism** lets one interface \(`Piece*`, `Screen*`, `Card*`\) refer to many concrete types\.

- **`virtual`** enables **dynamic binding** — the runtime type selects the function\.

- **Pure virtual \(****`= 0`****\)** defines a **contract**; the base class becomes **abstract**\.

- **Virtual destructor** is mandatory when deleting polymorphic objects through base pointers\.

- **Game loop simplification** — one update/draw loop over a heterogeneous collection\.

- **UI stack** — push/pop `Screen*` instead of monolithic state machines\.

### Card Game Application Summary \(§0\)

|Element|Inheritance design|
|---|---|
|`Card`|Base class: `id_`, `name_`, `cost_`|
|`MonsterCard`, `SpellCard`, `TrapCard`|Derived types with specialized fields and methods|
|`Deck`, `Hand`|Composition \(`has-a`\); may use `friend` for zone transfers|
|`BattleUnit` \+ `ZoneOccupant` → `MonsterCard`|Virtual base `GameEntity` when diamond inheritance appears|

### Chess Application Summary

|Element|Polymorphic design|
|---|---|
|`Piece`|Abstract base with `symbol()`, `legalMoves()`, `draw()`|
|`Pawn`, `Rook`, …|Concrete pieces override pure virtuals|
|`Board`|Holds `vector<Piece*>`, calls virtual methods uniformly|
|Game loop|Select piece, call `legalMovesFor` — no `switch` on piece type|

### Common Mistakes

|Mistake|Why wrong|Correct way|
|---|---|---|
|Forgetting `virtual` on base method|Always calls base version|Mark overriding chain with `virtual` \+ `override`|
|Missing virtual destructor|Leaks / undefined behavior on `delete basePtr`|`virtual ~Base() = default;`|
|`Piece p = Pawn(...);` \(by value\)|Object slicing — not polymorphic|Use `Piece*` or `Piece&`|
|Instantiating abstract class|Compiler error \(good\!\)|Instantiate concrete subclasses only|
|Pure virtual not implemented|Derived class stays abstract|Implement every `= 0` function in concrete class|
|Giant `switch` instead of virtual|Open for modification every new type|Add subclass, override virtual functions|

### Final Challenge

Extend the chess raylib demo:

1. Add `Knight` with polymorphic `legalMoves()`\.

2. Add a `PromotionScreen : public Screen` that appears when a pawn reaches the last rank — push it onto the UI stack, then return the chosen piece type as a new `Piece*`\.

3. Refactor `Board` to use `std::vector<std::unique_ptr<Piece>>` and explain why the virtual destructor still matters\.

