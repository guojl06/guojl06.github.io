# Week7 All about family！

# **Chapter: Inheritance and UML / 继承与UML**



\> **Building upon family trees: How classes inherit traits like children inherit genes**

\> **基于家族树的概念：类如何像孩子继承基因一样继承特性**



**\-\-\-**



## **0\. Difficult Points Review / 难点复习**



### **🔥 Deep Analysis of Class Member Variable Initialization**



**Static, Const, and Static Const Member Variables**



#### **📊 Comparison Table of Three Special Member Types**





|Member Type|Belongs To|Initialization Timing|Initialization Location|In\-Class Direct Init?|Key Characteristics|
|---|---|---|---|---|---|
|`static`|Class itself \(shared\)|When defined outside class|Outside class \(\.cpp file\)|C\+\+17❌ C\+\+17✅\(constexpr\)|All objects share one copy|
|`const`|Each object separately|Constructor initializer list|Initializer list|C\+\+11❌ C\+\+11✅|Cannot modify after creation|
|`static const`|Class itself \(shared\)|Inside or outside class|Inside class \(C\+\+11\) / Outside|Integral✅ Non\-integral pre\-C\+\+17❌|Shared \+ Immutable|





**\-\-\-**



#### **1️⃣ Static Member Variables**



**Core Concept**: Static members belong to the **class itself**, not to individual objects\. All objects share **the same single copy** of the data\.



**Analogy**: Just like a family sharing one home address—all family members \(objects\) point to the same location\.



```C++
// ========== Declaration (Header .h) ==========
class ChessPlayer {
private:
    static int totalPlayers;  // Declaration only, not definition
    string name;
public:
    ChessPlayer(string n) : name(n) {
        totalPlayers++;  // Increment count for each new player
    }
    static int getTotal() { return totalPlayers; }
};

// ========== Definition (Implementation .cpp) ==========
// ⚠️ MUST define outside the class! Most easily forgotten part!
int ChessPlayer::totalPlayers = 0;  // Definition and initialization
```



**⚠️ Common Mistakes Warning:**



```C++
// ❌ Error 1: Forgetting to define outside the class
// If you only declare but don't define, linker error: undefined reference

// ❌ Error 2: Repeating 'static' in the out-of-class definition
int ChessPlayer::static totalPlayers = 0;  // Wrong! No static keyword needed

// ❌ Error 3: Initializing static variable in constructor
ChessPlayer(string n) : name(n) {
    totalPlayers = 0;  // Wrong! Resets to zero every construction—defeats counting
}

// ✅ Correct: Initialize only once outside the class
int ChessPlayer::totalPlayers = 0;  // Initialized once at program startup
```



**\-\-\-**



#### **2️⃣ Const Member Variables**



**Core Concept**: \`const\` members belong to **each individual object**\. Each object has its own constant value that **cannot be modified** after creation\.



**Analogy**: Like a person's ID number—one per person, never changes throughout life\.



```C++
class ChessPiece {
private:
    const string pieceID;      // Each piece has a unique ID
    const bool isWhite;       // Color cannot change once determined
    int positionX, positionY;
    
public:
    // ✅ MUST initialize const members in the initializer list!
    ChessPiece(string id, bool white, int x, int y) 
        : pieceID(id)          // const members MUST be initialized here
        , isWhite(white)       // Cannot assign inside function body!
        , positionX(x)
        , positionY(y)
    {
        // ❌ Cannot assign inside constructor body
        // pieceID = id;  // Compile error: const member cannot be modified
    }
};
```



**⚠️ Key Rules:**





|Scenario|Allowed?|Explanation|
|---|---|---|
|Initializer list assignment|✅ Required|`Constructor() : constVar(value)`|
|Constructor body assignment|❌ Forbidden|Compile error: const cannot be modified|
|C\+\+11 in\-class direct init|✅ Allowed|`const int maxMoves = 100;`|





```C++
// C++11 onwards: can initialize directly in class (basic types only)
class ChessBoard {
    const int boardSize = 8;        // ✅ Supported since C++11
    const string name = "Chess";    // ❌ Strings still need initializer list
public:
    ChessBoard() : name("Chess") {} // Correct approach
};
```



**\-\-\-**



#### **3️⃣ Static Const Member Variables**



**Core Concept**: Combines the characteristics of static \(shared\) and const \(immutable\)—a **true class\-level constant**\.



**Analogy**: The rules of chess—all games follow the same unchanging set of rules\.



```C++
class ChessGame {
private:
    // ✅ C++11 onwards: integral types can initialize directly in class
    static const int BOARD_SIZE = 8;        // Integral: in-class init
    static const int MAX_PLAYERS = 2;      // Integral: in-class init
    
    // ⚠️ Non-integral: must initialize outside class before C++17
    static const string GAME_NAME;          // Declaration
    
public:
    void printBoard() {
        // Use static constant
        for(int i = 0; i < BOARD_SIZE; i++) {
            // ...
        }
    }
};

// Non-integral static const MUST be defined outside class (pre-C++17)
const string ChessGame::GAME_NAME = "International Chess";
```



**🎯 C\+\+ Standard Evolution:**



```C++
class Example {
    // C++98/03: Only integral static const could initialize in class, must be constant expression
    static const int MAX = 100;              // ✅ Supported since ancient standard
    
    // C++11: Added constexpr, stricter but more powerful
    static constexpr int MIN = 1;            // ✅ C++11
    
    // C++17: Inline variable revolution! All types can initialize in class
    static const inline string NAME = "Test";  // ✅ C++17
    static inline double PI = 3.14159;          // ✅ C++17
};
```



**\-\-\-**



#### **📋 Complete Comparison Code Example**



```C++
#include <iostream>
#include <string>
using namespace std;

// ==================== Complete Demonstration ====================
class ChessMaster {
private:
    // ========== static: Class Shared ==========
    static int totalMasters;           // Declaration (all masters share count)
    
    // ========== const: Object Constant ==========
    const string masterID;              // Each master has unique ID (immutable)
    const int rating;                   // Rating score (immutable)
    
    // ========== static const: Class-Level Constant ==========
    static const int MAX_RATING = 3000; // ✅ Integral: in-class init (C++11)
    static const string TITLE;          // Non-integral: outside init (pre-C++17)
    
public:
    // Constructor: const members MUST be initialized in initializer list!
    ChessMaster(string id, int r) 
        : masterID(id)      // ✅ const member: initializer list
        , rating(r)         // ✅ const member: initializer list
    {
        totalMasters++;     // ✅ static member: modified in function body
        // masterID = id;   // ❌ Error! const cannot be assigned in body
    }
    
