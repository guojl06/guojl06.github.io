# Week 6 Lifetime

# **Chapter 6: Classes Deep Dive \- Constructor, Destructor, Inheritance, Object Lifetime**



## **\#\#\# 📁 Basic File Management Rules for Beginners**



**The Golden Rule:** Keep your projects organized from day one\. Messy files = messy code\.



**Do's:**

\- **Create a dedicated folder** for every project \(e\.g\., \`C:\\Projects\\\` or \`\~/Documents/Code/\`\)

\- **Use clear folder names**: \`MyFirstWebsite\`, \`Python\-Homework\`, \`2026\-Learn\-JavaScript\`

\- **Separate by file type**: Put images in \`images/\`, documents in \`docs/\`, source code in \`src/\`

\- **Date your archives**: If you need backups, use \`ProjectName\-v1\`, \`ProjectName\-v2\` or add dates \`2026\-04\-01\-backup\`



**Don'ts:**

\- ❌ **Never save source files to Desktop** — it becomes a chaotic mess within a week

- ❌ Don't use spaces or Chinese in folder/file names \(use `MyProject` or `my_project`, not `My Project`, not `程设`\)

- ❌ Don't dump everything in one folder — you'll never find anything later

**Quick Example Structure:**

```Plain Text
Documents/
└── Code/
    ├── Learn-C++/
    │   ├── week1
    |   |   |──main.cpp
    |   |   |──student.cpp
    |   |   |──student.h    
    │   ├── week2
    └── notes.txt
```



**Why this matters:** Clean folders help you find bugs faster, prevent accidental deletion, and teach professional habits that employers expect\.



**\-\-\-**



*Pro tip: Treat your computer like a workspace, not a junk drawer\.*



**\-\-\-**



## **0\. Bilingual Quick Reference**



### **Table 1: Core Concepts**



|Chinese \(中文\)|English|Description|
|---|---|---|
|类|Class|A user\-defined type that bundles data and behavior\.|
|对象|Object|An instance of a class stored in memory\.|
|构造函数|Constructor|A special function called when an object is created\.|
|析构函数|Destructor|A special function called when an object is destroyed\.|
|继承|Inheritance|Building a new class from an existing class\.|
|封装|Encapsulation|Hide internals, expose safe public operations\.|
|生存期 / 生命周期|Lifetime|Duration from variable/object creation to destruction\.|
|作用域|Scope|Region of code where a variable name is visible/accessible\.|
|局部变量|Local Variable|Variable defined inside a function/block; destroyed when leaving scope\.|
|全局变量|Global Variable|Variable defined outside any function; lives for entire program\.|
|静态变量|Static Variable|Variable with extended lifetime but restricted scope\.|
|初始化|Initialization|Giving a variable its initial value at creation time\.|
|初始化列表|Initialization List|Constructor syntax for initializing members before body executes\.|
|公有继承|Public Inheritance|`public` base members keep access level in derived class\.|
|私有继承|Private Inheritance|Base `public`/`protected` members become `private` in derived\.|
|对象数组|Object Array|Array where each element is an object of a class\.|
|基类|Base Class|Parent class being inherited from\.|
|派生类|Derived Class|Child class inheriting from base class\.|



### **Table 2: Symbols \& Keywords**



|Symbol/Keyword|English Name|Chinese \(中文\)|Usage/Meaning|
|---|---|---|---|
|`::`|Scope Resolution|作用域解析符|Define member functions outside class|
|`.`|Member Access|成员访问符|Access member via object|
|`->`|Arrow Operator|箭头操作符|Access member via pointer|
|`:`|Inheritance/Init List|继承/初始化列表符号|`class B : public A`, constructor init list|
|`const`|Const Qualifier|常量限定符|Promise not to modify object state|
|`static`|Static Keyword|静态关键字|Extend variable lifetime, limit scope|
|`this`|This Pointer|自身指针|Points to current object instance|
|`private`|Private Access|私有访问权限|Only accessible within same class|
|`protected`|Protected Access|保护访问权限|Accessible within class and derived classes|
|`public`|Public Access|公有访问权限|Accessible from anywhere|



### **Table 3: Lifetime\-Related Terms**



|English|Chinese \(中文\)|Explanation|
|---|---|---|
|Automatic Storage Duration|自动存储期|Local variables; created on entry, destroyed on exit from scope\.|
|Static Storage Duration|静态存储期|Global and static variables; created at program start, destroyed at program end\.|
|Dynamic Storage Duration|动态存储期|Variables created with `new`; programmer controls lifetime\.|
|Scope|作用域|Where the variable name can be used to refer to the entity\.|
|Visibility|可见性|Whether a name can be referenced from a given point in code\.|
|Object Lifetime|对象生命周期|Duration from construction to destruction\.|
|RAII|资源获取即初始化|Resource lifecycle is bound to object lifetime\.|



### **Term intuition \(beginner\-friendly, Chinese\)**



Use this as a **mental hook**; formal definitions are in the tables above\.



\- **类 / Class**: 把数据和行为绑在一起；若只用零散全局变量，很难保证状态一致。

\- **构造函数**: 对象"出生"时自动执行，用来把对象放到合法状态；反例：先创建对象再漏写字段赋值。

\- **析构函数**: 对象"销毁"前自动执行；反例：在析构里写复杂业务逻辑，难以调试。

\- **继承**: 复用并扩展已有类型；反例：仅为复制代码而继承 unrelated 类。

\- **生存期 / Lifetime**: 变量从"诞生"到"死亡"的时间段；局部变量随代码块生灭，全局变量随程序生灭。

\- **作用域 / Scope**: 变量名在哪些代码行可以被使用；出了作用域，变量名就"看不见"了（但对象可能还活着，如果有其他引用）。

\- **局部变量**: 函数内部的变量，离开函数就销毁；反例：需要长期保存的数据用了局部变量。

\- **全局变量**: 所有函数都能访问的变量，程序结束才销毁；反例：滥用全局变量导致代码难以理解和测试。

\- **静态变量**: 只在定义处初始化一次，值会保持到下次访问；反例：在多线程环境不注意同步问题。

\- **初始化列表**: 在构造函数体执行前就初始化成员，更高效且必需用于 const 和引用成员。



**\-\-\-**



## **1\. Variable Lifetime and Scope Fundamentals \(变量生存期与作用域基础\)**



### **1\.1 The Core Concept: Why Lifetime Matters**



Every variable in C\+\+ has a **lifetime** \(生存期\) — the period during which it exists in memory and holds a valid value\. Understanding lifetime is crucial because:



1\. **Accessing destroyed variables causes bugs**: Using a variable after its lifetime ends is undefined behavior\.

2\. **Resource management**: Files, network connections, and memory should be released when no longer needed\.

3\. **Program correctness**: Knowing when objects are created and destroyed helps predict program behavior\.



### **1\.2 Three Fundamental Storage Durations**



C\+\+ has three main storage duration categories:



|Storage Duration|Chinese|Typical Variables|Creation Time|Destruction Time|
|---|---|---|---|---|
|Automatic|自动存储期|Local variables inside functions/blocks|When entering scope|When leaving scope|
|Static|静态存储期|Global variables, `static` local variables|Program start|Program end|
|Dynamic|动态存储期|Objects created with `new`|When `new` is called|When `delete` is called|



### **1\.3 Local Variables \(Automatic Storage\)**



Local variables are created when execution enters their scope and destroyed when leaving\.



```C++
void demonstrateLocalVariables() {
    int a = 10;           // Created here
    cout << a << endl;    // Valid: a exists
    
    if (a > 5) {
        int b = 20;       // b created when entering if-block
        cout << b << endl;
    }                     // b destroyed here
    
    // cout << b << endl; // ERROR: b no longer exists!
}                         // a destroyed here

int main() {
    demonstrateLocalVariables();
    // All local variables from the function are now destroyed
    return 0;
}
```



**Key Characteristics of Local Variables:**

\- Created on the **stack** \(typically\)

- Automatically destroyed when scope ends

- Each function call gets fresh copies

- Safe and easy to use — preferred for most temporary data

### **1\.4 Global Variables \(Static Storage\)**



Global variables are defined outside all functions and exist for the entire program duration\.



```C++
#include <iostream>
using namespace std;

// Global variables - exist for entire program
int globalCounter = 0;
string systemName = "University System";

void incrementCounter() {
    globalCounter++;      // Accessible from any function
    cout << "Counter: " << globalCounter << endl;
}

void printSystemInfo() {
    cout << "System: " << systemName << endl;
}

int main() {
    incrementCounter();   // Prints: Counter: 1
    incrementCounter();   // Prints: Counter: 2
    printSystemInfo();    // Prints: System: University System
    return 0;
}
```



**When to Use Global Variables \(Sparingly\!\):**

- Truly global configuration \(like `systemName` above\)

- Constants that never change \(use `const`\)

- Singleton\-like shared resources

**Dangers of Global Variables:**

- Any function can modify them — hard to track changes

- Makes testing difficult \(functions have hidden dependencies\)

- Name collisions in large programs

- Initialization order issues across files

**Better Practice for Global Constants:**

```C++
// In header file
namespace Config {
    const int MAX_COURSES = 50;        // Better: namespace + const
    const double DEFAULT_GPA = 0.0;
}

Config::MAX_COURSES 
```



### **1\.5 Static Variables \(The Best of Both Worlds\)**



Static variables combine **extended lifetime** \(like globals\) with **restricted scope** \(like locals\)\.



#### **1\.5\.1 Static Local Variables**



Static local variables maintain their value between function calls but are only accessible within the function\.



```C++
void visitCount() {
    static int visitCount = 0;  // Initialized ONLY once!
    visitCount++;
    cout << "Visit #" << visitCount << endl;
}

int main() {
    visitCount();  // Visit #1
    visitCount();  // Visit #2
    visitCount();  // Visit #3
    // visitCount is not accessible here (good! scope is limited)
    return 0;
}
```



**Use Cases for Static Local Variables:**

- Function call counters

- Caching/memoization

- Singleton pattern implementation

- Any data that needs to persist but shouldn't be globally visible

#### **1\.5\.2 Static Member Variables \(Class\-Level Data\)**



Static member variables are shared across all objects of a class\.



```C++
class Student {
private:
    int id;
    string name;
    static int totalStudents;  // Shared by ALL students
    
public:
    Student(int i, const string& n) : id(i), name(n) {
        totalStudents++;
        cout << "Student created. Total: " << totalStudents << endl;
    }
    
    ~Student() {
        totalStudents--;
        cout << "Student destroyed. Total: " << totalStudents << endl;
    }
    
    static int getTotalStudents() {
        return totalStudents;
    }
};

// REQUIRED: Define static member outside class
int Student::totalStudents = 0;

int main() {
    cout << "Initial total: " << Student::getTotalStudents() << endl;
    
    Student s1(1001, "Alice");  // Total: 1
    Student s2(1002, "Bob");    // Total: 2
    
    {
        Student s3(1003, "Carol");  // Total: 3
    }  // s3 destroyed, Total: 2
    
    cout << "Final total: " << Student::getTotalStudents() << endl;  // 2
    return 0;
}
```



**Key Points about Static Members:**

- Only ONE copy exists, shared by all objects

- Must be defined outside the class \(in \.cpp file\)

- Can be accessed via class name: `Student::getTotalStudents()`

- Useful for: counting objects, shared configuration, class\-wide constants

### **1\.6 Scope vs Lifetime \(重要区别\)**



**Scope** \(作用域\): Where the variable name is visible — compile\-time concept

**Lifetime** \(生存期\): When the variable actually exists in memory — runtime concept



They usually match, but not always:



```C++
void scopeVsLifetimeDemo() {
    // Example: static variable has limited scope but extended lifetime
    static int counter = 0;
    counter++;
    
    // 'counter' is only visible inside this function (scope)
    // But 'counter' exists for entire program (lifetime)
}

// Example: dynamically allocated object
void dynamicDemo() {
    // Local pointer - automatic storage
    int* ptr = new int(42);  // Dynamic int created
    
    // ptr itself is local (will be destroyed when function ends)
    // But the int it points to lives until delete is called!
    
    delete ptr;  // Now the dynamic int is destroyed
}  // ptr destroyed here, but if we forgot delete, memory leaks!
```



### **Checkpoint 1 \(you should now be able to\)**



1. Explain the difference between scope and lifetime with your own example\.

2. Predict how many times `static int count = 0;` is initialized in a function called 5 times\.

3. Name one danger of global variables and one appropriate use case\.

4. When does a local variable's lifetime end? When does a static variable's lifetime end?

**\-\-\-**



## **2\. Constructors and Initialization Deep Dive \(构造函数与初始化深入\)**



### **2\.1 The Problem: Why Constructors Matter for Lifetime**



Proper initialization is the **start of an object's lifetime**\. A poorly initialized object is a bug waiting to happen\.



**Before Constructors \(Procedural Style\):**

```C++
// Old withProf style - risky!
Professor prof;
prof.id = 1001;           // What if we forget this line?
prof.name = "Dr. Smith";  // What if name stays empty?
prof.courseCount = 0;     // Manual initialization everywhere
// Object could be in invalid state between creation and initialization!
```



**After Constructors \(Object\-Oriented Style\):**

```C++
// Better: Object is valid immediately after birth
Professor prof(1001, "Dr. Smith");  // All fields initialized at once
// No possibility of half-initialized object!
```



### **2\.2 Constructor Types and When They're Called**



```C++
class Professor {
private:
    int id;
    string name;
    string courses[50];
    int courseCount;
    
public:
    // 1. Default Constructor - called when no arguments provided
    Professor() : id(0), courseCount(0) {
        for (int i = 0; i < 50; i++) {
            courses[i] = "";
        }
    }
    
    // 2. Parameterized Constructor - called with arguments
    Professor(int id, const string& name) 
        : id(id), name(name), courseCount(0) {
        for (int i = 0; i < 50; i++) {
            courses[i] = "";
        }
    }
    
    // 3. Copy Constructor - called when copying objects
    Professor(const Professor& other)
        : id(other.id), name(other.name), courseCount(other.courseCount) {
        for (int i = 0; i < courseCount; i++) {
            courses[i] = other.courses[i];
        }
        for (int i = courseCount; i < 50; i++) {
            courses[i] = "";
        }
    }
};
```



**Constructor Call Examples:**

```C++
Professor p1;                          // Default constructor
Professor p2(1001, "Dr. Smith");       // Parameterized constructor
Professor p3 = p2;                     // Copy constructor
Professor p4(p2);                      // Also copy constructor
void func(Professor p);  
func(p2);    // Copy constructor (pass by value)
Professor returnProf() 
{ 
    Professor p; 
    return p; 
}  // Copy/move constructor

p2 = returnProf();
```



### **2\.3 Member Initialization List \(成员初始化列表\)**



The initialization list runs **before** the constructor body executes\. It is the preferred way to initialize members\.



**Syntax:**

```C++
ClassName(parameters) : member1(value1), member2(value2), ... {
    // Constructor body
}
```



**Why Prefer Initialization Lists:**



|Aspect|Initialization List|Assignment in Body|
|---|---|---|
|Timing|Before body executes|During body execution|
|Efficiency|Direct initialization|Default construction \+ assignment|
|const members|REQUIRED|Not possible|
|Reference members|REQUIRED|Not possible|
|Base class initialization|REQUIRED|Not possible|



**Example Comparison:**



```C++
// Less efficient: default construct then assign
class Professor {
    string name;
    int id;
public:
    Professor(int i, const string& n) {
        name = n;   // First: default constructs empty string
        id = i;     // Then: assigns new value
    }
};

// More efficient: direct initialization
class Professor {
    string name;
    int id;
public:
    Professor(int i, const string& n) 
        : name(n)   // Direct construct with value
        , id(i)     // Direct initialization
    {
        // Empty body is fine!
    }
};
```



### **2\.4 Initialization Order \(Important\!\)**



Members are initialized in the **order they are declared in the class**, NOT the order in the initialization list\!



```C++
class InitializationOrderDemo {
    int a;  // Declared first
    int b;  // Declared second
    int c;  // Declared third
    
public:
    // Even though list order is c, a, b...
    InitializationOrderDemo() 
        : c(3)   // ...a is initialized first (declared first!)
        , a(1)   // ...then b (declared second!)
        , b(2)   // ...then c (declared third!)
    {
        cout << a << b << c << endl;  // Prints: 1 2 3
    }
};
```



**Best Practice:** Always write initialization list in the same order as member declarations to avoid confusion\.



### **2\.5 Constructor Validation: Enforcing Invariants**



Use constructors to ensure objects start in valid states\.



```C++
class Professor {
private:
    int id;
    string name;
    int courseCount;
    static const int MAX_COURSES = 50;
    
public:
    Professor(int id, const string& name)
        : id(id > 0 ? id : -1)           // Validate: ID must be positive
        , name(name.empty() ? "Unknown" : name)  // Validate: name can't be empty
        , courseCount(0)                 // Always start with 0 courses
    {
        // Post-construction validation
        if (this->id == -1) {
            cout << "Warning: Invalid ID provided, using -1\n";
        }
    }
    
    bool isValid() const { return id > 0; }
};
```



### **2\.6 Default Member Initializers \(C\+\+11 and later\)**



You can provide default values directly in the class definition:



```C++
class ModernProfessor {
private:
    int id = 0;                    // Default member initializer
    string name = "Unknown";
    int courseCount = 0;
    static const int MAX_COURSES = 50;
    
public:
    // Default constructor - members already initialized
    ModernProfessor() = default;
    
    // Parameterized constructor - can override defaults
    ModernProfessor(int i, const string& n)
        : id(i > 0 ? i : 0)
        , name(n.empty() ? "Unknown" : n)
    {
        // courseCount already 0 from default initializer
    }
};
```



### **2\.7 Common Constructor Mistakes**



|Mistake|Why Wrong|Correct Way|
|---|---|---|
|`id = id;`|Parameter shadows member, self\-assigns|`this->id = id` or init list|
|Forgetting to initialize all members|Object in undefined state|Use init list, provide defaults|
|Complex logic in constructor|Can throw exceptions, hard to debug|Keep simple, validate inputs|
|Calling virtual functions|Derived class not yet constructed|Avoid virtual calls in constructor|
|`Professor()` instead of `Professor`|Creates temporary, not variable|Just write `Professor p;`|



### **Checkpoint 2 \(you should now be able to\)**



1. Write a constructor using initialization list for a `Course` class with `code`, `name`, and `capacity`\.

2. Explain why `const` members must use initialization lists\.

3. Identify the bug: `Professor(int id) { id = id; }`

4. Predict initialization order given member declaration order vs init list order\.

**\-\-\-**



## **3\. Destructors and Object Lifetime End \(析构函数与对象生存期结束\)**



### **3\.1 Destructor Fundamentals**



A destructor is called automatically when an object's lifetime ends\. Its job is to clean up resources and perform final actions\.



**Syntax:**

```C++
class ClassName {
public:
    ~ClassName() {  // Destructor: ~ + ClassName
        // Cleanup code
    }
};
```



**Characteristics:**

- No return type, no parameters

- Exactly one destructor per class

- Cannot be overloaded

- Automatically generated if not defined

### **3\.2 When Is the Destructor Called?**



```C++
void demonstrateDestructorTiming() {
    cout << "Entering function\n";
    
    Professor p1(1001, "Dr. A");  // Constructor called
    cout << "p1 created\n";
    
    {  // New scope
        Professor p2(1002, "Dr. B");  // Constructor
        cout << "p2 created\n";
    }  // p2's destructor called here!
    
    cout << "p2 destroyed\n";
    cout << "Leaving function\n";
}  // p1's destructor called here!

int main() {
    demonstrateDestructorTiming();
    cout << "Function returned\n";
    return 0;
}
```



**Output:**

```Plain Text
Entering function
p1 created
p2 created
p2 destroyed
Leaving function
p1 destroyed
Function returned
```



### **3\.3 Destructor Order: Reverse of Construction**



When multiple objects are destroyed, they follow **reverse construction order** \(LIFO: Last In, First Out\)\.



```C++
class Trace {
    string label;
public:
    Trace(const string& s) : label(s) {
        cout << "Creating: " << label << endl;
    }
    ~Trace() {
        cout << "Destroying: " << label << endl;
    }
};

void nestedScopes() {
    Trace a("outer");
    {
        Trace b("inner-1");
        Trace c("inner-2");
    }
    Trace d("outer-end");
}
```



**Output:**

```Plain Text
Creating: outer
Creating: inner-1
Creating: inner-2
Destroying: inner-2
Destroying: inner-1
Creating: outer-end
Destroying: outer-end
Destroying: outer
```



### **3\.4 Practical Example: Session Tracking**



```C++
class AuditSession {
    string sessionId;
    static int activeSessions;
    
public:
    AuditSession(const string& id) : sessionId(id) {
        activeSessions++;
        cout << "[" << sessionId << "] Session started. "
             << "Active: " << activeSessions << endl;
    }
    
    ~AuditSession() {
        activeSessions--;
        cout << "[" << sessionId << "] Session ended. "
             << "Active: " << activeSessions << endl;
    }
    
    static int getActiveCount() { return activeSessions; }
};

int AuditSession::activeSessions = 0;

void processProfessor() {
    AuditSession session("prof-1001");
    // Do work...
    cout << "Processing professor...\n";
}  // session destroyed here

void processCourse() {
    AuditSession session("course-CS101");
    processProfessor();  // Nested session
    cout << "Processing course...\n";
}  // course session destroyed

int main() {
    cout << "Starting main\n";
    processCourse();
    cout << "Main ending. Active sessions: " 
         << AuditSession::getActiveCount() << endl;
    return 0;
}
```



**Output:**

```Plain Text
Starting main
[course-CS101] Session started. Active: 1
[prof-1001] Session started. Active: 2
Processing professor...
[prof-1001] Session ended. Active: 1
Processing course...
[course-CS101] Session ended. Active: 0
Main ending. Active sessions: 0
```



### **3\.5 Object Arrays and Destructors**



When an array of objects is destroyed, each element's destructor is called in **reverse order**\.



```C++
class Simple {
    int id;
public:
    Simple(int i) : id(i) { cout << "Created #" << id << endl; }
    ~Simple() { cout << "Destroyed #" << id << endl; }
};

int main() {
    Simple arr[3] = {Simple(1), Simple(2), Simple(3)};
    cout << "Array created\n";
    // arr destroyed when main ends
    // Destruction order: 3, 2, 1 (reverse)
    return 0;
}
```



**Output:**

```Plain Text
Created #1
Created #2
Created #3
Array created
Destroyed #3
Destroyed #2
Destroyed #1
```



### **3\.6 Common Destructor Mistakes**



|Mistake|Symptom|Fix|
|---|---|---|
|Throwing exceptions|Program termination|Never throw from destructor|
|Heavy business logic|Hard\-to\-debug side effects|Keep cleanup only|
|Forgetting virtual destructor|Memory leaks in inheritance|Add `virtual ~Base()` for base classes|
|Accessing other objects|May already be destroyed|Don't depend on external state|



### **Checkpoint 3 \(you should now be able to\)**



1. Predict destructor call order for three nested objects\.

2. Explain why destructors run in reverse order of constructors\.

3. Write a simple class that tracks how many instances are active\.

4. When is a local object's destructor called? A global object's destructor?

**\-\-\-**



## **4\. Object Arrays \(对象数组\)**



### **4\.1 Declaring and Initializing Object Arrays**



Object arrays allow you to manage collections of objects with the same lifetime\.



```C++
class Professor {
    int id;
    string name;
public:
    Professor() : id(0), name("Unknown") {}  // Default constructor required!
    Professor(int i, const string& n) : id(i), name(n) {}
    void print() const { cout << id << ": " << name << endl; }
};

int main() {
    // Array of 3 Professors - default constructor called for each
    Professor faculty[3];
    
    // Each element can be accessed and modified
    faculty[0] = Professor(1001, "Dr. Smith");
    faculty[1] = Professor(1002, "Dr. Jones");
    faculty[2] = Professor(1003, "Dr. Lee");
    
    for (int i = 0; i < 3; i++) {
        faculty[i].print();
    }
    
    return 0;  // All 3 destructors called in reverse order
}
```



### **4\.2 Initialization List for Arrays**



You can initialize arrays using brace\-enclosed lists:



```C++
// Explicit initialization for each element
Professor faculty[3] = {
    Professor(1001, "Dr. Smith"),
    Professor(1002, "Dr. Jones"),
    Professor(1003, "Dr. Lee")
};

// With C++11 and later, can be simpler:
Professor faculty2[3] = {
    {1001, "Dr. Smith"},   // Implicit constructor call
    {1002, "Dr. Jones"},
    {1003, "Dr. Lee"}
};
```



### **4\.3 Arrays in Classes: Managing Collections**



A common pattern is for a class to manage an array of objects:



```C++
class Department {
private:
    string name;
    Professor professors[10];  // Fixed-size array
    int professorCount;
    
public:
    Department(const string& n) 
        : name(n), professorCount(0) {
        // professors array already default-constructed
    }
    
    bool addProfessor(int id, const string& profName) {
        if (professorCount >= 10) {
            return false;  // Department is full
        }
        professors[professorCount] = Professor(id, profName);
        professorCount++;
        return true;
    }
    
    void printRoster() const {
        cout << "Department: " << name << endl;
        cout << "Professors (" << professorCount << "):\n";
        for (int i = 0; i < professorCount; i++) {
            cout << "  ";
            professors[i].print();
        }
    }
};
```



### **4\.4 Lifetime of Array Elements**



All elements in an array share the **same lifetime** as the array itself:



```C++
void arrayLifetimeDemo() {
    // All 5 Professors created here
    Professor team[5];
    cout << "Team assembled\n";
    
    // ... use the team ...
    
}  // All 5 destructors called here (in reverse order: 4, 3, 2, 1, 0)

int main() {
    arrayLifetimeDemo();
    cout << "Team disbanded\n";
    return 0;
}
```



### **4\.5 Static Arrays vs Local Arrays**



```C++
// Global array - static storage duration
Professor globalFaculty[5];  // Lives entire program, initialized before main()

void functionWithLocalArray() {
    // Local array - automatic storage duration
    Professor localTeam[3];    // Created on entry, destroyed on exit
    
    // Static local array - static storage duration, local scope
    static Professor staticTeam[2];  // Created once, persists between calls
}
```



### **4\.6 Common Array Mistakes**



|Mistake|Why Wrong|Correct Way|
|---|---|---|
|Missing default constructor|Array initialization fails|Provide default constructor|
|Array bounds violation|Undefined behavior, crashes|Always check index \< size|
|`Professor arr[3] = Professor(1, "A");`|Tries to assign one to array|Use brace list or loop|
|Returning local array|Dangling reference|Use static, dynamic allocation, or pass in buffer|



### **Checkpoint 4 \(you should now be able to\)**



1. Create an array of 5 `Course` objects and initialize them with different values\.

2. Explain when array element destructors are called\.

3. Why does `Professor arr[10];` require a default constructor?

4. Write a `University` class that manages an array of `Department` objects\.

**\-\-\-**



## **5\. Access Control and Encapsulation \(访问控制与封装\)**



### **5\.1 The Three Access Levels**



Access specifiers control **who can use** class members:



```C++
class AccessDemo {
private:      // Only this class can access
    int secretId;
    void internalHelper() {}
    
protected:    // This class and derived classes can access
    int familyId;
    void familyMethod() {}
    
public:       // Anyone can access
    int publicId;
    void publicMethod() {}
};
```



|Access Level|Same Class|Derived Class|Outside Code|
|---|---|---|---|
|`private`|✓|✗|✗|
|`protected`|✓|✓|✗|
|`public`|✓|✓|✓|



### **5\.2 Encapsulation in Practice**



**Goal:** Hide internal state, expose controlled interface\.



```C++
class Professor {
private:
    int id;                    // Private: can't be modified directly
    string name;
    string courses[50];
    int courseCount;
    static const int MAX_COURSES = 50;
    
public:
    // Constructor - controlled initialization
    Professor(int id, const string& name);
    
    // Getter methods (read-only access)
    int getId() const { return id; }
    string getName() const { return name; }
    int getCourseCount() const { return courseCount; }
    
    // Controlled modification
    void addCourse(const string& course);
    void removeCourse(const string& course);
    
    // Utility method using internal state
    void print() const;
    bool isTeaching(const string& course) const;
};
```



**Benefits of Encapsulation:**

1\. **Invariant protection**: \`id\` can't become negative because we validate in constructor

2\. **Flexibility**: Can change internal representation without affecting users

3\. **Debugging**: All modifications go through controlled methods

4\. **Safety**: Can't accidentally corrupt object state



### **5\.3 Friend Functions \(Occasional Exception\)**



Sometimes you need external functions to access private members:



```C++
class Professor {
private:
    int id;
    string name;
    
public:
    Professor(int i, const string& n) : id(i), name(n) {}
    
    // Grant access to specific external function
    friend bool haveSameDepartment(const Professor& a, const Professor& b);
};

// Friend function can access private members
bool haveSameDepartment(const Professor& a, const Professor& b) {
    // Hypothetically checking if same department
    // Can access a.id and b.id directly
    return (a.id / 1000) == (b.id / 1000);  // Same department prefix
}
```



**Use friends sparingly** — they break encapsulation\. Prefer public interfaces\.



### **Checkpoint 5 \(you should now be able to\)**



1. List the three access levels and who can access each\.

2. Explain why `private` members with `public` getters are better than public members\.

3. Write a `Course` class with private `code` and `capacity`, public getters, and controlled enrollment method\.

**\-\-\-**



## **6\. Inheritance with Constructors and Destructors \(继承中的构造与析构\)**



### **6\.1 Basic Inheritance Syntax**



Inheritance allows a derived class to reuse and extend a base class:



```C++
// Base class
class Person {
protected:  // Accessible to derived classes
    int id;
    string name;
    
public:
    Person(int i, const string& n) : id(i), name(n) {}
    
    void printBasic() const {
        cout << "ID: " << id << ", Name: " << name << endl;
    }
    
    int getId() const { return id; }
    string getName() const { return name; }
};

// Derived class
class Student : public Person {
private:
    double gpa;
    string major;
    
public:
    // Must call base constructor in initialization list
    Student(int i, const string& n, double g, const string& m)
        : Person(i, n)      // Base constructor first!
        , gpa(g)
        , major(m)
    {}
    
    void print() const {
        printBasic();  // Reuse base method
        cout << "GPA: " << gpa << ", Major: " << major << endl;
    }
};

// Another derived class
class Professor : public Person {
private:
    string department;
    int yearsOfService;
    
public:
    Professor(int i, const string& n, const string& dept, int years)
        : Person(i, n)
        , department(dept)
        , yearsOfService(years)
    {}
    
    void print() const {
        printBasic();
        cout << "Department: " << department 
             << ", Experience: " << yearsOfService << " years" << endl;
    }
};
```



### **6\.2 Construction Order in Inheritance**



When creating a derived object:



1\. **Base class** constructor runs first

2\. **Member variables** are initialized \(in declaration order\)

3\. **Derived class** constructor body runs



```C++
class Base {
public:
    Base() { cout << "Base constructor\n"; }
};

class Member {
public:
    Member() { cout << "Member constructor\n"; }
};

class Derived : public Base {
    Member m;
public:
    Derived() { cout << "Derived constructor\n"; }
};

// Creating Derived:
// 1. "Base constructor"
// 2. "Member constructor"  
// 3. "Derived constructor"
```



### **6\.3 Destruction Order in Inheritance**



Destruction is the **reverse** of construction:



1\. **Derived class** destructor runs

2\. **Member variables** are destroyed \(reverse declaration order\)

3\. **Base class** destructor runs



```C++
class Base {
public:
    ~Base() { cout << "Base destructor\n"; }
};

class Member {
public:
    ~Member() { cout << "Member destructor\n"; }
};

class Derived : public Base {
    Member m;
public:
    ~Derived() { cout << "Derived destructor\n"; }
};

// Destroying Derived:
// 1. "Derived destructor"
// 2. "Member destructor"
// 3. "Base destructor"
```



### **6\.4 Access Control in Inheritance**



#### **Public Inheritance \(\`class B : public A\`\)**

\- Models **is\-a** relationship

- Base `public` members stay `public` in derived

- Base `protected` members stay `protected` in derived

```C++
class Person {
public:
    void greet() { cout << "Hello!\n"; }
};

class Student : public Person {
    // greet() is still public here
};

Student s;
s.greet();  // OK: Student is-a Person
```



#### **Private Inheritance \(\`class B : private A\`\)**

\- Models **implemented\-in\-terms\-of** relationship

- Base `public` and `protected` members become `private` in derived

- Not an "is\-a" relationship to outside world

```C++
class Logger {
protected:
    void log(const string& msg) { cout << msg << endl; }
};

class CourseManager : private Logger {
public:
    void recordAction(const string& action) {
        log(action);  // Can use internally
    }
    // log() is NOT accessible from outside
};

CourseManager cm;
// cm.log("test");  // ERROR: log is private!
cm.recordAction("Added course");  // OK
```



### **6\.5 Inheritance vs Composition**



**Use inheritance when:**

- Clear "is\-a" relationship \(Student is\-a Person\)

- Need to reuse interface, not just implementation

- Derived class should be substitutable for base class

**Use composition when:**

- "has\-a" relationship \(Professor has\-a array of courses\)

- Just need to reuse implementation

- Don't want to expose base class interface

```C++
// Composition: Professor has-a collection of courses
class Professor {
private:
    string courses[50];  // Has courses, not "is" courses
    int courseCount;
};

// Inheritance: Professor is-a Person
class Professor : public Person {
    // Professor has all Person characteristics
};
```



### **6\.6 Protected Members: Balancing Access**



Protected members are accessible to derived classes but not outside code:



```C++
class Person {
protected:
    int id;              // Derived classes can access
    string name;
    
private:
    string ssn;          // Only Person can access
    
public:
    Person(int i, const string& n, const string& s)
        : id(i), name(n), ssn(s) {}
};

class Student : public Person {
public:
    void printId() const {
        cout << id << endl;      // OK: protected
        // cout << ssn;          // ERROR: private!
    }
};

Student s(1001, "Alice", "123-45-6789");
// cout << s.id;  // ERROR: protected, not accessible outside
```



### **Checkpoint 6 \(you should now be able to\)**



1. Draw the construction/destruction order for a 3\-level inheritance chain\.

2. Explain the difference between `public` and `private` inheritance\.

3. When should you prefer composition over inheritance?

4. Write a `TeachingAssistant` class that inherits from `Student` and adds `teachingHours`\.

**\-\-\-**



## **7\. Comprehensive withProf Refactor \(综合项目重构\)**



### **7\.1 Project Requirements**



Let's redesign the `withProf` system using all concepts from this chapter:



**Requirements:**

1. Track professors with IDs, names, and courses

2. Support a department managing multiple professors

3. Use proper initialization and encapsulation

4. Demonstrate object lifetime and arrays

### **7\.2 Class Design**



```C++
// ==================== Person.h ====================
#ifndef PERSON_H
#define PERSON_H

#include <string>
using namespace std;

class Person {
protected:
    int id;
    string name;
    
public:
    Person(int id, const string& name);
    virtual ~Person() = default;  // Virtual for proper cleanup in inheritance
    
    int getId() const { return id; }
    string getName() const { return name; }
    void print() const;
};

#endif

// ==================== Person.cpp ====================
#include "Person.h"
#include <iostream>

Person::Person(int id, const string& name)
    : id(id > 0 ? id : -1)
    , name(name.empty() ? "Unknown" : name)
{
    if (this->id == -1) {
        cout << "Warning: Invalid ID for person\n";
    }
}

void Person::print() const {
    cout << "Person [" << id << "]: " << name << endl;
}

// ==================== Professor.h ====================
#ifndef PROFESSOR_H
#define PROFESSOR_H

#include "Person.h"
#include <string>
using namespace std;

class Professor : public Person {
private:
    string courses[50];
    int courseCount;
    static const int MAX_COURSES = 50;
    
public:
    Professor();
    Professor(int id, const string& name);
    
    void addCourse(const string& courseCode);
    void removeCourse(const string& courseCode);
    int getCourseCount() const { return courseCount; }
    string getCourse(int index) const;
    
    void print() const;  // Overrides Person::print
};

#endif

// ==================== Professor.cpp ====================
#include "Professor.h"
#include <iostream>

Professor::Professor() 
    : Person(0, "Unknown")
    , courseCount(0) 
{
    for (int i = 0; i < MAX_COURSES; i++) {
        courses[i] = "";
    }
}

Professor::Professor(int id, const string& name)
    : Person(id, name)
    , courseCount(0)
{
    for (int i = 0; i < MAX_COURSES; i++) {
        courses[i] = "";
    }
}

void Professor::addCourse(const string& courseCode) {
    if (courseCode.empty() || courseCount >= MAX_COURSES) {
        return;
    }
    
    for (int i = 0; i < courseCount; i++) {
        if (courses[i] == courseCode) {
            cout << "Note: " << getName() << " already teaches " << courseCode << endl;
            return;
        }
    }
    
    courses[courseCount] = courseCode;
    courseCount++;
}

void Professor::removeCourse(const string& courseCode) {
    for (int i = 0; i < courseCount; i++) {
        if (courses[i] == courseCode) {
            for (int j = i; j < courseCount - 1; j++) {
                courses[j] = courses[j + 1];
            }
            courses[courseCount - 1] = "";
            courseCount--;
            return;
        }
    }
}

string Professor::getCourse(int index) const {
    if (index < 0 || index >= courseCount) {
        return "";
    }
    return courses[index];
}

void Professor::print() const {
    cout << "Professor [" << getId() << "]: " << getName() << endl;
    cout << "  Teaching " << courseCount << " course(s):";
    for (int i = 0; i < courseCount; i++) {
        cout << " " << courses[i];
    }
    cout << endl;
}

// ==================== Department.h ====================
#ifndef DEPARTMENT_H
#define DEPARTMENT_H

#include "Professor.h"
#include <string>
using namespace std;

class Department {
private:
    string name;
    Professor faculty[10];  // Fixed-size array of professors
    int facultyCount;
    static const int MAX_FACULTY = 10;
    
public:
    Department(const string& name);
    
    bool addProfessor(int id, const string& name);
    void assignCourseToProfessor(int profIndex, const string& course);
    
    void printRoster() const;
    int getFacultyCount() const { return facultyCount; }
};

#endif

// ==================== Department.cpp ====================
#include "Department.h"
#include <iostream>

Department::Department(const string& name)
    : name(name.empty() ? "Unnamed Department" : name)
    , facultyCount(0)
{
    // faculty array automatically default-constructed
    cout << "Department '" << this->name << "' created\n";
}

bool Department::addProfessor(int id, const string& name) {
    if (facultyCount >= MAX_FACULTY) {
        cout << "Error: Department is at capacity\n";
        return false;
    }
    
    faculty[facultyCount] = Professor(id, name);
    facultyCount++;
    cout << "Added professor to department. Total faculty: " << facultyCount << endl;
    return true;
}

void Department::assignCourseToProfessor(int profIndex, const string& course) {
    if (profIndex < 0 || profIndex >= facultyCount) {
        cout << "Error: Invalid professor index\n";
        return;
    }
    faculty[profIndex].addCourse(course);
}

void Department::printRoster() const {
    cout << "\n=== " << name << " Roster ===\n";
    cout << "Faculty count: " << facultyCount << "/" << MAX_FACULTY << endl;
    for (int i = 0; i < facultyCount; i++) {
        cout << "  " << (i + 1) << ". ";
        faculty[i].print();
    }
    cout << "========================\n";
}

// ==================== main.cpp ====================
#include "Department.h"
#include <iostream>
using namespace std;

// Global department (demonstrates global variable)
Department globalCS("Computer Science");

void demonstrateLocalAndStatic() {
    cout << "\n--- Local vs Static Demo ---\n";
    
    // Local professor - automatic storage
    Professor localProf(2001, "Dr. Local");
    localProf.addCourse("TEMP101");
    localProf.print();
    
    // Static professor - static storage, local scope
    static Professor staticProf(2002, "Dr. Static");
    static int callCount = 0;  // Static local variable
    callCount++;
    
    cout << "Function called " << callCount << " time(s)\n";
    staticProf.addCourse("STATIC" + to_string(callCount));
    staticProf.print();
    
    cout << "--- End of function ---\n";
    // localProf destroyed here, but staticProf lives on!
}

int main() {
    cout << "=== University System Demo ===\n";
    
    // Using global department
    globalCS.addProfessor(1001, "Dr. Smith");
    globalCS.addProfessor(1002, "Dr. Jones");
    globalCS.assignCourseToProfessor(0, "CS101");
    globalCS.assignCourseToProfessor(0, "CS202");
    globalCS.assignCourseToProfessor(1, "MATH101");
    
    // Demonstrate local vs static
    demonstrateLocalAndStatic();
    cout << "\nCalling function again...\n";
    demonstrateLocalAndStatic();
    
    // Create local department
    {
        cout << "\n--- Creating local department ---\n";
        Department localMath("Mathematics");
        localMath.addProfessor(3001, "Dr. LocalMath");
        localMath.printRoster();
        cout << "--- Local department going out of scope ---\n";
    }  // localMath and its faculty destroyed here
    
    // Print final state
    cout << "\n--- Final Global State ---\n";
    globalCS.printRoster();
    
    // Array of professors
    cout << "\n--- Professor Array Demo ---\n";
    Professor researchGroup[3] = {
        Professor(4001, "Researcher A"),
        Professor(4002, "Researcher B"),
        Professor(4003, "Researcher C")
    };
    
    for (int i = 0; i < 3; i++) {
        researchGroup[i].addCourse("RESEARCH" + to_string(i + 1));
        researchGroup[i].print();
    }
    // researchGroup destroyed here when main ends
    
    cout << "\n=== Program Ending ===\n";
    return 0;
    // Global objects destroyed here in reverse creation order
}
```



### **7\.3 Expected Output and Lifetime Observations**



When you run this program, observe:



1\. **Global department** created before \`main\(\)\` starts

2\. **Local professor** created and destroyed each function call

3\. **Static professor** persists between function calls

4\. **Local department** destroyed when leaving its scope

5\. **Array elements** destroyed in reverse order

6\. **Global objects** destroyed after \`main\(\)\` ends



### **Checkpoint 7 \(you should now be able to\)**



1. Explain the lifetime of global vs local vs static variables in this program\.

2. Trace through when each constructor and destructor is called\.

3. Modify the code to add a static member counting total professors\.

4. Create an array of departments instead of a single global one\.

**\-\-\-**



## **8\. High\-Frequency Mistakes Summary**



|Mistake|Why Wrong|Correct Way|
|---|---|---|
|`id = id;` in constructor|Self\-assignment bug|Use init list or `this->id`|
|Forgetting base constructor call|Base part uninitialized|`Derived(...) : Base(...), ... {}`|
|Accessing local variable after scope|Undefined behavior, crashes|Don't return pointers/references to locals|
|Forgetting `static` variable initialization|Linker error|Define `Type Class::member = value;`|
|Array bounds violation|Buffer overflow, crashes|Always check `index < size`|
|Public data members|Breaks encapsulation|Private members \+ getters/setters|
|Missing default constructor for arrays|Compilation error|Provide default constructor|
|Initialization list order confusion|Hard\-to\-find bugs|Match declaration order|
|Confusing scope with lifetime|Logical errors|Scope = visibility, lifetime = existence|
|Throwing from destructor|Program termination|Never throw exceptions from destructors|



**\-\-\-**



## **9\. Practice Exercises**



### **Exercise A: Variable Lifetime Analysis**

Given this code, predict the output order of all constructor/destructor messages:



```C++
class X {
    int id;
public:
    X(int i) : id(i) { cout << "X" << id << " ctor\n"; }
    ~X() { cout << "X" << id << " dtor\n"; }
};

X global(1);

void func() {
    X local(2);
    static X staticLocal(3);
    X arr[2] = {X(4), X(5)};
}

int main() {
    func();
    func();
    return 0;
}
```



**Questions:**

1. In what order are the constructors called on the first `func()` call?

2. In what order are the destructors called when leaving `func()` the first time?

3. How many times is `X3` constructed? Why?

4. What is the complete output sequence?

### **Exercise B: Professor Class Enhancement**

Enhance the `Professor` class with:



1. Add a static member `totalProfessors` that tracks how many Professor objects exist

2. Add a `static int getTotalProfessors()` method

3. Ensure the count is correct when objects are created and destroyed

4. Write a `main()` that demonstrates:

    - Creating professors in different scopes

    - Showing the count changes correctly

### **Exercise C: Department Array Management**

Create a `University` class that:



1. Contains an array of 5 `Department` objects

2. Has methods to add a department at a specific index

3. Has a method to print all departments

4. Demonstrates proper initialization and destruction

**Bonus:** Add bounds checking and prevent duplicate department names\.



### **Exercise D: Access Control Design**

Design a `Course` class with proper encapsulation:



**Private members:**

- `code` \(string\): Course code \(e\.g\., "CS101"\)

- `name` \(string\): Course name

- `capacity` \(int\): Maximum enrollment

- `enrolled` \(int\): Current enrollment

**Public interface:**

- Constructor with validation \(code can't be empty, capacity must be positive\)

- Getters for all fields

- `bool enrollStudent()` \- returns false if at capacity

- `void dropStudent()` \- decreases enrolled count

- `int getAvailableSeats() const`

Write a `main()` that creates a course, attempts enrollments, and demonstrates encapsulation\.



### **Exercise E: Inheritance Chain**

Create a three\-level inheritance hierarchy:



1\. **Person**: Base class with \`id\`, \`name\`

2\. **Employee**: Inherits Person, adds \`salary\`, \`department\`

3\. **Professor**: Inherits Employee, adds \`courses\[\]\`, \`courseCount\`



**Requirements:**

- Each constructor properly calls its parent constructor

- Each class has a `print()` method that reuses parent's `print()`

- Demonstrate construction/destruction order

- Show how `protected` allows derived class access

**\-\-\-**



## **10\. Suggested Answer Outlines**



### **Exercise A Hints**

- Global `X1` constructed before `main()`

- Each `func()` call: `X2` \(local\), `X3` \(static \- only once\!\), `X4`, `X5`

- Destruction: reverse of construction for automatic locals

- Static `X3` destroyed after `main()` ends

### **Exercise B Hints**

```C++
class Professor {
private:
    static int totalProfessors;
public:
    Professor(...) { totalProfessors++; }
    ~Professor() { totalProfessors--; }
    static int getTotal() { return totalProfessors; }
};
int Professor::totalProfessors = 0;
```



### **Exercise C Key Points**

- Array requires default constructor

- Use index tracking for "added" departments

- Bounds check before array access

- Print should handle "empty" slots

### **Exercise D Key Points**

- All setters should validate

- `enrollStudent()` should check `enrolled < capacity`

- Negative counts should be prevented

- Demonstrate in main: try to over\-enroll, verify it fails

### **Exercise E Key Points**

```C++
class Person { /* id, name */ };
class Employee : public Person { 
    Employee(int id, string name, double sal) 
        : Person(id, name), salary(sal) {} 
};
class Professor : public Employee {
    Professor(int id, string name, double sal, string dept)
        : Employee(id, name, sal), ... {}
};
```



**\-\-\-**



## **11\. Chapter Summary**



### **Core Concepts**



**Variable Lifetime and Scope:**

\- **Local variables**: Automatic storage, created on scope entry, destroyed on exit

\- **Global variables**: Static storage, created at program start, destroyed at program end

\- **Static variables**: Static storage duration with local scope \- persist between calls

\- **Scope vs Lifetime**: Scope is where name is visible; lifetime is when object exists



**Constructors and Initialization:**

\- Constructors establish the **beginning of an object's lifetime**

- Initialization lists are preferred for efficiency and required for const/reference members

- Default, parameterized, and copy constructors serve different purposes

- Constructors should validate inputs to maintain object invariants

**Destructors:**

\- Destructors mark the **end of an object's lifetime**

- Called automatically when leaving scope or program end

\- Run in **reverse order** of construction

- Should not throw exceptions or contain complex logic

**Object Arrays:**

- Arrays of objects require default constructors

- All elements share the same lifetime as the array

- Elements destroyed in reverse index order

**Access Control and Encapsulation:**

- `private`: Only within class

- `protected`: Within class and derived classes  

- `public`: Accessible everywhere

- Encapsulation hides internal state, exposes controlled interface

**Inheritance:**

\- **Public inheritance**: Models "is\-a" relationship

\- **Private inheritance**: Models "implemented\-in\-terms\-of"

- Construction order: Base → Members → Derived

- Destruction order: Derived → Members → Base \(reverse\)

### **Design Principles**



1\. **RAII**: Resource Acquisition Is Initialization — acquire resources in constructor, release in destructor

2\. **Encapsulation**: Keep data private, expose behavior through public interfaces

3\. **Prefer composition over inheritance** for "has\-a" relationships

4\. **Initialize everything**: Never leave members in undefined states

5\. **Match lifetime to need**: Use locals for temporary data, statics for persistence, globals sparingly



### **Key Takeaways for withProf System**



- Proper initialization prevents half\-constructed objects

- Static members enable class\-level tracking \(total professors\)

- Object arrays enable managing collections \(faculty roster\)

- Inheritance enables code reuse \(Person → Professor\)

- Access control protects invariants \(private course list\)

- Understanding lifetime prevents use\-after\-free bugs

**\-\-\-**



*End of Chapter 6: Constructors, Destructors, Inheritance, and Object Lifetime*



