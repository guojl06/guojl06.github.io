# Chapter4\_Classes\_and\_Objects\_new

# Chapter 4: Functions, Classes and Objects

## Bilingual Reference Tables

### Table 1: Core Concepts

|Chinese \(中文\)|English|Description|
|---|---|---|
|函数|Function|A reusable block of code that performs a specific task|
|参数|Parameter|Input values a function receives to work with|
|返回值|Return Value|The output a function sends back after completing its task|
|值传递|Pass by Value|Copy of data is passed; changes don't affect the original|
|引用传递|Pass by Reference|Alias to original data; changes affect the original object|
|类|Class|A blueprint or template that defines data and behavior|
|对象|Object|A specific instance created from a class|
|成员变量|Member Variable|Data stored inside a class \(also called data members\)|
|成员函数|Member Function|Functions that operate on the class \(also called methods\)|
|构造函数|Constructor|Special function that initializes an object when it is created|
|封装|Encapsulation|Hiding internal details and exposing only what is needed|
|公有|Public|Accessible from anywhere|
|私有|Private|Accessible only within the class|

### Table 2: Symbols \& Operators

|Symbol|English Name|Chinese \(中文\)|Usage/Meaning|
|---|---|---|---|
|`()`|Parentheses|圆括号|Function call or parameter list|
|`{}`|Curly Braces|花括号|Function body enclosure|
|`return`|Return statement|返回语句|Exits function and optionally sends back a value|
|`void`|Void return type|无返回值|Function returns nothing|
|`&` \(in parameter\)|Reference|引用|Alias for the original; changes affect the original object|
|`class`|class keyword|类关键字|Declares a new class|
|`public:`|public access|公有访问|Members below are accessible from outside|
|`private:`|private access|私有访问|Members below are only visible inside the class|
|`::`|Scope resolution|作用域解析|Links a member to its class \(e\.g\., `Piece::print`\)|
|`.`|Member access|成员访问|Access a member of an object \(e\.g\., `pawn.row`\)|
|`const`|Constant qualifier|常量限定|After a function: this function does not modify the object|

### Table 3: Chapter\-Specific Terms

|English|Chinese \(中文\)|Explanation|
|---|---|---|
|Function Signature|函数签名|The function name plus its parameter types \(used for overloading\)|
|Function Overloading|函数重载|Multiple functions with the same name but different parameters|
|Blueprint|蓝图|A class is like a blueprint—it describes what an object will have, but you need to create actual objects|
|Instance|实例|One specific object created from a class|
|Method|方法|Another name for member function|
|Data member|数据成员|Another name for member variable|
|enum|枚举|Defines a set of named constants \(e\.g\., PAWN, KNIGHT\)|
|Header file|头文件|`.h` file that declares a class \(interface\)|
|Source file|源文件|`.cpp` file that implements member functions|

---

## Prerequisites

Before this chapter, you should know:

- Variables, data types, and basic operators

- Basic control flow \(if, loops\)

- Arrays and basic array operations

**Connection to next chapter**: After mastering functions and classes, you will learn about inheritance \(reusing and extending classes\) and polymorphism\.

---

## 1\. Functions — The Building Blocks of Code

### The Problem: Repeating Code Everywhere

> **Opening Question**: Imagine you need to calculate the area of 10 different rectangles in your program\. Would you write the same formula 10 times?

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YjMyNDdmNGE4ZTJiZDJkNGFkYjAyYmY1N2MwZWViODVfM2U0OTg5OWM5NWY2NWI1MTEzOTY3MDg1MDZmMjc2MTNfSUQ6NzYyMTA1MDQ4MjUxMzEyMDIwMF8xNzgxMDYwNjQ5OjE3ODExNDcwNDlfVjM)

### Step 1: The Naive Approach

Without functions, you would copy\-paste the same logic everywhere:

```C++
#include <iostream>
using namespace std;

int main() {
    // Rectangle 1
    int width1 = 5, height1 = 3;
    int area1 = width1 * height1;
    cout << "Area 1: " << area1 << endl;
    
    // Rectangle 2
    int width2 = 4, height2 = 6;
    int area2 = width2 * height2;
    cout << "Area 2: " << area2 << endl;
    
    // Rectangle 3... and so on
    // This is repetitive and error-prone!
    
    return 0;
}
```

**Problems with this approach**:

1. **Code duplication** — Same logic repeated many times

2. **Hard to maintain** — If the formula changes, update everywhere

3. **Error\-prone** — Easy to make mistakes when copying

4. **Hard to read** — Main logic gets buried in details

### Step 2: Exploring the Problem

> **Exploration Questions**:

- What if the area formula needs to change \(e\.g\., add validation\)?

- How do we make the code more organized and reusable?

- Can we give a name to a block of code and "call" it when needed?

### Step 3: The Solution — Functions

> A **function** is a named block of code that performs a specific task\. You define it once, then call it whenever you need that task\.

**Syntax**:

```C++
returnType functionName(parameterList) { functionBody }
```

|Part|Meaning|Example|
|---|---|---|
|`returnType`|Return type — what the function sends back|`int`|
|`functionName`|Function name — how you call it|`add`|
|`parameterList`|Parameters — inputs the function receives|`(int a, int b)`|
|`functionBody`|Function body — the work being done|`{ int sum = a + b; return sum; }`|

### Example 1: Minimal \(Single Concept\)

```C++
#include <iostream>
using namespace std;

// Function definition
// returnType functionName(parameterList) { functionBody }
int add(int a, int b) {
    int sum = a + b;
    return sum;  // Send the result back
}

int main() {
    // Function calls
    int result1 = add(3, 5);   // result1 = 8
    int result2 = add(10, 20); // result2 = 30
    
    cout << "3 + 5 = " << result1 << endl;
    cout << "10 + 20 = " << result2 << endl;
    
    return 0;
}
```

**Output**:

```Plaintext
3 + 5 = 8
10 + 20 = 30
```