    void display() const {
        cout << "ID: " << masterID 
             << ", Rating: " << rating 
             << "/" << MAX_RATING
             << ", Total: " << totalMasters << endl;
    }
    
    static int getTotal() { return totalMasters; }
};

// ========== Outside-Class Definitions (Easiest Part to Forget!) ==========
int ChessMaster::totalMasters = 0;           // static definition + init
const string ChessMaster::TITLE = "GM";      // static const non-integral definition

// ==================== Usage Test ====================
int main() {
    cout << "Max Rating: " << ChessMaster::MAX_RATING << endl;  // No object needed
    
    ChessMaster m1("GM001", 2800);
    ChessMaster m2("GM002", 2750);
    
    m1.display();  // ID: GM001, Rating: 2800/3000, Total: 2
    m2.display();  // ID: GM002, Rating: 2750/3000, Total: 2
    
    // m1.rating = 2900;  // ❌ Compile error! const cannot be modified
    
    return 0;
}
```



**\-\-\-**



#### **🎯 Memory Mnemonic**



```Plain Text
【Static Members】
Don't forget to define outside the class, all objects share one copy
Never initialize in constructor, declaration and definition must separate

【Const Members】
Initializer list is their home, cannot assign in function body
One per object independent value, fixed forever after creation

【Static Const】
Integral types C++11 in-class fine, non-integral pre-C++17 outside define
Shared + read-only is the nature, class-level constants most reliable
```



**\-\-\-**



## **1\. Learning Objectives / 学习目标**



By the end of this chapter, you will:



- Draw UML class diagrams showing inheritance

- Implement `class Derived : public Base` inheritance in C\+\+

- Understand `protected` access and when to use it

- Predict constructor/destructor calling order

- Refactor duplicated code using inheritance

**\-\-\-**



## **2\. UML Class Diagrams: Blueprints for Code / UML类图：代码的蓝图**



### **1\.1 What is UML? / 什么是UML？**



**Analogy: The Architect's Blueprint**



Before building a house, architects create blueprints showing rooms, walls, and electrical wiring\. They don't start pouring concrete immediately\!



Similarly, **UML \(Unified Modeling Language\)** is a visual blueprint for software\. It lets us design classes and their relationships **before writing code**\.



\> **Analogy**: UML is to code what blueprints are to buildings / UML之于代码，正如蓝图之于建筑



**Key Benefits:**



1\. **Visual communication** \- Show class structures without code details

2\. **Design before coding** \- Plan the architecture first

3\. **Documentation** \- Understand existing code quickly



UML Blueprint Analogy

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Mjc2ZmM0YmU3MjE3MzZjZTQ1OThiNTUyOTdjMjFkNzJfNTQ0M2U0ZTM1ODQ2NDg1ZTIxNjExOWE1YmRhNjU2NGRfSUQ6NzYyNjIzODIyNzE0MTU2MTUyOV8xNzgxMDYwMzc4OjE3ODExNDY3NzhfVjM)

*Figure 1: UML diagrams are to code what blueprints are to buildings \- they provide a visual plan before implementation*



**\-\-\-**



### **1\.2 Class Representation in UML / UML中的类表示**



A UML class is drawn as a rectangle with three compartments:



```Plain Text
┌─────────────────────────────┐
│       ClassName             │  ← Name (italic = abstract class)
├─────────────────────────────┤
│ - id: int                   │  ← Attributes
│ - name: string              │     - = private, # = protected, + = public
│ # email: string             │
├─────────────────────────────┤
│ + getName(): string         │  ← Methods/Operations
│ # print(): void             │
│ - calculate(): double       │
└─────────────────────────────┘
```



**Symbol Key / 符号对照表:**





|Symbol|Access Level|中文|Usage|
|---|---|---|---|
|`+`|`public`|公有|Everyone can access|
|`-`|`private`|私有|Only this class|
|`#`|`protected`|保护|This class \+ derived classes|





UML Class Structure

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Y2NkNGYyZDUyYjUyZDk2YWNmNDMxOTRkMGM4NDJiYTRfMmYwMGZjODRhYjFiMDQxY2Q2NjVlYzY5MTdiMTFjOGZfSUQ6NzYyNjIzODMwMTE3MDkxMjIwMV8xNzgxMDYwMzc4OjE3ODExNDY3NzhfVjM)

*Figure 2: UML class box structure with three sections \(name, attributes, methods\) and access modifiers legend*



**\-\-\-**



### **1\.3 Types of Relationships / 关系类型**



**Analogy: Different Types of Relationships in a Family**



Just like families have different relationship types \(parent\-child, marriage, roommates\), classes have different relationship types too\.



#### **1\.3\.1 Inheritance: "Is\-A" / 继承："是一个"**



**Analogy: Genetic Inheritance**



\- A child **is a** human \(inherits human traits\)

\- A student **is a** person \(inherits person attributes\)

\- A dog **is an** animal \(inherits animal characteristics\)



```Plain Text
classDiagram
    class Person {
        #id: int
        #name: string
        +getName(): string
        +print(): void
    }
    
    class Student {
        -gpa: double
        -major: string
        +print(): void
    }
    
    Person <|-- Student
```







**UML Notation**: Hollow triangle arrow pointing to parent



- C\+\+: `class Student : public Person`

**Think about it**: What common attributes would all Person objects have? What would only Students have?



**\-\-\-**



#### **1\.3\.2 Composition: "Has\-A" \(Strong\) / 组合："有一个"（强）**



**Analogy: A Human Has\-A Heart**



\- A human **has a** heart

- The heart cannot exist independently

- If the human dies, the heart dies too

```Plain Text
classDiagram
    class Human {
        -heart: Heart
        +live(): void
    }
    
    class Heart {
        -rate: int
        +beat(): void
    }
    
    Human *-- Heart
```







**UML Notation**: Filled diamond



- C\+\+: `class Human { Heart heart; };` \(member object\)

**Think about it**: Can you think of other "strong ownership" relationships? \(Car\-Engine, House\-Room\)



UML Relationships Comparison

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Y2QyYjE0YTRkOTNiNjI2NjA4Y2M2MDJmZGVhMTlkNTFfYmI2NThiMGJhYzNiZDkyZjg3MjI3YTdlNTM4MzgyYzNfSUQ6NzYyNjIzODM1MDE0MzYwNTY5OF8xNzgxMDYwMzc4OjE3ODExNDY3NzhfVjM)

*Figure 3: Three fundamental UML relationships \- Inheritance \(is\-a\), Composition \(has\-a strong\), and Aggregation \(has\-a weak\)*



**\-\-\-**



#### **1\.3\.3 Aggregation: "Has\-A" \(Weak\) / 聚合："有一个"（弱）**



**Analogy: A University Has Students**



\- A university **has** students

- But students exist independently

- If the university closes, students still exist

```Plain Text
classDiagram
    class University {
        -students: Student[]
        +enroll(s: Student): void
    }
    
    class Student {
        -name: string
    }
    
    University o-- Student
```







**UML Notation**: Hollow diamond



- C\+\+: `class University { Student* students[]; };` \(pointers\)

**Key Difference**: Composition = owned \(dies together\), Aggregation = referenced \(lives independently\)



**\-\-\-**



### **1\.4 Interactive Exercise: Draw the Diagram / 互动练习：画图**



**Scenario**: Design a university system with Department, Professor, and Course\.



**Relationships to identify:**



1. What is the "is\-a" relationship? \(inheritance\)

2. What "has\-a" relationships exist? \(composition/aggregation\)

```Plain Text
classDiagram
    class Department {
        -name: string
        -faculty: Professor[]
        +addProfessor(): void
        +printRoster(): void
    }
    
    class Professor {
        -courses: string[]
        +addCourse(): void
    }
```







**Your Task**: 



- Identify what Professor inherits from \(if anything\)

- Add the inheritance arrow

- Determine if Department\-Professor is composition or aggregation

- Draw the complete diagram

Click to see the answer / 点击查看答案



```Plain Text
classDiagram
    class Person {
        #id: int
        #name: string
        +getName(): string
        +print(): void
    }
    
    class Professor {
        -courses: string[]
        -courseCount: int
        +addCourse(): void
        +getCourseCount(): int
    }
    
    class Department {
        -name: string
        -faculty: Professor[]
        +addProfessor(): void
        +printRoster(): void
    }
    
    Person <|-- Professor
    Department o-- Professor
```







**Explanation**: Professor is\-a Person \(inheritance\)\. Department has Professors \(aggregation \- professors exist outside the department\)\.



**\-\-\-**



## **3\. Inheritance in C\+\+/ C\+\+中的继承**



### **2\.1 The Problem: Code Duplication / 问题：代码重复**



**Scenario**: Building a university management system



Without inheritance, we write:



```C++
class Student {
private:
    int id;          // Duplicated!
    string name;     // Duplicated!
    string email;    // Duplicated!
    double gpa;      // Student-specific
public:
    void print() {    // Similar logic
        cout << "Student: " << name << endl;
    }
};

class Professor {
private:
    int id;          // Duplicated again!
    string name;     // Duplicated again!
    string email;    // Duplicated again!
    string dept;     // Professor-specific
public:
    void print() {    // Similar logic
        cout << "Professor: " << name << endl;
    }
};
```



**Problems:**



- ❌ `id`, `name`, `email` repeated in every class

- ❌ Change `print()` format → edit all classes

- ❌ No way to store Students and Professors together

**Think about it**: What if we need to add "phone number" to all people? How many places must we edit?



**\-\-\-**



### **2\.2 The Solution: Extract Common Code / 解决方案：提取公共代码**



**Analogy: Family Genes**



All family members share common traits \(eye color, height\)\. Each person then develops unique skills\.



```C++
// Base class = common "genes"
class Person {
protected:  // ← Key: accessible to children (derived classes)
    int id;
    string name;
    string email;
    
public:
    Person(int id, const string& name, const string& email)
        : id(id), name(name), email(email) {}
    
    void printBasic() const {
        cout << "[" << id << "] " << name << endl;
    }
};

// Derived class = inherits + specializes
class Student : public Person {  // "Student is-a Person"
private:
    double gpa;      // Student-specific only
    string major;
    
public:
    Student(int id, const string& name, const string& email,
            double gpa, const string& major)
        : Person(id, name, email)  // ← Call parent's constructor!
        , gpa(gpa), major(major) {}
    
    void print() const {
        printBasic();  // ← Reuse parent's method!
        cout << "  Major: " << major << ", GPA: " << gpa << endl;
    }
};
```



**Key Syntax Elements:**





|Syntax|Meaning|Why It Matters|
|---|---|---|
|`class Student : public Person`|Inheritance declaration|`public` = "is\-a" relationship|
|`protected:`|Access specifier|Like `private`, but children can access|
|`Person(id, name, email)`|Base constructor call|Must initialize parent first\!|





Code Duplication vs Inheritance

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OGNlMjBiZTFiYzYzZDBlYzE0M2U2MTI5YTBlNmRlNjRfNWUwYzA3MGFmMDlkNDU5Y2E5NDQ2ODViMWY0NjlkM2NfSUQ6NzYyNjIzODQ1Mjk4NzgwODk0Nl8xNzgxMDYwMzc4OjE3ODExNDY3NzhfVjM)

*Figure 4: Comparison of code duplication \(left\) versus inheritance solution \(right\) \- inheritance extracts common attributes into a base class*



**\-\-\-**



### **2\.3 The Three Access Levels in Inheritance / 继承中的三种访问级别**



**Analogy: Family Secrets**



- `private` = Your diary \(only you read it\)

- `protected` = Family recipe \(family members know it\)

- `public` = Public announcement \(everyone knows\)

```C++
class Parent {
private:
    int secretDiary;        // Only Parent can access
protected:
    int familyRecipe;       // Parent + Children can access
public:
    int publicAnnouncement; // Everyone can access
};

class Child : public Parent {
public:
    void tryAccess() {
        // secretDiary = 1;     // ❌ ERROR: private
        familyRecipe = 2;       // ✓ OK: protected
        publicAnnouncement = 3; // ✓ OK: public
    }
};
```



**\*\*Why use \`protected\`?\*\***



```C++
class Person {
protected:
    int id;      // Derived classes need to access this
    string name;
public:
    // Getters are public
    int getId() const { return id; }
};