**Key Parts of a Function**:

```C++
int add(int a, int b)  // Function header: return type, name, parameters
{                      // Opening brace
    int sum = a + b;   // Function body: the work being done
    return sum;        // Return statement: send result back
}                      // Closing brace
```

|Part|Meaning|Example|
|---|---|---|
|`int`|Return type — what the function sends back|Function returns an integer|
|`add`|Function name — how you call it|Call with `add(3, 5)`|
|`(int a, int b)`|Parameters — inputs the function receives|`a=3`, `b=5` when called|
|`return sum`|Return statement — exits and sends value back|Returns 8|

### Example 2: Void Functions \(No Return Value\)

Not all functions need to return a value\. Use `void` when the function just performs an action:

```C++
#include <iostream>
using namespace std;

// void means "returns nothing"
void printGreeting(string name) {
    cout << "Hello, " << name << "! Welcome to C++." << endl;
    // No return statement needed
}

void printSeparator() {
    cout << "------------------------" << endl;
}

int main() {
    printGreeting("Alice");
    printSeparator();
    printGreeting("Bob");
    printSeparator();
    
    return 0;
}
```

**Output**:

```Plaintext
Hello, Alice! Welcome to C++.
------------------------
Hello, Bob! Welcome to C++.
------------------------
```

### Example 3: Rectangle Area with Validation

A more practical example with error checking:

```C++
#include <iostream>
using namespace std;

// Calculate rectangle area with validation
int calculateArea(int width, int height) {
    // Validate inputs
    if (width < 0 || height < 0) {
        cout << "Error: Dimensions cannot be negative!" << endl;
        return -1;  // Return error code
    }
    
    return width * height;
}

// Display area with formatting
void displayArea(int width, int height, int area) {
    cout << "Rectangle " << width << " x " << height 
         << " has area: " << area << endl;
}

int main() {
    // Test with valid dimensions
    int w1 = 5, h1 = 3;
    int area1 = calculateArea(w1, h1);
    if (area1 >= 0) {
        displayArea(w1, h1, area1);
    }
    
    // Test with invalid dimensions
    int w2 = -4, h2 = 6;
    int area2 = calculateArea(w2, h2);
    // This will show error message
    
    return 0;
}
```

**Output**:

```Plaintext
Rectangle 5 x 3 has area: 15
Error: Dimensions cannot be negative!
```

### Step 4: Practice

#### Try It Yourself 1: Function with Validation

Write a function `bool isPositive(int number)` that returns `true` if the number is positive, `false` otherwise\. Use it in `main()` to check several numbers\.

---

## 2\. Function Parameters — Passing Data In

### The Problem: Different Ways to Share Data

> **Opening Question**: When you pass a variable to a function, should the function work with a copy of the value, or should it be able to modify the original?

### Step 1: Pass by Value \(The Default\)

By default, C\+\+ passes **a copy** of the data\. Changes inside the function don't affect the original:

```C++
#include <iostream>
using namespace std;

void tryToChange(int x) {
    x = 100;  // This only changes the local copy
    cout << "Inside function: x = " << x << endl;
}

int main() {
    int a = 5;
    cout << "Before: a = " << a << endl;
    
    tryToChange(a);
    
    cout << "After: a = " << a << endl;  // Still 5!
    return 0;
}
```

**Output**:

```Plaintext
Before: a = 5
Inside function: x = 100
After: a = 5
```

**Why?** The function receives a **copy** of `a`\. Modifying `x` doesn't touch the original `a`\.

### Step 2: Pass by Reference \(Using `&`\)

Use `&` to pass the **original variable itself** \(an alias\)\. Changes affect the original:

```C++
#include <iostream>
using namespace std;

void actuallyChange(int& x) {  // & means "reference to"
    x = 100;  // This changes the original!
    cout << "Inside function: x = " << x << endl;
}

int main() {
    int a = 5;
    cout << "Before: a = " << a << endl;
    
    actuallyChange(a);
    
    cout << "After: a = " << a << endl;  // Now 100!
    return 0;
}
```

**Output**:

```Plaintext
Before: a = 5
Inside function: x = 100
After: a = 100
```

**Why?** The function receives a **reference** \(alias\) to `a`\. Modifying `x` actually modifies `a`\.

### Step 3: Comparing Value vs Reference

|Aspect|Pass by Value|Pass by Reference|
|---|---|---|
|Syntax|`int x`|`int& x`|
|What is passed|Copy of data|Original variable|
|Function can modify original?|No|Yes|
|Use when|Input data shouldn't change|Need to modify original or large data|

### Example 1: Minimal \(Swap Function\)

A classic example showing the difference:

```C++
#include <iostream>
using namespace std;

// WRONG: Pass by value - won't work
void badSwap(int a, int b) {
    int temp = a;
    a = b;
    b = temp;
    // Local copies are swapped, originals unchanged
}

// CORRECT: Pass by reference
void goodSwap(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
    // Originals are swapped!
}

int main() {
    int x = 5, y = 10;
    
    cout << "Before: x = " << x << ", y = " << y << endl;
    
    badSwap(x, y);
    cout << "After badSwap: x = " << x << ", y = " << y << endl;
    
    goodSwap(x, y);
    cout << "After goodSwap: x = " << x << ", y = " << y << endl;
    
    return 0;
}
```

**Output**:

```Plaintext
Before: x = 5, y = 10
After badSwap: x = 5, y = 10
After goodSwap: x = 10, y = 5
```

### Example 2: Multiple Outputs via Reference

Functions can only return one value directly\. Use references to "return" multiple values:

```C++
#include <iostream>
using namespace std;

// Calculate both area and perimeter
void calculateRectangle(int width, int height, 
                        int& area, int& perimeter) {
    area = width * height;
    perimeter = 2 * (width + height);
}

int main() {
    int w = 5, h = 3;
    int myArea, myPerimeter;
    
    // Pass w, h by value (inputs)
    // Pass myArea, myPerimeter by reference (outputs)
    calculateRectangle(w, h, myArea, myPerimeter);
    
    cout << "Rectangle " << w << " x " << h << endl;
    cout << "Area: " << myArea << endl;
    cout << "Perimeter: " << myPerimeter << endl;
    
    return 0;
}
```

**Output**:

```Plaintext
Rectangle 5 x 3
Area: 15
Perimeter: 16
```

### Step 4: Practice

#### Try It Yourself 2\.1: Pass by Value

Write a function `void doubleValue(int x)` that sets `x = x * 2`\. Show that the original variable in `main()` doesn't change\.

#### Try It Yourself 2\.2: Pass by Reference

Write a function `void doubleIt(int& x)` that actually doubles the original variable\. Show that it works\.

#### Try It Yourself 2\.3: Multiple Outputs

Write a function `void getMinMax(int a, int b, int& min, int& max)` that sets `min` to the smaller value and `max` to the larger value\.

---

## 3\. Function Overloading — Same Name, Different Parameters

### The Problem: Too Many Similar Function Names

> **Opening Question**: What if you want a `print` function that works for integers, doubles, and strings? Do you need `printInt`, `printDouble`, `printString`?

### Step 1: The Naive Approach

Without overloading, you create multiple functions with different names:

```C++
void printInt(int x) { cout << "Integer: " << x << endl; }
void printDouble(double x) { cout << "Double: " << x << endl; }
void printString(string x) { cout << "String: " << x << endl; }

// Usage - must remember which name to use!
printInt(42);
printDouble(3.14);
printString("Hello");
```

**Problems**:

1. Must remember multiple function names

2. Code is less intuitive

3. Hard to extend

### Step 2: The Solution — Function Overloading

> **The "Aha" Moment**: C\+\+ lets you define multiple functions with the **same name** as long as their **parameter lists are different**\. The compiler picks the right one based on the arguments\.

### Syntax and Rules

```C++
// All named "print", but different parameters
void print(int x);        // Takes an int
void print(double x);     // Takes a double  
void print(string x);     // Takes a string
void print(int x, int y); // Takes two ints (different count)
```

**Rules for valid overloading**:

- Parameter **types** must differ, OR

- Parameter **count** must differ, OR

- Parameter **order** must differ \(for mixed types\)

**Not allowed**: Only return type differs

```C++
// ERROR: Cannot overload on return type alone
int getValue();
double getValue();  // Compile error!
```

### Example 1: Minimal \(Basic Overloading\)

```C++
#include <iostream>
#include <string>
using namespace std;

// Three functions, all named "print"
void print(int x) {
    cout << "Integer: " << x << endl;
}

void print(double x) {
    cout << "Double: " << x << endl;
}

void print(string x) {
    cout << "String: \"" << x << "\"" << endl;
}

int main() {
    print(42);        // Calls print(int)
    print(3.14);      // Calls print(double)
    print("Hello");   // Calls print(string)
    
    return 0;
}
```

**Output**:

```Plaintext
Integer: 42
Double: 3.14
String: "Hello"
```

### Example 2: Area Calculations

Real\-world example: calculating areas of different shapes:

```C++
#include <iostream>
using namespace std;

// Rectangle area
int area(int width, int height) {
    cout << "Rectangle: ";
    return width * height;
}

// Square area (overload by parameter count)
int area(int side) {
    cout << "Square: ";
    return side * side;
}

// Circle area (overload by parameter type)
double area(double radius) {
    cout << "Circle: ";
    return 3.14159 * radius * radius;
}

int main() {
    cout << area(5, 3) << endl;      // Rectangle: 15
    cout << area(4) << endl;          // Square: 16
    cout << area(2.5) << endl;        // Circle: 19.635
    
    return 0;
}
```

**Output**:

```Plaintext
Rectangle: 15
Square: 16
Circle: 19.635
```

### Step 3: Practice

#### Try It Yourself 3\.1: Basic Overloading

Write overloaded `display` functions:

- `void display(int x)` — prints "Integer: \[value\]"

- `void display(double x)` — prints "Double: \[value\]"

- `void display(char x)` — prints "Character: \[value\]"

#### Try It Yourself 3\.2: Max Function

Write overloaded `max` functions:

- `int max(int a, int b)` — returns larger of two ints

- `int max(int a, int b, int c)` — returns largest of three ints

#### Try It Yourself 3\.3: Calculate

Write overloaded `calculate` functions:

- `int calculate(int a, int b)` — returns a \+ b

- `double calculate(double a, double b)` — returns a \* b

---

## 4\. Separating Declaration and Definition

### The Problem: Organizing Large Programs

> **Opening Question**: As programs grow, how do we organize code so that the main logic is readable, and implementation details don't clutter it?

### Step 1: Declaration vs Definition

In C\+\+, a function has two parts:

- **Declaration** \(prototype\): Tells the compiler "this function exists"

- **Definition**: The actual implementation

```C++
// Declaration (ends with semicolon)
int add(int a, int b);

// Definition (has body)
int add(int a, int b) {
    return a + b;
}
```

### Step 2: Why Separate Them?

1. **Organization**: Main file shows "what" functions exist; separate file shows "how" they work

2. **Compilation**: Compiler only needs declarations to validate calls

3. **Reusability**: Other files can include just the declarations

### Example 1: Minimal \(Single File Separation\)

```C++
#include <iostream>
using namespace std;

// Declarations first (function prototypes)
int add(int a, int b);
int multiply(int a, int b);

// Main function - clean and readable
int main() {
    int x = 5, y = 3;
    
    cout << "Add: " << add(x, y) << endl;
    cout << "Multiply: " << multiply(x, y) << endl;
    
    return 0;
}

// Definitions after main (or in separate file)
int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}
```

### Example 2: Multi\-File Structure