class Student : public Person {
public:
    void print() const {
        // Can access id directly (it's protected)
        cout << "Student #" << id << ": " << getName() << endl;
    }
};
```



Access Control Levels

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MjVhYWMzMjU4ZTI3NmJjMTdmNDMwMjA2MzFlMjVlMzJfODNlYTAzZWYyOWM3OGIxN2Q3MGNmNWQzMTdlMWVhMDRfSUQ6NzYyNjIzODUyODIwODgwMDcwNV8xNzgxMDYwMzc4OjE3ODExNDY3NzhfVjM)

*Figure 5: Access control levels using family metaphor \- public \(broadcast to everyone\), protected \(family dinner table\), private \(locked diary\)*



**Think about it**: Should \`id\` be \`private\` or \`protected\`? What if no derived class needs to modify it directly?



**\-\-\-**



### **2\.3B The "Friend" Exception / "友元"例外**



\> **Breaking Encapsulation for Trusted Allies**

\> **为信任盟友打破封装**



#### **What is a Friend? / 什么是友元？**



**Analogy: The Spare Key to Your Home / 你家的备用钥匙**



Imagine you have:



\- **Private bedroom** \(private members\): Only you can enter

\- **Protected living room** \(protected members\): Family can enter

\- **Public yard** \(public members\): Anyone can enter



Now imagine your **best friend** or **trusted neighbor**:



- They're not family \(not inheritance\)

\- But you give them a **spare key** to your home

\- They can enter your **private bedroom** when needed



In C\+\+, a `friend` is like giving a spare key \- granting special access to private/protected members\.



**\-\-\-**



#### **Friend Function: External Function with Private Access / 友元函数：可访问私有的外部函数**



```C++
class BankAccount {
private:
    double balance;      // Private - only the account can modify
    string password;     // Private - sensitive data
    
public:
    BankAccount(double initial) : balance(initial) {}
    
    // Regular public interface
    double getBalance() const { return balance; }
    
    // Declare external function as FRIEND
    // 声明外部函数为友元
    friend bool transferFunds(BankAccount& from, BankAccount& to, double amount);
    friend class BankManager;  // Entire class is a friend!
};

// External function - but can access private members!
// 外部函数 - 但可以访问私有成员！
bool transferFunds(BankAccount& from, BankAccount& to, double amount) {
    // This function is NOT a member of BankAccount
    // 这个函数不是BankAccount的成员
    // But it can access PRIVATE members!
    // 但它可以访问私有成员！
    
    if (from.balance >= amount) {  // ✓ Accessing private 'balance'!
        from.balance -= amount;
        to.balance += amount;      // ✓ Accessing private 'balance'!
        return true;
    }
    return false;
}
```



**Why Use Friend? / 为什么使用友元？**



1\. **Collaboration between classes**: Two classes need to work closely together

**类之间的紧密协作**：两个类需要密切合作

2\. **Efficiency**: Avoiding getter/setter overhead in performance\-critical code

**效率**：在性能关键代码中避免getter/setter开销



**\-\-\-**



#### **Friend Class: Entire Class Gets Access / 友元类：整个类获得访问权限**



```C++
class BankManager;  // Forward declaration

class BankAccount {
private:
    double balance;
    int accountNumber;
    
public:
    BankAccount(int num, double initial) 
        : accountNumber(num), balance(initial) {}
    
    // Grant ALL members of BankManager access to ALL private members
    // 授予BankManager所有成员访问所有私有成员的权限
    friend class BankManager;
};

class BankManager {
public:
    // Can access private data of BankAccount directly!
    // 可以直接访问BankAccount的私有数据！
    void auditAccount(const BankAccount& account) {
        cout << "Account #" << account.accountNumber << endl;  // ✓ Private!
        cout << "Balance: $" << account.balance << endl;       // ✓ Private!
    }
    
    void freezeAccount(BankAccount& account) {
        // Direct modification of private data!
        account.balance = 0;  // ✓ Can modify private!
        cout << "Account frozen!" << endl;
    }
};
```



**\-\-\-**



#### **Key Characteristics of Friend / 友元的关键特性**





|Feature|Description|Analogy|
|---|---|---|

\| **Not a member**         \| Friend functions are NOT class members                \| Friend has a spare key, not a bedroom         \|

\| **Not symmetric**        \| If A is B's friend, B is NOT automatically A's friend \| You gave them a key, they didn't give you one \|

\| **Not inherited**        \| Derived classes don't inherit friendship              \| Children don't inherit parent's friends       \|

\| **Declared in class**    \| Friend declaration goes inside the class              \| You decide who gets a key                     \|

\| **Accesses all private** \| Friends can access ALL private/protected members      \| Spare key opens all doors                     \|





Friend Concept

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OGRjNjdlZDY1NmQ5NTZiOTA2NjU1MWNjNDBkZmE1ODhfNDEyNmMyMjc4ZTk3YzUxYWY0YmYxYzNmYTA5N2JiYTZfSUQ6NzYyNjIzODU4NDIxNTA2MzUxMl8xNzgxMDYwMzc4OjE3ODExNDY3NzhfVjM)

*Figure 5B: The friend concept \- friends have "spare keys" to access private members, different from family \(protected\) or public access*



**\-\-\-**



#### **Analogy: Comparing Access Levels / 访问级别类比对比**





|Access|Relationship|Analogy|
|---|---|---|
|`public`|Anyone|Public park|
|`protected`|Family \(inheritance\)|Family living room|
|`private`|Self only|Your bedroom|
|`friend`|Trusted ally|Friend with spare key|





**Think about it**: 



- When should you use `friend` instead of making something `public`?

- Why not just make everything `public` if friends can access private anyway?

\> **Best Practice**: Use \`friend\` sparingly\. It breaks encapsulation, so only use it when:

> 
> 
> 1. Two classes are logically tightly coupled \(like Department\-Professor\)
> 
> 2. You need external operators \(like `<<`, `>>`, `+`\)
> 
> 3. Performance is critical and getters/setters add overhead
> 
> 



**\-\-\-**



### **2\.4 Constructor Order: Building a Family / 构造顺序：建造家族**



**Analogy: Building a House**



When building a custom home:



1\. **Foundation** \(Base class\) must be poured first

2\. **Framing** \(Members\) comes next

3\. **Finishing touches** \(Derived class\) comes last



When demolishing:



1\. **Finishing touches** removed first

2\. **Framing** removed next

3\. **Foundation** removed last \(reverse order\!\)



```C++
class Person {
public:
    Person() { cout << "1. Person constructor (Foundation)" << endl; }
    ~Person() { cout << "4. Person destructor (Last)" << endl; }
};

class Student : public Person {
    int studentId;
public:
    Student() : Person() {  // Explicit base call
        cout << "2. Student constructor (Finishing)" << endl;
    }
    ~Student() {
        cout << "3. Student destructor (First)" << endl;
    }
};

// Usage:
Student s;
// Output:
// 1. Person constructor (Foundation)
// 2. Student constructor (Finishing)
// 3. Student destructor (First)
// 4. Person destructor (Last)
```



**The Golden Rule:**





|Phase|Order|Memory Analogy|
|---|---|---|
|Construction|Base → Members → Derived|Build foundation first|
|Destruction|Derived → Members → Base|Remove roof before foundation|





Constructor and Destructor Order

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YTFiNzA3ZDk3NDc5MGFkM2Q3NjZiZTViOTZlNWMyODJfYzc1ODIxMWRhNDZlOGM0Yzk4NmRmYWY1NmUxZTAxNWZfSUQ6NzYyNjIzODY0NjQxMjU2MTYwMl8xNzgxMDYwMzc4OjE3ODExNDY3NzhfVjM)

*Figure 6: Constructor and destructor execution order in inheritance \- construction goes base\-to\-derived, destruction goes derived\-to\-base \(reverse order\)*



**\-\-\-**



### **2\.5 Inheritance from newClass / newClass中的继承实例**



Let's examine the actual university system code:



**Person\.h \- The Base Class:**



```C++
class Person {
protected:  // ← Children can access
    int id;
    string name;
    
public:
    Person(int id, const string& name);
    ~Person() = default;
    
    int getId() const { return id; }
    string getName() const { return name; }
    void print() const;
};
```



**Student\.h \- Inherits from Person:**



```C++
#include "Person.h"

class Student : public Person {  // "Student is-a Person"
private:
    double gpa;
    string major;
    static int totalStudents;
    
public:
    Student();
    Student(int id, const string& name, double gpa, const string& major);
    ~Student();
    
    // Student-specific methods
    double getGpa() const { return gpa; }
    string getMajor() const { return major; }
    void updateGpa(double newGpa);
    void print() const;  // Specialized version
    
    static int getTotalStudents();
};
```



**Key observations:**



1. `Student` inherits `id`, `name` from `Person`

2. `Student` adds `gpa`, `major` \(its unique traits\)

3. `Student` constructor must call `Person` constructor

**Professor\.h \- Also Inherits from Person:**



```C++
#include "Person.h"

class Professor : public Person {  // "Professor is-a Person"
private:
    string courses[50];
    int courseCount;
    
public:
    Professor();
    Professor(int id, const string& name);
    
    // Professor-specific methods
    void addCourse(const string& courseCode);
    int getCourseCount() const { return courseCount; }
    void print() const;  // Specialized version
};
```



**\-\-\-**



### **2\.6 Implementation Details / 实现细节**



**Student\.cpp \- Constructor Chaining:**



```C++
#include "Student.h"

int Student::totalStudents = 0;

// Default constructor
Student::Student() 
    : Person(0, "Unknown")  // ← Must call base constructor
    , gpa(0.0)
    , major("Undeclared") 
{
    totalStudents++;
}

// Parameterized constructor
Student::Student(int id, const string& name, 
                 double gpa, const string& major)
    : Person(id, name)    // ← Initialize base first!
    , gpa(gpa)
    , major(major)
{
    totalStudents++;
}

// Destructor
Student::~Student() {
    totalStudents--;
}
```



**Think about it**: Why can't we write \`id = id;\` in the Student constructor body? Why must we use the initialization list?



Answer / 答案



`id` is `protected` in Person, but it's still a member of Person, not Student\. By the time the Student constructor body runs, the Person part must already be constructed\. We use the initialization list to tell C\+\+: "Build the Person part first with these arguments\."



**\-\-\-**



## **4\. Inheritance Types / 继承类型**



### **3\.1 Public Inheritance \(Most Common\) / 公有继承（最常用）**



```C++
class Student : public Person { };
```



**Access level preservation:**





|Base|Becomes in Derived|Usage|
|---|---|---|
|`public`|`public`|"is\-a" relationship|
|`protected`|`protected`|Derived classes need access|
|`private`|`private` \(inaccessible\)|Hidden implementation|





**Think about it**: Should a Student be able to do everything a Person can do? That's "is\-a"\!



**\-\-\-**



### **3\.2 Protected Inheritance \(Rare\) / 保护继承（罕见）**



```C++
class SecretStudent : protected Person { };
```



**Effect**: All \`public\` members become \`protected\`



Use case: When you want to reuse implementation, but not expose the interface\.



**\-\-\-**



### **3\.3 Private Inheritance \(Implementation Detail\) / 私有继承（实现细节）**



```C++
class Car : private Engine { };  // "implemented-in-terms-of"
```



**Effect**: All members become \`private\`



**Analogy**: A car has an engine, but you can't "be" an engine\. The engine is a private implementation detail\.



\> **Best Practice**: Prefer composition \(\`class Car \{ Engine e; \};\`\) over private inheritance\. It's clearer and more flexible\.



**\-\-\-**



**\#\#\#\# Detailed Example: Rectangle inherits from Point \(Private Inheritance\)**



This example demonstrates how `Rectangle` privately inherits from `Point` to reuse the coordinate functionality while exposing only its own interface\.



**Point\.h** \- Base class defining a 2D point:

```C++
#ifndef _POINT_H
#define _POINT_H

class Point {  // Base class Point definition
public:  // Public function members
    void initPoint(float x = 0, float y = 0) { 
        this->x = x; 
        this->y = y;
    }
    void move(float offX, float offY) { 
        x += offX; 
        y += offY; 
    }
    float getX() const { return x; }
    float getY() const { return y; }
private:  // Private data members
    float x, y;
};

#endif // _POINT_H
```



**Rectangle\.h** \- Derived class using private inheritance:

```C++
#ifndef _RECTANGLE_H
#define _RECTANGLE_H
#include "Point.h"

class Rectangle : private Point {  // Derived class definition
public:  // New public function members
    void initRectangle(float x, float y, float w, float h) {
        initPoint(x, y);  // Call base class public member function
        this->w = w;
        this->h = h;
    }
    void move(float offX, float offY) { 
        Point::move(offX, offY);  // Explicitly call base class move
    }
    float getX() const { return Point::getX(); }  // Expose via wrapper
    float getY() const { return Point::getY(); }  // Expose via wrapper
    float getH() const { return h; }
    float getW() const { return w; }
private:  // New private data members
    float w, h;  // Width and height
};