As projects grow, split into header and source files:

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MGQxZTBmNTlmNjViOWQ4MWZkODU1YTUxZGY4MDc3ODlfNTU1MDU3ZjFkZThiNzcxODM3Y2IwZTQ0NTgwZGIwNzFfSUQ6NzYyMTA1MDgxMjM1NzQ2MzIyOV8xNzgxMDYwNjQ5OjE3ODExNDcwNDlfVjM)

**Visual Overview:**

```Plaintext
Project/
├── math_utils.h      <-- Declarations (interface)
├── math_utils.cpp    <-- Implementation
└── main.cpp          <-- Usage
```

**math\_utils\.h** \(declarations\)

```C++
#ifndef MATH_UTILS_H
#define MATH_UTILS_H

// Function declarations only
int add(int a, int b);
int subtract(int a, int b);
int multiply(int a, int b);
double divide(int a, int b);

#endif
```

**math\_utils\.cpp** \(definitions\)

```C++
#include "math_utils.h"

int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int multiply(int a, int b) {
    return a * b;
}

double divide(int a, int b) {
    if (b == 0) return 0;  // Simple error handling
    return static_cast<double>(a) / b;
}
```

**main\.cpp** \(uses the functions\)

```C++
#include <iostream>
#include "math_utils.h"
using namespace std;

int main() {
    cout << "10 + 5 = " << add(10, 5) << endl;
    cout << "10 - 5 = " << subtract(10, 5) << endl;
    cout << "10 * 5 = " << multiply(10, 5) << endl;
    cout << "10 / 5 = " << divide(10, 5) << endl;
    
    return 0;
}
```

### Step 3: Practice

#### Try It Yourself 4: Separate in Multiple Files

Implement the previous example in multiple files\.
try the effect of removing the header file and see what happens\.
try the effect of removing the guard of the header file and see what happens\. Delete \#ifndef and \#define and see what happens\. What if we include the header file twice in the same file?
Try \#pragma once and see what happens\.

---

## 5\. Classes and Objects — From Design to Code

### 5\.1 The Philosophy: Why We Need Classes

> **The Problem**: Imagine you're building a university course management system\. You need to track students \(with ID, name, major, GPA\) and courses \(with code, title, credits, enrolled students\)\. How do you organize this data in code?

#### The Naive Approach \(Without Classes\)

```C++
// For students - parallel arrays (hard to maintain!)
int studentIDs[1000];
string studentNames[1000];
string studentMajors[1000];
double studentGPAs[1000];

// For courses - more parallel arrays
string courseCodes[100];
string courseTitles[100];
int courseCredits[100];
int courseEnrollments[100][50];  // Which students are enrolled?

// Problems:
// 1. No connection between studentIDs[0] and studentNames[0]
// 2. Easy to get indices mixed up
// 3. Adding a field (e.g., student email) requires changing ALL arrays
// 4. Functions need to pass entire arrays: void printStudent(int index)
```

**The Core Insight**: Data that belongs together should STAY together\.

#### The Class\-Based Solution

A **class** bundles related data into a single unit\. Think of it like a real\-world form:

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OGU0OWYxNmFjNmViMTQxYzcyZmE2YmI0Yzg5YjIxMGRfMDZkZmFlMDI4NDY1N2JiODczMTVkYThjM2I4OWI1MTNfSUQ6NzYyMTA1MTEwNjQwNzQxODgxOF8xNzgxMDYwNjQ5OjE3ODExNDcwNDlfVjM)

**Analogy:**

- **Blank form \(Class\)**: Has fields for name, ID, major\.\.\. but no values yet

- **Filled form \(Object\)**: Has specific values: "Alice", "1001", "Computer Science", 3\.8

**Key Insight:** One class can create many objects, just like one blueprint can build many houses\.

---

### 5\.2 Class Syntax Deep Dive

#### 5\.2\.1 Basic Class Definition

```C++
// ============================================
// CLASS DEFINITION SYNTAX
// ============================================
// class ClassName {
//     access_specifier:
//         member_declarations;
// };
//
// CRITICAL: Don't forget the semicolon after the closing brace!

class Student {
public:                      // Everything after this is publicly accessible
    int id;                 // Member variable (each object gets its own copy)
    string name;            // Member variable
    string major;           // Member variable
    double gpa;             // Member variable
};                          // <-- SEMICOLON IS REQUIRED!
```

**Syntax Components Explained:**

|Component|Purpose|Notes|
|---|---|---|
|`class`|Keyword to declare a class|Must be lowercase|
|`Student`|Class name|Should be descriptive, typically PascalCase|
|`{ }`|Encloses class body|All members go inside|
|`public:`|Access specifier|Members are accessible from outside|
|`int id;`|Member variable declaration|Like a regular variable, but belongs to the class|
|`;`|End of class definition|**FORGETTING THIS IS A COMMON ERROR\!**|

**⚠️ Common Error \#1: Missing Semicolon**

```C++
class Student {
    int id;
    string name;
}                           // ERROR! Missing semicolon

int main() { ... }            // Compiler error here (confusing!)
```

#### 5\.2\.2 Creating Objects

```C++
// ============================================
// OBJECT CREATION SYNTAX
// ============================================

int main() {
    // Method 1: Simple declaration
    // Syntax: ClassName objectName;
    Student alice;              // Creates one Student object
                                // alice now has: alice.id, alice.name, etc.
    
    // Method 2: Array of objects
    Student students[30];       // Creates 30 Student objects
                                // Access: students[0].name, students[1].gpa, etc.
    
    // Method 3: Pointer (advanced)
    Student* ptr = &alice;      // ptr points to alice
    ptr->gpa = 3.8;             // Access via pointer (use -> not .)
    
    return 0;
}
```

**⚠️ Common Error \#2: Wrong Object Creation Syntax**

```C++
Student alice();    // WRONG! This declares a FUNCTION, not an object
                    // The compiler thinks you're declaring:
                    // "A function named alice that takes no parameters
                    //  and returns a Student"
                    
Student alice;      // CORRECT! Creates a Student object named alice
Student bob(1001);  // CORRECT (if constructor exists)
```