#endif // _RECTANGLE_H
```



**Main\.cpp** \- Using the Rectangle class:

```C++
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    Rectangle rect;  // Create a Rectangle object
    rect.initRectangle(2, 3, 20, 10);  // Set rectangle position and size
    rect.move(3, 2);  // Move rectangle position
    
    cout << "The data of rect(x, y, w, h): " << endl;
    cout << rect.getX() << ", "    // Access via wrapper methods
         << rect.getY() << ", "
         << rect.getW() << ", "
         << rect.getH() << endl;
    return 0;
}
```



**Output:**

```Plain Text
The data of rect(x, y, w, h):
5, 5, 20, 10
```



**Key Observations:**



|Aspect|Behavior|
|---|---|
|`Point` members in `Rectangle`|All become `private` \(including `public` ones\)|
|`initPoint()`|Can be called inside `Rectangle` methods, but not from outside|
|`getX()`, `getY()`|Must create wrapper methods to expose them|
|External code|Cannot directly access any `Point` functionality|



**Why Private Inheritance Here?**



\- \`Rectangle\` **is implemented in terms of** \`Point\` \(uses coordinates internally\)

\- But \`Rectangle\` is **not** a \`Point\` conceptually \(no "is\-a" relationship\)

- The coordinate interface should be hidden from `Rectangle` users

- `Rectangle` selectively exposes only what it needs through wrapper methods

**\-\-\-**



### **3\.4 Virtual Base Class \(Advanced\)**



#### **The Diamond Problem**



**Analogy: Family Genealogy Confusion**



Imagine a child who has:



- A grandmother \(Person\)

- Mother inherits from grandmother

- Father inherits from grandmother  

- Child inherits from both mother and father

The child ends up with **TWO copies** of the grandmother's genes\! This is biologically impossible and confusing\.



Diamond Problem

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Zjc4NzhhODNiMWZmNmMyN2E5ZWZiMmNiYWJhYjdhZjVfOTM0NjA0YjljMjgwYjllZTNhYjdmMzdlMDZjY2NjZmVfSUQ6NzYyNjIzODcwMjIwNDk0NzQyMV8xNzgxMDYwMzc4OjE3ODExNDY3NzhfVjM)

*Figure 7: The Diamond Problem \- TeachingAssistant inherits from both Student and Professor, each containing a copy of Person, causing ambiguity*



**In C\+\+ Code Structure:**



```Plain Text
Person
       /      \
      /        \
   Student   Professor
      \      /
       \    /
      TeachingAssistant
```



A `TeachingAssistant` is both a `Student` and a `Professor`, but there's only ONE real person\!



**UML Class Diagram \- Virtual Base Class Solution:**



Virtual Base Class UML Diagram

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NTRiY2VmYjM4Mzg1ZDAwZmYxMmMwNjY1YjJlNjRkZmRfMmY0NTBhZGU4MDkwNmZmZTgxYTk3NmI3YjE4MzdlNGVfSUQ6NzYyNjIzODkwMTMzMzY0MjE5MV8xNzgxMDYwMzc4OjE3ODExNDY3NzhfVjM)

*Figure X: UML diagram showing the Diamond Problem solution using virtual inheritance \- Person is declared as virtual base class, ensuring TeachingAssistant inherits only one copy of Person's attributes*



|Class|Inheritance|Virtual?|Own Attributes|
|---|---|---|---|
|Person|\(base class\)|—|name, id|
|Student|public Person|✓ virtual|gpa|
|Professor|public Person|✓ virtual|department|
|TeachingAssistant|public Student, public Professor|—|\(none, uses virtual base\)|



**Key UML Notations:**

- «virtual» stereotype: Marks virtual inheritance relationship

- Hollow triangle arrow: Standard UML inheritance symbol

- `-` \(minus\): Private/protected attributes

- `+` \(plus\): Public methods

**The Problem in Code:**



```C++
class Person {
public:
    string name;
    Person(const string& n) : name(n) {}
};

class Student : public Person {  // ← Inherits Person
public:
    double gpa;
    Student(const string& n, double g) : Person(n), gpa(g) {}
};

class Professor : public Person {  // ← Also inherits Person!
public:
    string department;
    Professor(const string& n, const string& d) : Person(n), department(d) {}
};

// Teaching Assistant is both Student AND Professor
class TA : public Student, public Professor {
public:
    TA(const string& n, double g, const string& d)
        : Student(n, g), Professor(n, d)  // ⚠️ PROBLEM: Person constructed TWICE!
    {}
};

// What happens here?
TA ta("Alice", 3.8, "CS");
// ta.name = ???  // ERROR: ambiguous! Which name? Student's or Professor's?
```



**The Ambiguity Problem:**



```C++
cout << ta.name;  // ❌ ERROR: 'name' is ambiguous
// Compiler: "Do you mean Student::name or Professor::name?"
// But they're the SAME person! This makes no sense!
```



**Memory Layout Without Virtual Base / 无虚基类的内存布局：**



```Plain Text
TA Object in Memory:
┌───────────────────────────────┐
│  Student::Person part         │ ← name (copy 1)
│  ├─ name: "Alice"            │
│  └─ ...                      │
├───────────────────────────────┤
│  Student-specific part        │
│  └─ gpa: 3.8                 │
├───────────────────────────────┤
│  Professor::Person part       │ ← name (copy 2) - DUPLICATE!
│  ├─ name: "Alice"            │     ← WASTED SPACE + CONFUSION
│  └─ ...                      │
├───────────────────────────────┤
│  Professor-specific part      │
│  └─ department: "CS"         │
└───────────────────────────────┘
```



\> **Think about it**: Should a TA have two names? Two IDs? No\! A person is a person, regardless of their multiple roles\.



Virtual Base Memory Layout

*Figure 8: Memory layout comparison \- without virtual inheritance \(left\) creates duplicate Person subobjects causing ambiguity; with virtual inheritance \(right\) creates a single shared Person subobject*



**\-\-\-**



#### **The Solution: Virtual Base Class**



**Analogy: Shared Family Heritage**



Instead of each parent carrying their own copy of grandma's photo, they share **ONE** copy that the grandchild inherits directly\.



**\*\*Syntax: Add \`virtual\` to Inheritance\*\***



```C++
class Person {
public:
    string name;
    int id;
    Person(const string& n, int i) : name(n), id(i) {}
};

// Use VIRTUAL inheritance
class Student : virtual public Person {  // ← virtual!
public:
    double gpa;
    Student(const string& n, int i, double g) 
        : Person(n, i), gpa(g) {}
};

class Professor : virtual public Person {  // ← virtual!
public:
    string department;
    Professor(const string& n, int i, const string& d) 
        : Person(n, i), department(d) {}
};

// Now TA has only ONE Person part
class TA : public Student, public Professor {
public:
    // MUST initialize virtual base directly!
    TA(const string& n, int i, double g, const string& d)
        : Person(n, i)           // ← Initialize virtual base FIRST
        , Student(n, i, g)       // Virtual base init ignored here
        , Professor(n, i, d)   // Virtual base init ignored here
    {}
};

// Usage:
TA ta("Alice", 1001, 3.8, "CS");
cout << ta.name;       // ✓ OK: Unambiguous! Single copy
cout << ta.id;         // ✓ OK: Only one id
```



**Memory Layout With Virtual Base / 有虚基类的内存布局：**



```Plain Text
TA Object in Memory:
┌───────────────────────────────┐
│  Shared Person part           │ ← name, id (SINGLE copy!)
│  ├─ name: "Alice"             │
│  └─ id: 1001                  │
├───────────────────────────────┤
│  Student-specific part        │
│  └─ gpa: 3.8                  │
├───────────────────────────────┤
│  Professor-specific part      │
│  └─ department: "CS"          │
├───────────────────────────────┤
│  Pointer to shared Person     │ ← (internal implementation)
│  (vtable for virtual base)    │
└───────────────────────────────┘
```



**Key Rules for Virtual Base Classes:**





|Rule|Explanation|中文解释|
|---|---|---|
|`virtual public Base`|Syntax for virtual inheritance|虚继承语法|

\| **Most derived class** initializes \| TA must call \`Person\(\)\` directly         \| 最终派生类负责初始化   \|

\| Intermediate classes' init ignored \| Student/Professor Person\(\) calls skipped \| 中间类的基类初始化被忽略 \|

\| Single shared instance             \| Only one Base subobject exists           \| 只有一份基类实例     \|





Virtual Base Initialization Order

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NTU3ODVlNGM3N2VkNTA5NGJkZWQ2OTJkZmY5NWE1Y2FfN2MyMjU1NGQxYTcyMWM3N2I4YjA4OThkYjYwZTU4MzBfSUQ6NzYyNjIzODk2NDIyMzA4NTc1NF8xNzgxMDYwMzc4OjE3ODExNDY3NzhfVjM)

*Figure 9: Virtual base initialization order \- the most derived class \(TeachingAssistant\) must directly initialize the virtual base \(Person\), while intermediate classes \(Student/Professor\) skip their virtual base initialization*



**\-\-\-**



#### **Complete Working Example / 完整可运行示例**



```C++
#include <iostream>
#include <string>
using namespace std;

// ========== VIRTUAL BASE CLASS ==========
class Person {
protected:
    string name;
    int id;
    
public:
    Person(const string& n = "", int i = 0) 
        : name(n), id(i) {
        cout << "Person constructor: " << name << endl;
    }
    
    void print() const {
        cout << "Person: " << name << " (ID: " << id << ")" << endl;
    }
};

// VIRTUAL inheritance
class Student : virtual public Person {
protected:
    double gpa;
    string major;
    
public:
    Student(const string& n, int i, double g, const string& m)
        : Person(n, i), gpa(g), major(m) {
        cout << "Student constructor" << endl;
    }
    
    void printStudent() const {
        cout << "  Student - Major: " << major << ", GPA: " << gpa << endl;
    }
};

// VIRTUAL inheritance
class Professor : virtual public Person {
protected:
    string department;
    string courses[10];
    int courseCount;
    
public:
    Professor(const string& n, int i, const string& d)
        : Person(n, i), department(d), courseCount(0) {
        cout << "Professor constructor" << endl;
    }
    
    void printProfessor() const {
        cout << "  Professor - Dept: " << department << endl;
    }
};

// Multiple inheritance with VIRTUAL base
class TA : public Student, public Professor {
private:
    int hoursPerWeek;  // TA-specific
    
public:
    // CRITICAL: Must initialize virtual base Person() directly!
    TA(const string& n, int i, double g, const string& m,
       const string& dept, int hours)
        : Person(n, i)              // ← Direct virtual base init
        , Student(n, i, g, m)       // Person() here is IGNORED
        , Professor(n, i, dept)     // Person() here is IGNORED
        , hoursPerWeek(hours)
    {
        cout << "TA constructor" << endl;
    }
    
    void print() const {
        Person::print();            // Unambiguous! Only one Person
        printStudent();
        printProfessor();
        cout << "  TA Hours: " << hoursPerWeek << "/week" << endl;
    }
};

int main() {
    cout << "=== Creating TA ===" << endl;
    TA ta("Alice Johnson", 1001, 3.9, "Computer Science", 
          "CS Department", 20);
    
    cout << "\n=== TA Info ===" << endl;
    ta.print();
    
    cout << "\n=== Accessing name directly ===" << endl;
    ta.print();  // No ambiguity! Single Person::print()
    
    return 0;
}
```



**Expected Output / 预期输出：**



```Plain Text
=== Creating TA ===
Person constructor: Alice Johnson   ← ONLY ONCE!
Student constructor
Professor constructor
TA constructor

=== TA Info ===
Person: Alice Johnson (ID: 1001)
  Student - Major: Computer Science, GPA: 3.9
  Professor - Dept: CS Department
  TA Hours: 20/week

=== Accessing name directly ===
Person: Alice Johnson (ID: 1001)
...
```



\> **Notice**: \`Person constructor\` is called **only once**, by the most derived class \`TA\`\!



**\-\-\-**



#### **When to Use Virtual Base / 何时使用虚基类**





|Scenario|Use Virtual?|Why|
|---|---|---|
|`class D : public A, public B` \(A and B unrelated\)|❌ No|No shared base|

\| Diamond inheritance pattern                        \| ✓ **Yes**    \| Avoid duplicate base subobjects          \|

\| Interface classes \(pure virtual\)                   \| ✓ Often      \| Multiple interfaces \+ one implementation \|





**Real\-world Examples / 实际场景：**



```C++
// GUI Framework - Widget inherits from multiple mixins
class Widget : virtual public EventHandler,
               virtual public Drawable,
               virtual public Focusable { };
// All three mixins may share a common base (like ReferenceCounted)