#### 5\.2\.3 Accessing Members

```C++
// ============================================
// MEMBER ACCESS SYNTAX
// ============================================
// objectName.memberName

int main() {
    Student alice;              // Create object
    
    // Setting values (write access)
    alice.id = 1001;            // Dot operator (.) accesses member
    alice.name = "Alice Chen";   // Can assign strings to string members
    alice.major = "Computer Science";
    alice.gpa = 3.85;
    
    // Reading values (read access)
    cout << "Student: " << alice.name << endl;
    cout << "GPA: " << alice.gpa << endl;
    
    return 0;
}
```

**The Dot Operator \(\.\)**: Think of it as "possessive" — `alice.gpa` means "alice's gpa"

---

#### 5\.2\.4 Object Initialization

When you create an object, its member variables start with **garbage values** \(whatever was in memory\)\. You should always initialize them before use\.

```C++
// ============================================
// INITIALIZATION METHODS
// ============================================

int main() {
    // Method 1: Initialize immediately after creation
    Student alice;
    alice.id = 1001;
    alice.name = "Alice Chen";
    alice.major = "Computer Science";
    alice.gpa = 3.85;
    
    // Method 2: Use a helper function for initialization
    Student bob;
    initializeStudent(bob, 1002, "Bob Smith", "Mathematics", 3.2);
    
    // Method 3: Create an initialization member function (best practice)
    Student carol;
    carol.initialize(1003, "Carol White", "Physics", 3.9);
    
    return 0;
}

// Helper function (standalone)
void initializeStudent(Student& s, int id, string name, 
                       string major, double gpa) {
    s.id = id;
    s.name = name;
    s.major = major;
    s.gpa = gpa;
}
```

**⚠️ Danger: Uninitialized Variables**

```C++
Student alice;      // Member variables contain garbage values!
cout << alice.gpa;  // Dangerous! Could print any random number

// CORRECT: Always initialize before using
alice.id = 1001;
alice.gpa = 3.85;
cout << alice.gpa;  // Safe: prints 3.85
```

---

#### 5\.2\.5 Encapsulation with Getters and Setters

Currently, all our member variables are `public`, meaning anyone can change them directly\. This is risky — what if someone sets a negative GPA?

```C++
Student alice;
alice.gpa = -5.0;   // Allowed, but makes no sense!
alice.id = -999;    // ID should be positive
```

**The Solution: Controlled Access via Functions**

Instead of direct access, we provide **getter** \(read\) and **setter** \(write\) functions:

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NTM4MDAxZTQ3ZTIzNTAwM2JlMTRhMDNmNTcxZjk3OTNfMWNkYzFjYWNiMGNjMzRiZDVjMmQxM2JkZmJjOWVlM2ZfSUQ6NzYyMTA1MTY1MTgwNTI1MjU2OF8xNzgxMDYwNjQ5OjE3ODExNDcwNDlfVjM)

**How It Works:**

- Private data is "hidden" inside the class

- Public functions act as controlled entry points

- Setters validate data before changing it

- Getters provide safe read access

```C++
// ============================================
// ENCAPSULATION PATTERN: Private Data + Public Interface
// ============================================

class Student {
private:                     // Private: only accessible inside the class
    int id;
    double gpa;
    
public:                      // Public: accessible from outside
    string name;             // Can leave some fields public if needed
    string major;
    
    // SETTERS (set values with validation)
    void setId(int newId) {
        if (newId > 0) {
            id = newId;
        } else {
            cout << "Error: ID must be positive!" << endl;
            id = 0;  // Default safe value
        }
    }
    
    void setGpa(double newGpa) {
        if (newGpa >= 0.0 && newGpa <= 4.0) {
            gpa = newGpa;
        } else {
            cout << "Error: GPA must be between 0.0 and 4.0!" << endl;
            gpa = 0.0;  // Default safe value
        }
    }
    
    // GETTERS (read values)
    int getId() const {
        return id;           // Returns the private id
    }
    
    double getGpa() const {
        return gpa;          // Returns the private gpa
    }
    
    // INITIALIZATION FUNCTION
    void initialize(int newId, string newName, 
                    string newMajor, double newGpa) {
        setId(newId);        // Use setter for validation
        name = newName;      // Direct assignment for public members
        major = newMajor;
        setGpa(newGpa);      // Use setter for validation
    }
};
```

**Using the Encapsulated Class:**

```C++
int main() {
    Student alice;
    
    // Use setters for private members
    alice.setId(1001);              // Valid ID, accepted
    alice.setGpa(3.85);             // Valid GPA, accepted
    alice.setGpa(5.0);              // Invalid! Error message printed
    
    // Use getters to read private members
    cout << "ID: " << alice.getId() << endl;
    cout << "GPA: " << alice.getGpa() << endl;
    
    // Direct access for public members
    alice.name = "Alice Chen";      // OK: name is public
    alice.major = "Computer Science"; // OK: major is public
    
    // Use initialization function for convenience
    Student bob;
    bob.initialize(1002, "Bob Smith", "Mathematics", 3.2);
    
    return 0;
}
```

**Benefits of Getters and Setters:**

|Benefit|Explanation|
|---|---|
|**Validation**|Setters can check if values are valid|
|**Read\-only**|Provide getter without setter = read\-only access|
|**Controlled write**|Setter can limit when/how values change|
|**Flexibility**|Can change internal representation without breaking code|

**Syntax Summary:**

```C++
class ClassName {
private:
    type privateVar;              // Hidden data
    
public:
    // Setter pattern
    void setVarName(type value) {
        // Validate and set
        privateVar = value;
    }
    
    // Getter pattern (const = doesn't modify object)
    type getVarName() const {
        return privateVar;
    }
};
```

---

### 5\.3 Complete Example: Student and Course System

Let's build a realistic example with both Student and Course classes\.

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZWI1YmY4OGZlODJlZGJiOWZhN2IwYmJhNTYxYTAwZTRfOGM5ZWQ0NzY0MDcxYzhmMzQwMDQ4YmIyYWY4YTVmMjdfSUQ6NzYyMTA1MTQ3ODQ2MzE1NTE0NV8xNzgxMDYwNjQ5OjE3ODExNDcwNDlfVjM)

#### Step 1: Design the Classes

**Student Class Design:**

- Data needed: ID, name, major, GPA

- Operations needed: Print info, Check if honor student \(GPA \>= 3\.5\)

**Course Class Design:**

- Data needed: Course code, title, credits, enrolled students, max capacity

- Operations needed: Print info, Enroll student, Check if full

#### Step 2: Header File — student\.h

```C++
// ============================================
// FILE: student.h
// PURPOSE: Declares the Student class interface
// This is like a contract — it tells other files what Student can do
// ============================================

#ifndef STUDENT_H        // Header guard: prevents double inclusion
#define STUDENT_H

#include <string>
using namespace std;

// ============================================
// STUDENT CLASS DECLARATION
// ============================================
class Student {
public:
    // ----------------------------------------
    // MEMBER VARIABLES (Data)
    // Each Student object gets its own copy of these
    // ----------------------------------------
    int id;                 // Student ID number
    string name;            // Full name
    string major;           // Field of study
    double gpa;             // Grade point average
    
    // ----------------------------------------
    // MEMBER FUNCTIONS (Behavior)
    // These operate on a specific Student object's data
    // ----------------------------------------
    
    // Print all student information
    // 'const' means this function promises NOT to modify the object
    void print() const;
    
    // Check if student is on honor roll (GPA >= 3.5)
    bool isHonorStudent() const;
    
    // Get academic standing: "Excellent", "Good", "Warning"
    string getStanding() const;
};

#endif // STUDENT_H
```

**Key Concepts in the Header:**

1. **Header Guard \(****`#ifndef`**** / ****`#define`**** / ****`#endif`****\)**:

    - Prevents the same code from being processed twice

    - Without it: "redefinition of class Student" error

    - Naming convention: `FILENAME_H` \(uppercase, underscores\)

2. **`const`**** after function**:

    - Promise: "I will not modify any member variables"

    - Allows calling these functions on `const` objects

    - Good practice for "getter" functions

#### Step 3: Implementation File — student\.cpp

```C++
// ============================================
// FILE: student.cpp
// PURPOSE: Implements the Student class functions
// Defines HOW each function works
// ============================================

#include "student.h"      // Include the declaration (must match exactly!)
#include <iostream>
using namespace std;

// ============================================
// MEMBER FUNCTION IMPLEMENTATIONS
// Syntax: ReturnType ClassName::FunctionName(parameters) { body }
// The :: is the "scope resolution operator" - it says "this belongs to Student"
// ============================================

// Print all student information
void Student::print() const {
    cout << "ID: " << id << endl;
    cout << "Name: " << name << endl;
    cout << "Major: " << major << endl;
    cout << "GPA: " << gpa << endl;
}

// Check if honor student (GPA >= 3.5)
bool Student::isHonorStudent() const {
    return gpa >= 3.5;    // Simple comparison, returns true or false
}

// Get academic standing based on GPA
string Student::getStanding() const {
    if (gpa >= 3.5) {
        return "Excellent";
    } else if (gpa >= 3.0) {
        return "Good";
    } else if (gpa >= 2.0) {
        return "Satisfactory";
    } else {
        return "Warning";
    }
}
```

**⚠️ Common Error \#3: Missing Scope Resolution Operator**

```C++
// WRONG: This creates a global function, not a member function
void print() const {
    cout << id << endl;     // ERROR: 'id' is not defined in this scope
}

// CORRECT: The :: links the function to the Student class
void Student::print() const {
    cout << id << endl;     // OK: 'id' refers to this object's id
}
```

**⚠️ Common Error \#4: Forgetting \#include**

```C++
// WRONG in student.cpp
void Student::print() const {
    cout << name << endl;   // ERROR: 'cout' and 'name' not recognized
}

// CORRECT
#include "student.h"      // Brings in string and other definitions
#include <iostream>       // Brings in cout
using namespace std;
```

#### Step 4: Using the Class — main\.cpp

```C++
// ============================================
// FILE: main.cpp
// PURPOSE: Demonstrates using the Student class
// ============================================

#include <iostream>
#include "student.h"      // Use quotes ("") for your own headers
using namespace std;

int main() {
    cout << "=== Student Management System Demo ===" << endl;
    
    // ----------------------------------------
    // Create and set up individual students
    // ----------------------------------------
    Student alice;              // Create first student object
    alice.id = 1001;
    alice.name = "Alice Chen";
    alice.major = "Computer Science";
    alice.gpa = 3.85;
    
    Student bob;                // Create second student object
    bob.id = 1002;
    bob.name = "Bob Smith";
    bob.major = "Mathematics";
    bob.gpa = 3.2;
    
    // ----------------------------------------
    // Use member functions
    // ----------------------------------------
    cout << "\n--- Alice's Information ---" << endl;
    alice.print();                              // Call print function
    cout << "Honor Student: " 
         << (alice.isHonorStudent() ? "Yes" : "No") << endl;
    cout << "Standing: " << alice.getStanding() << endl;
    
    cout << "\n--- Bob's Information ---" << endl;
    bob.print();
    cout << "Honor Student: " 
         << (bob.isHonorStudent() ? "Yes" : "No") << endl;
    cout << "Standing: " << bob.getStanding() << endl;
    
    // ----------------------------------------
    // Create an array of students
    // ----------------------------------------
    cout << "\n--- Class Roster ---" << endl;
    Student cs101[3];           // Array of 3 students
    
    // Initialize first student in array
    cs101[0].id = 2001;
    cs101[0].name = "Carol White";
    cs101[0].major = "Computer Science";
    cs101[0].gpa = 3.9;
    
    // Initialize second student
    cs101[1].id = 2002;
    cs101[1].name = "David Lee";
    cs101[1].major = "Computer Science";
    cs101[1].gpa = 2.8;
    
    // Initialize third student
    cs101[2].id = 2003;
    cs101[2].name = "Eva Brown";
    cs101[2].major = "Computer Science";
    cs101[2].gpa = 3.5;
    
    // Print all students in class
    for (int i = 0; i < 3; i++) {
        cout << "\nStudent " << (i + 1) << ":" << endl;
        cs101[i].print();
    }
    
    return 0;
}
```