// IO Streams - iostream inherits from istream AND ostream
class iostream : public istream, public ostream { };
// Both istream and ostream share virtual base ios_base
```



**\-\-\-**



#### **Interactive Exercise: Fix the Diamond / 互动练习：修复菱形**



**Broken Code / 有问题的代码：**



```C++
class Animal {
public:
    string name;
    Animal(const string& n) : name(n) {}
};

class Flyer : public Animal {
public:
    int wingSpan;
    Flyer(const string& n, int w) : Animal(n), wingSpan(w) {}
};

class Swimmer : public Animal {
public:
    int swimSpeed;
    Swimmer(const string& n, int s) : Animal(n), swimSpeed(s) {}
};

class Duck : public Flyer, public Swimmer {
public:
    Duck(const string& n, int w, int s)
        : Flyer(n, w), Swimmer(n, s) {}  // ⚠️ PROBLEM!
};

int main() {
    Duck duck("Donald", 50, 10);
    cout << duck.name;  // ❌ ERROR: ambiguous
}
```



**Your Task**: Fix the code using virtual inheritance\. Make \`Duck\` have only **one** \`Animal\` part\.



Solution / 解答



```C++
class Animal {
public:
    string name;
    Animal(const string& n) : name(n) {}
};

class Flyer : virtual public Animal {  // ← Add virtual!
public:
    int wingSpan;
    Flyer(const string& n, int w) : Animal(n), wingSpan(w) {}
};

class Swimmer : virtual public Animal {  // ← Add virtual!
public:
    int swimSpeed;
    Swimmer(const string& n, int s) : Animal(n), swimSpeed(s) {}
};

class Duck : public Flyer, public Swimmer {
public:
    Duck(const string& n, int w, int s)
        : Animal(n)              // ← Must init virtual base directly
        , Flyer(n, w)            // Animal() ignored here
        , Swimmer(n, s) {}       // Animal() ignored here
};

int main() {
    Duck duck("Donald", 50, 10);
    cout << duck.name;  // ✓ OK: Unambiguous!
}
```



**\-\-\-**



## **5\. Interactive Exercises / 互动练习**



### **Exercise 1: Design Inheritance Hierarchy / 练习1：设计继承层次**



**Scenario**: A game has Characters\. Characters can be Warriors or Mages\.



All Characters have:



- name

- health

- level

Warriors have:



- strength

- weapon

Mages have:



- mana

- spellBook

**Your Task**:



1. Draw the UML diagram

2. Write the C\+\+ class declarations \(no implementation needed\)

Click for solution outline / 点击查看解答框架



```C++
class Character {
protected:
    string name;
    int health;
    int level;
public:
    Character(string n, int h, int l);
    void takeDamage(int dmg);
};

class Warrior : public Character {
private:
    int strength;
    string weapon;
public:
    Warrior(string n, int h, int l, int str, string w);
    void attack();
};

class Mage : public Character {
private:
    int mana;
    string spellBook[10];
public:
    Mage(string n, int h, int l, int m);
    void castSpell();
};
```



**\-\-\-**



### **Exercise 2: Constructor Order Quiz / 练习2：构造顺序测验**



What is the output of this code?



```C++
class A {
public:
    A() { cout << "A constructed" << endl; }
    ~A() { cout << "A destroyed" << endl; }
};

class B : public A {
public:
    B() { cout << "B constructed" << endl; }
    ~B() { cout << "B destroyed" << endl; }
};

class C : public B {
public:
    C() { cout << "C constructed" << endl; }
    ~C() { cout << "C destroyed" << endl; }
};

int main() {
    C obj;
    return 0;
}
```



Click for answer / 点击查看答案



```Plain Text
A constructed
B constructed
C constructed
C destroyed
B destroyed
A destroyed
```



**Rule**: Construction goes top\-down \(base first\), destruction goes bottom\-up \(derived first\)\.



**\-\-\-**



### **Exercise 3: Access Control Challenge / 练习3：访问控制挑战**



Given:



```C++
class Base {
private:    int a;
protected:  int b;
public:     int c;
};

class Derived : public Base {
public:
    void test() {
        // Which lines are valid?
        a = 1;  // ???
        b = 2;  // ???
        c = 3;  // ???
    }
};

int main() {
    Derived d;
    // Which lines are valid?
    d.a = 1;  // ???
    d.b = 2;  // ???
    d.c = 3;  // ???
}
```



Mark each line: ✓ \(valid\) or ❌ \(error\)



Click for answers / 点击查看答案



Inside `Derived::test()`:



- `a = 1;` ❌ \- `a` is private to Base

- `b = 2;` ✓ \- `b` is protected, accessible to derived

- `c = 3;` ✓ \- `c` is public

Inside `main()`:



- `d.a = 1;` ❌ \- private

- `d.b = 2;` ❌ \- protected \(only accessible in class and derived classes\)

- `d.c = 3;` ✓ \- public

**\-\-\-**



## **6\. Key Takeaways / 核心要点**



### **5\.1 Summary Table / 总结表**





|Concept|Key Point|Analogy|
|---|---|---|
|Inheritance|`class D : public B`|Genetic traits|
|`protected`|Private to world, accessible to children|Family recipe|
|Constructor|Base → Derived \(top\-down\)|Build foundation first|
|Destructor|Derived → Base \(bottom\-up\)|Remove roof first|
|UML Arrow|`◄───` hollow triangle|Points to parent|





### **5\.2 Design Checklist / 设计检查清单**



When designing inheritance:



- Is it "is\-a"? \(Student is\-a Person\) ✓

- Is it "has\-a"? Consider composition instead

- Common attributes in base class?

- `protected` for data derived classes need?

- Base class constructor called in init list?

- `public` inheritance \(most cases\)?

**\-\-\-**



## **7\. Mini Project: Refactor with Inheritance / 小项目：用继承重构**



**Starting Code** \(without inheritance\):



```C++
class Dog {
    string name;
    int age;
    string breed;
public:
    Dog(string n, int a, string b);
    void speak() { cout << "Woof!" << endl; }
};

class Cat {
    string name;
    int age;
    bool indoor;
public:
    Cat(string n, int a, bool i);
    void speak() { cout << "Meow!" << endl; }
};
```



**Your Task**: Refactor using a common \`Animal\` base class\.



**Requirements**:



1. Extract common attributes \(`name`, `age`\)

2. Use `protected` appropriately

3. Call base constructor in derived classes

4. Keep unique attributes in derived classes

**\-\-\-**



\> **Next Chapter Preview**: Now that we can organize related classes, how do we make them respond differently to the same command? Enter **Polymorphism**\.\.\.