**Expected Output:**

```Plaintext
=== Student Management System Demo ===

--- Alice's Information ---
ID: 1001
Name: Alice Chen
Major: Computer Science
GPA: 3.85
Honor Student: Yes
Standing: Excellent

--- Bob's Information ---
Major: Mathematics
GPA: 3.2
Honor Student: No
Standing: Good

--- Class Roster ---

Student 1:
ID: 2001
Name: Carol White
Major: Computer Science
GPA: 3.9

Student 2:
ID: 2002
Name: David Lee
Major: Computer Science
GPA: 2.8

Student 3:
ID: 2003
Name: Eva Brown
Major: Computer Science
GPA: 3.5
```

### 5\.4 The Course Class — Adding Relationships

Now let's create a Course class that can enroll students\.

#### course\.h

```C++
#ifndef COURSE_H
#define COURSE_H

#include <string>
#include "student.h"      // Need to know about Student class
using namespace std;

// ============================================
// COURSE CLASS DECLARATION
// ============================================
class Course {
public:
    // ----------------------------------------
    // MEMBER VARIABLES
    // ----------------------------------------
    string code;            // Course code (e.g., "CS101")
    string title;           // Course title (e.g., "Introduction to Programming")
    int credits;            // Credit hours
    int capacity;           // Maximum enrollment
    
    // Array of enrolled students (store student IDs)
    int enrolledStudents[50];  // Fixed-size array
    int enrollmentCount;       // Current number of enrolled students
    
    // ----------------------------------------
    // MEMBER FUNCTIONS
    // ----------------------------------------
    
    // Initialize course (like a setup function)
    void initialize(string c, string t, int cred, int cap);
    
    // Try to enroll a student (by ID)
    // Returns true if successful, false if course is full
    bool enrollStudent(int studentID);
    
    // Print course information
    void print() const;
    
    // Check if course is full
    bool isFull() const;
    
    // Get number of available seats
    int getAvailableSeats() const;
};

#endif // COURSE_H
```

#### course\.cpp

```C++
#include "course.h"
#include <iostream>
using namespace std;

// Initialize all course data
void Course::initialize(string c, string t, int cred, int cap) {
    code = c;
    title = t;
    credits = cred;
    capacity = cap;
    enrollmentCount = 0;    // Start with no students enrolled
    
    // Initialize all array elements to 0 (good practice)
    for (int i = 0; i < 50; i++) {
        enrolledStudents[i] = 0;
    }
}

// Try to enroll a student
bool Course::enrollStudent(int studentID) {
    // Check if course is full
    if (enrollmentCount >= capacity) {
        cout << "Error: Course " << code << " is full!" << endl;
        return false;
    }
    
    // Check if student already enrolled
    for (int i = 0; i < enrollmentCount; i++) {
        if (enrolledStudents[i] == studentID) {
            cout << "Error: Student " << studentID 
                 << " is already enrolled in " << code << endl;
            return false;
        }
    }
    
    // Add student to array
    enrolledStudents[enrollmentCount] = studentID;
    enrollmentCount++;
    
    cout << "Success: Student " << studentID 
         << " enrolled in " << code << endl;
    return true;
}

// Print course information
void Course::print() const {
    cout << code << ": " << title << endl;
    cout << "Credits: " << credits << endl;
    cout << "Enrollment: " << enrollmentCount << "/" << capacity << endl;
    
    if (enrollmentCount > 0) {
        cout << "Enrolled Students: ";
        for (int i = 0; i < enrollmentCount; i++) {
            cout << enrolledStudents[i];
            if (i < enrollmentCount - 1) {
                cout << ", ";
            }
        }
        cout << endl;
    }
}

// Check if course is full
bool Course::isFull() const {
    return enrollmentCount >= capacity;
}

// Get available seats
int Course::getAvailableSeats() const {
    return capacity - enrollmentCount;
}
```

---

### 5\.5 Complete System Integration

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YTQ5YTg1M2ZmYzg5ZjRjOWM1YTM0MzEwM2VjNzAwOWZfYWRiOTczZWFlZmRmNTdkOTJkZWQxYjQ2ODM2YWIwN2RfSUQ6NzYyMTA1Mjc3OTE3MTIzNzA0Ml8xNzgxMDYwNjQ5OjE3ODExNDcwNDlfVjM)

#### Updated main\.cpp with both classes

```C++
#include <iostream>
#include "student.h"
#include "course.h"
using namespace std;

int main() {
    cout << "=== University Course Management System ===" << endl;
    
    // ----------------------------------------
    // Create students
    // ----------------------------------------
    Student alice, bob, carol;
    
    alice.id = 1001;
    alice.name = "Alice Chen";
    alice.major = "Computer Science";
    alice.gpa = 3.85;
    
    bob.id = 1002;
    bob.name = "Bob Smith";
    bob.major = "Computer Science";
    bob.gpa = 3.2;
    
    carol.id = 1003;
    carol.name = "Carol White";
    carol.major = "Mathematics";
    carol.gpa = 3.9;
    
    // ----------------------------------------
    // Create and set up courses
    // ----------------------------------------
    Course cs101, math201;
    
    cs101.initialize("CS101", "Intro to Programming", 3, 2);  // Capacity of 2
    math201.initialize("MATH201", "Calculus II", 4, 30);
    
    // ----------------------------------------
    // Enroll students in courses
    // ----------------------------------------
    cout << "\n--- Enrolling Students ---" << endl;
    
    cs101.enrollStudent(alice.id);   // Success
    cs101.enrollStudent(bob.id);     // Success
    cs101.enrollStudent(carol.id);   // Fail (course full)
    
    math201.enrollStudent(alice.id); // Success
    math201.enrollStudent(bob.id);   // Success
    
    // ----------------------------------------
    // Print final status
    // ----------------------------------------
    cout << "\n--- Course Status ---" << endl;
    cs101.print();
    cout << endl;
    math201.print();
    
    cout << "\n--- Student Status ---" << endl;
    cout << alice.name << " - Standing: " << alice.getStanding() << endl;
    cout << bob.name << " - Standing: " << bob.getStanding() << endl;
    cout << carol.name << " - Standing: " << carol.getStanding() << endl;
    
    return 0;
}
```

### 5\.6 Syntax Summary and Common Pitfalls

#### Quick Reference Table

|Task|Syntax|Example|
|---|---|---|
|**Class Declaration**|`class Name { members };`|`class Student { int id; };`|
|**Member Variable**|`type name;`|`string name;`|
|**Member Function \(header\)**|`returnType name(params);`|`void print() const;`|
|**Member Function \(implementation\)**|`ReturnType ClassName::name(params) { }`|`void Student::print() { }`|
|**Create Object**|`ClassName objectName;`|`Student alice;`|
|**Access Member**|`object.member`|`alice.name = "Alice";`|
|**Call Method**|`object.method(args)`|`alice.print();`|

#### Common Errors Checklist

|Error|Symptom|Solution|
|---|---|---|
|Missing semicolon after class|Weird errors in next line|Add `;` after `}`|
|`Student s();`|Declares function, not object|Use `Student s;` or `Student s(args);`|
|Forgetting `ClassName::`|"undefined reference" errors|Add scope resolution operator|
|Missing header guard|"redefinition of class"|Add `#ifndef`/`#define`/`#endif`|
|Not compiling all \.cpp files|Linker errors|Include all implementation files|
|Wrong quotes in \#include|File not found|Use `"file.h"` for your files, `<file.h>` for system|

---

### 5\.7 Practice Exercises

#### Exercise 1: Create a Professor Class

Create a `Professor` class with:

- Members: `id` \(int\), `name` \(string\), `department` \(string\), `tenured` \(bool\)

- Functions: `print()`, `isTenured()` \(returns tenured status\)

**Steps:**

1. Create `professor.h` with the class declaration

2. Create `professor.cpp` with function implementations

3. Update `main.cpp` to create and display a professor

#### Exercise 2: Enhance the Course Class

Add these features to the Course class:

1. `dropStudent(int studentID)` — Remove a student from enrollment

2. `hasStudent(int studentID)` — Check if a student is enrolled

3. `getEnrollmentRate()` — Return percentage filled \(as double\)

**Hints:**

- For dropStudent: Find the student, shift all later students left, decrease count

- Check for edge cases: student not found, empty course

#### Exercise 3: Create a Simple Gradebook

Create a `Gradebook` class that:

- Has a course and an array of student grades

- Can add grades for students

- Can calculate class average

- Can find highest and lowest grades

**Challenge:** Use parallel arrays or create a small `Grade` struct\.

---

### 5\.8 Summary

**Key Concepts:**

- **Class**: Blueprint/template defining what data and operations exist

- **Object**: Actual instance created from the class, with specific values

- **Member Variable**: Data stored inside each object

- **Member Function**: Operation that works on a specific object's data

- **Header File \(\.h\)**: Declares the class interface

- **Implementation File \(\.cpp\)**: Defines how functions work

**Design Principles:**

1. Group related data into classes

2. Each class should have a clear purpose

3. Use member functions to operate on object data

4. Split into \.h and \.cpp files for organization

5. Use header guards to prevent double inclusion

## Chapter Summary

### Key Concepts Review

**Functions**:

- **Function** = reusable block of code that performs a task

- **Parameters** = inputs the function receives

- **Return value** = output the function sends back

- **Pass by value** = function gets a copy \(default\)

- **Pass by reference** = function gets the original \(using `&`\)

- **Function overloading** = multiple functions with same name, different parameters

- **Declaration vs Definition** = interface vs implementation

**Classes and Objects**:

- **Class** = blueprint; **Object** = instance

- **Member variables** = data inside the class

- **Member functions** = behavior that operates on the object

- **Constructor** = runs when object is created; initializes data

- **Encapsulation** = private data \+ public interface \(getters/setters\)

- **Multi\-file design** = header \(`.h`\) declares, source \(`.cpp`\) implements

### Common Mistakes Table

|Mistake|Why Wrong|Correct Way|
|---|---|---|
|`Piece p();`|Declares a function, not an object|`Piece p;` or `Piece p(2, 3, 'W');`|
|Forgetting `;` after class|Syntax error|`};` at end of class|
|Accessing private members from outside|Compiler error|Use public getters/setters|
|Constructor with return type|`void Piece()` is wrong|`Piece()` — no return type|
|Forgetting `&` for pass\-by\-reference|Changes don't affect original|Use `int& x` to modify original|
|Only return type differs in overloading|Not allowed|Must differ in parameter types or count|

---

## Quick Reference Card

```Plaintext
Class definition:
  class Name { public: ... private: ... };

Creating object:
  ClassName obj;
  ClassName obj(args);

Member access:
  obj.memberVar;
  obj.memberFunc();

Constructor:
  ClassName() { ... }  // Same name as class, no return type

Multi-file structure:
  // In .h file:
  #ifndef NAME_H
  #define NAME_H
  class Name { ... };
  #endif
  
  // In .cpp file:
  #include "name.h"
  ReturnType Name::functionName() { ... }
```

