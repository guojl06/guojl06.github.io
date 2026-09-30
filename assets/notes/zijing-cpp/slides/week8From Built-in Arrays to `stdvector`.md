# week8From Built\-in Arrays to \`std::vector\`

**\# Chapter 8: From Built\-in Arrays to \`std::vector\`  **

**\# 第 8 章：从内置数组到 \`std::vector\`**



---



**\#\# Bilingual reference tables \| 双语参考表**



**\#\#\# Table 1: Core concepts \| 表 1：核心概念**



|Chinese \(中文\)|English|Description|
|---|---|---|

\| 数组 \| Array \| For a **built\-in array** / \`std::array\`: fixed length \`N\`, same type, contiguous storage\. **\*\*\`std::vector\`\*\*** is also contiguous but its **size can change** at run time\. \|

\| 指针 \| Pointer \| A variable that holds a memory address; can refer to a single object or the first element of an array\. \|

\| 下标 / 索引 \| Subscript / Index \| Integer offset `0 .. N-1` used with `a[i]` to access the `i`\-th element\. \|

\| 解引用 \| Dereference \| Operation `*p` reads or writes the object pointed to by `p`\. \|

\| 取址 \| Address\-of \| Operation `&x` yields the address of object `x`\. \|

\| 封装 \| Encapsulation \| Hiding representation details behind a class interface \(constructors, methods\)\. \|

\| 模板 \| Template \| A compile\-time parameterized blueprint for functions or classes \(`template<typename T> ...`\)\. \|

\| 容器 \| Container \| An object that owns and manages a sequence of elements \(e\.g\., `std::vector`, `std::string`\)\. \|

\| 嵌套 vector \| Nested vector \| \`std::vector\<std::vector\<T\>\>\`: outer sequence often models **rows**, each inner \`vector\<T\>\` a **row of cells** \(e\.g\. chess \`board\[r\]\[c\]\`\)\. \|

\| 迭代器 \| Iterator \| Generalized “position” in a sequence; for `vector`, pointer\-like random access iterators exist\. \|

\| 动态内存 \| Dynamic memory \| Storage whose lifetime is not tied to a scope block \(e\.g\., `new`/`delete`; `vector` manages this internally\)\. \|





**\#\#\# Table 2: Symbols \& operators \| 表 2：符号与运算符**



|Symbol|English Name|Chinese \(中文\)|Usage / Meaning|
|---|---|---|---|
|`T a[N];`|Array declaration|数组声明|`N` must be a compile\-time constant in classic C\-style array declarations at block scope \(before C\+\+14 `constexpr` nuances\); see notes\.|
|`a[i]`|Subscript operator|下标运算符|Element access; equivalent to `*(a + i)` for array/pointer decay cases\.|
|`*`|Dereference \(unary\)|解引用|Access object through pointer\.|
|`&`|Address\-of \(unary\)|取地址|Get address of an lvalue\.|
|`->`|Arrow operator|成员访问（经由指针）|`p->m` means `(*p).m` when `p` is pointer\-to\-class\.|
|`.`|Dot operator|成员访问|`obj.m` accesses member `m` of object `obj`\.|
|`[]`|Subscript|下标|Also overloaded for `std::vector` and `std::string`\.|
|`template<typename T>`|Template introduction|模板引入|Introduces a template parameter `T`\.|
|`new` / `delete`|Single\-object dynamic allocation|单个对象的动态分配 / 释放|`new T` allocates one object on the heap; `delete p` destroys it\.|
|`new[]` / `delete[]`|Array dynamic allocation|动态数组分配 / 释放|`new T[n]` allocates `n` objects; must pair with `delete[]`\.|



**\#\#\# Table 3: Chapter\-specific terms \| 表 3：本章术语**



|English|Chinese \(中文\)|Explanation|
|---|---|---|
|Array\-to\-pointer decay|数组退化为指针|In many expressions, an array name becomes a pointer to its first element; size information is lost\.|
|Contiguous storage|连续存储|Elements lie adjacent in memory; important for cache and pointer arithmetic\.|
|`size_t`|无符号尺寸类型|Unsigned type used for sizes and indices in the standard library\.|
|Capacity vs size|容量与大小|`vector` distinguishes `size()` \(number of elements\) from `capacity()` \(allocated room\)\.|
|RAII|资源获取即初始化|Objects acquire resources in constructors and release them in destructors; `vector` uses RAII for memory\.|
|Shallow copy|浅拷贝|Copy pointer members as addresses only; multiple owners of one heap block → double\-free risk\.|
|Deep copy|深拷贝|Allocate new storage and copy element values so each object owns its own buffer\.|



---



**\#\# Learning goals \| 学习目标**



By the end of this chapter, you should be able to:



1\. **Define** what a C\+\+ built\-in array is, how indexing and memory layout work, and how arrays interact with pointers\.  

2\. **Motivate** a small “dynamic array” class with encapsulation, then **generalize** it with templates\.  

3\. **Use** \`std::vector\` and \`std::string\` with correct mental models \(growth, iterators, common APIs\), including a **\*\*nested \`vector\`\*\*** for a **2D grid** \(e\.g\. chess board\)\.  

4\. **Implement** a tiny game that combines fixed arrays, pointers \(where appropriate\), templates, \`vector\`, and \`string\`\.



**Prerequisites \| 先修**：basic types, functions, references, classes, constructors/destructors, namespaces, \`using\` declarations\.



**Chess theme \| 国际象棋主题**：throughout the chapter, examples use ranks/files, piece symbols, and board rows to keep a single coherent application story\.



---



**\#\# 1\. Built\-in arrays: definition, syntax, and memory**

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OWVlYTY0MGNhZGNkNGFhMzI3YTQ5ZjRiN2FjZjI1ZTJfMWY0NWY4NzYwODg4ZGNiZjg0Y2ZiNTUyODRlZDg3NjNfSUQ6NzYyODg0NjQzNDAyNDIxMzY5NV8xNzgxMDYwMzQ5OjE3ODExNDY3NDlfVjM)

*\*Figure 1: Contiguous memory cells for \`int a\[4\]\`; each box holds one \`int\`; indices are 0\-based\.\**



**\#\#\# The Problem: many related values without many names**



\> **Opening Question**: How do you store the eight pawn files on the starting rank without eight separate variables?



**\#\#\# Step 1: The naive approach**



```C++
int whitePawnFile0 = 1;
int whitePawnFile1 = 2;
// ... six more variables ...
```



**Problems**:



1. Repetitive names and code\.  

2. Hard to loop over all pawns\.  

3. No single object you can pass to a function as one parameter\.

**\#\#\# Step 2: Exploring the problem**



\> **Exploration Questions**:  

> - What do all pawn files have in common \(type\)?  
> 
> - Do we always know the count at compile time \(eight files on a standard board\)?
> 
> 



**\#\#\# Step 3: The solution — built\-in arrays**



\> **Key idea \(要点\)**: An array is **one name** for **many elements of the same type**, laid out **contiguously** in memory\.



**\#\#\#\# Formal definition \| 定义**



A **built\-in array** of element type \`T\` and length \`N\` is a sequence of exactly \`N\` objects of type \`T\`, indexed from \`0\` to \`N\-1\`\. The expression \`a\[i\]\` accesses the element at offset \`i\` from the beginning of \`a\`\.



**\#\#\#\# Core syntax \| 语法格式**



```Plain Text
T arrayName[constant_length];           // declaration (length is compile-time constant in typical teaching examples)
T arrayName[constant_length] = { ... }; // declaration with initializer list
```



**Element access**:



```Plain Text
arrayName[index]     // read or write, index must be in [0, N-1] for valid access
```

```C++
#include <iostream>
using namespace std;
int main() {
  int a[10], b[10];
  for(int i = 0; i < 10; i++) {
    a[i] = i * 2 - 1;
    b[10 - i - 1] = a[i];
  }
  for(int i = 0; i < 10; i++) {
    cout << "a[" << i << "] = " << a[i] << "  ";
    cout << "b[" << i << "] = " << b[i] << endl;
  }
  return 0;
}
```

**Important notes \(accurate C\+\+ rules, simplified for class\)**:



\- At **automatic** \(stack\) scope, \`N\` must be known at compile time unless you use a different facility \(e\.g\., \`std::vector\`, \`std::array\`, or VLAs which are not standard C\+\+\)\.  

\- **Out\-of\-range** subscripts are **undefined behavior**; the language does not guarantee a run\-time error\.  

\- Arrays do **not** know their own length; you must pass size separately or use a sentinel \(risky\) or a higher\-level type\.



**\#\#\#\# Out\-of\-bounds examples \(undefined behavior\) \| 数组越界示例**



Valid indices for \`int a\[N\]\` are **\*\*\`0\` through \`N \- 1\` only\*\***\. The cases below are all **illegal**; a compiler might emit **no diagnostic**, and the program might **appear** to work until it corrupts memory\.



**Example A — constant past the end \| 常量下标越界**



```C++
int a[3] = {10, 20, 30};
int x = a[3];   // last valid index is 2; a[3] is UB
```



**Example B — off\-by\-one loop \| 循环多走一步**



```C++
#include <iostream>

int files[8] = {1, 2, 3, 4, 5, 6, 7, 8};
for (int i = 0; i <= 8; ++i) {   // should be i < 8
    std::cout << files[i];       // when i == 8, reads past the array
}
```



**Example C — wrong size passed with a pointer \| 长度传错**



```C++
#include <iostream>

void readSum(const int* p, int count) {
    int s = 0;
    for (int i = 0; i < count; ++i) {
        s += p[i];  // UB if count is larger than the actual array length
    }
}
int pieceValues[3] = {1, 3, 5};
readSum(pieceValues, 5);  // bug: caller passes 5 but only 3 elements exist
```





**\#\#\#\# Example : Basic \(chess application\)**



```C++
#include <iostream>

int main() {
    const int NUM_PAWNS = 8;
    char whitePawnFiles[NUM_PAWNS] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'};
    for (int i = 0; i < NUM_PAWNS; ++i) {
        std::cout << "Pawn " << i << " starts on file " << whitePawnFiles[i] << "\n";
    }
    return 0;
}
```



**\#\#\#\# Example 3: Structured \(module\-ready constants\)**



```C++
// chess/piece.h
#ifndef CHESS_PIECE_H
#define CHESS_PIECE_H

const int BOARD_SIZE = 8;
const int NUM_PAWNS = 8;

#endif
```



```C++
// main.cpp
#include <iostream>
#include "chess/piece.h"

int main() {
    int whitePawnRanks[NUM_PAWNS];  // uninitialized until we fill
    for (int i = 0; i < NUM_PAWNS; ++i) {
        whitePawnRanks[i] = 2;      // white pawn starting rank (teaching convention)
    }
    return 0;
}
```



**\#\#\# Step 4: Examples \(worked\) \| 示例（详解）**



**\#\#\#\# Example 4: Black pawn ranks \(all rank 7\)**



```C++
#include <iostream>
#include "chess/piece.h"

int main() {
    int blackPawnRanks[NUM_PAWNS];
    for (int i = 0; i < NUM_PAWNS; ++i) {
        blackPawnRanks[i] = 7;  // teaching convention: black pawns start on rank 7
    }
    for (int i = 0; i < NUM_PAWNS; ++i) {
        std::cout << blackPawnRanks[i] << (i + 1 == NUM_PAWNS ? '\n' : ' ');
    }
    return 0;
}
```



**\#\#\#\# Example 5: Back rank symbols on one line**



```C++
#include <iostream>
#include "chess/piece.h"

int main() {
    char backRank[BOARD_SIZE] = {'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'};
    for (int i = 0; i < BOARD_SIZE; ++i) {
        std::cout << backRank[i];
    }
    std::cout << "\n";
    return 0;
}
```



**\#\#\#\# Example 6: Safe indexing before \`board\[row\]\[col\]\`**



```C++
#include "chess/piece.h"

bool inBoard(int row, int col) {
    return row >= 0 && row < BOARD_SIZE && col >= 0 && col < BOARD_SIZE;
}

// int readCell(int board[][BOARD_SIZE], int row, int col) {
//     if (!inBoard(row, col)) { /* handle error */ return -1; }
//     return board[row][col];
// }
```



**After this section \| 本节检查点**: You can state why **\*\*\`a\[i\]\` out of range\*\*** is UB, and why a built\-in array **\*\*does not store \`N\`\*\***\.



---



**\#\# 2\. Pointers: definition, relationship to arrays, and syntax**

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YWFjNDE0NTYyYzgyZGY2NWExNjdkOTc5MGQxM2Q5MjhfYzA3YThmNDg5ZmVhMWFjMjk1YjZlMjcwZDBhMjM2YzNfSUQ6NzYyODg0NzIzNjU3MDk1ODc4OV8xNzgxMDYwMzQ5OjE3ODExNDY3NDlfVjM)

*\*Figure 2: A pointer variable stores an address that refers to an \`int\` object in memory\.\**



**Section roadmap \| 本节导读**：The next blocks give a **minimal memory model** \(bytes, addresses, \`new\`/\`delete\`\) so that **pointers**, **array decay**, and **who owns storage** have a common vocabulary\. Then we return to the opening problem: passing arrays into functions and using pointer \+ size safely\.



**\#\#\#\# Memory, addresses, and storage duration \(primer\) \| 内存、地址与存储期**



**Memory \| 内存**：Program data lives in **bytes** in RAM\. Each byte has a **machine address** \(think “house number on a long street”\)\. A variable of type \`T\` occupies **sizeof\(T\)** consecutive bytes at some starting address\.



**Object and address \| 对象与地址**：An **object** is a region of storage with a type and a lifetime\. The **address\-of** operator \`\&x\` yields the address where \`x\` begins\. A **pointer** variable \`T\* p\` **stores** such an address; \`\*p\` means “the \`T\` object located at that address\.”



**\#\#\#\# \`new\` and \`delete\` \(single object\) \| 单个对象的动态分配**



|Syntax|Role|
|---|---|

\| \`T\* p = new T\(args\);\` \| Allocates one \`T\` on the **heap**, runs a constructor, returns \`T\*\`\. \|

\| \`delete p;\` \| Destroys the object and **releases** that storage\. \`p\` becomes indeterminate; do not dereference it\. \|

\| \`T\* q = new T\[n\];\` \| Allocates **\*\*\`n\`\*\*** default\-constructed objects; returns pointer to first element\. \|

\| `delete[] q;` \| Destroys all `n` elements and releases the array storage\. \|



**Rules \| 规则**：Every \`new\` must match **exactly one** \`delete\`; every \`new\[\]\` must match **exactly one** \`delete\[\]\`\. Mixing \`delete\` with \`new\[\]\` or vice versa is **undefined behavior**\. Deleting the same pointer twice is **undefined behavior**\. Dereferencing after \`delete\` is **undefined behavior**\.



```C++
int* p = new int(42);   // one int on the heap
*p = 7;
delete p;             // frees that int
// *p = 3;            // wrong: UB (use a new pointer from new if you need more heap ints)

int* a = new int[4]{1, 2, 3, 4};
delete[] a;           // must be delete[], not delete
```



**\#\#\# The Problem: functions cannot receive “a whole array” as a value**



\> **Opening Question**: Why does \`void foo\(int a\[8\]\)\` behave like a pointer parameter, and how do we process a range of squares generically?



**\#\#\# Step 1: The naive approach**



Copy every element when calling a function \(slow, clumsy for large boards\)\.



**\#\#\# Step 2: Exploring the problem**



\> **Exploration Questions**:  

\> \- What is the **address** of \`x\`?  

> - If you know the address of the first cell of an array, how do you reach the next cell?
> 
> 



**\#\#\# Step 3: The solution — pointers and array decay**



\> **Key idea \(要点\)**: A pointer holds an **address**\. For arrays, the array name often **decays** to a pointer to the first element; \`a\[i\]\` and \`\*\(a \+ i\)\` match for built\-in arrays\.



**\#\#\#\# Formal definitions \| 定义**



\- **\*\*Pointer \(to \`T\`\)\*\***: A value of type \`T\*\` that is either null \(\`nullptr\` in modern C\+\+\) or holds the address of an object of type \`T\`\.  

\- **Address\-of**: For an object \`x\` of type \`T\`, \`\&x\` has type \`T\*\` and points to \`x\`\.  

\- **Dereference**: For \`p\` of type \`T\*\`, \`\*p\` is the object \`p\` points to \(if \`p\` is valid and not singular\)\.  

\- **Array\-to\-pointer decay**: In many value contexts, an lvalue of type “array of \`N\` \`T\`” becomes a prvalue of type “pointer to \`T\`” pointing to the first element\.



**Parameter decay \| 形参退化**：In \`void foo\(int a\[8\]\)\`, the \`8\` is **not part of the type** of \`a\` for overload resolution—\`a\` is effectively \`int\*\`\. Do not rely on the number for bounds checking; pass \`N\` separately or use \`std::span\` / \`std::vector\`\.



**\*\*\`sizeof\` trap \| \`sizeof\` 陷阱\*\***：Inside such a function, \`sizeof\(a\)\` is typically **\*\*\`sizeof\(int\*\)\`\*\***, not \`8 \* sizeof\(int\)\`, because \`a\` is a pointer there\. At the **definition site** of a real array, \`sizeof\(arr\)\` gives the full byte size of the array object\.



**Core syntax \| 语法格式**



```Plain Text
T* p;              // uninitialized local pointer: dangerous until assigned
T* p = &x;         // p points to x
T* p = arr;        // often equivalent to &arr[0] after decay
*p = value;        // write through pointer
p[i]               // pointer subscript: valid for contiguous sequence of T objects
p + k              // pointer arithmetic: moves k elements (not k bytes), type must be complete
```







**\#\#\#\# Example 1: Minimal**



```C++
#include <iostream>

int main() {
    int x = 42;
    int* p = &x;
    std::cout << *p << "\n";  // 42
    *p = 7;
    std::cout << x << "\n";   // 7
    return 0;
}
```



**\#\#\#\# Example 2: Basic \(chess application\)**



```C++
#include <iostream>

void printFiles(const char* firstFile, int count) {
    for (int i = 0; i < count; ++i) {
        std::cout << firstFile[i];  // same as *(firstFile + i)
    }
    std::cout << "\n";
}

int main() {
    const char files[8] = {'a','b','c','d','e','f','g','h'};
    printFiles(files, 8);  // files decays to const char*
    return 0;
}
```



**\#\#\#\# Example 3: Structured \(pointer \+ size idiom\)**



```C++
#include <iostream>

int sumMaterial(const int* values, int count) {
    int total = 0;
    for (int i = 0; i < count; ++i) {
        total += values[i];
    }
    return total;
}

int main() {
    int pieceValues[5] = {1, 3, 3, 5, 9};  // pawn,knight,bishop,rook,queen (example weights)
    std::cout << sumMaterial(pieceValues, 5) << "\n";
    return 0;
}
```



**\#\#\#\# Example 4: \`new\[\]\` / \`delete\[\]\` with a small buffer \(teaching\)**



```C++
#include <iostream>

int main() {
    const int n = 8;
    int* ranks = new int[n];
    for (int i = 0; i < n; ++i) {
        ranks[i] = 2;  // example: white pawn rank
    }
    std::cout << ranks[0] << "\n";
    delete[] ranks;
    return 0;
}
```



**\#\#\# Step 4: Examples \(worked\) \| 示例（详解）**



**\#\#\#\# Example 6: \`swapInt\` through pointers**



```C++
void swapInt(int* a, int* b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

// int x = 1, y = 2;
// swapInt(&x, &y);  // now x == 2, y == 1
```



**\#\#\#\# Example 7: \`minRank\` with pointer \+ count**



```C++
int minRank(const int* begin, int count) {
    if (count <= 0) {
        return 0;  // teaching only: real code would use optional or assert
    }
    int best = begin[0];
    for (int i = 1; i < count; ++i) {
        if (begin[i] < best) {
            best = begin[i];
        }
    }
    return best;
}

// int ranks[8] = {7, 7, 7, 7, 7, 7, 7, 7};
// int m = minRank(ranks, 8);
```



**After this section \| 本节检查点**: You can explain **\*\*\`void f\(int a\[8\]\)\` vs \`int\*\`\*\***, and why **\*\*\`sizeof\(a\)\` inside \`f\`\*\*** is not \`8 \* sizeof\(int\)\`\.

Object pointers are widely used in C\+\+ programs for dynamic memory management and flexible array usage, even before considering class inheritance or polymorphism\. The most common scenario is storing or manipulating arrays of objects when the number of objects may be determined at runtime or when objects must be created and destroyed dynamically\.



Consider a class `Pawn` representing a chess pawn\. If you need an array of pawns, but want to allocate each on the heap \(for example, to explicitly control object lifetimes or to easily reset or replace pawns\), you would use an array of pointers\. Here is a simple example:



```C++
#include <iostream>
using namespace std;

class Pawn {
public:
    Pawn(int id) : id_(id) {}
    int id() const { return id_; }
    void promote() { promoted_ = true; }
    void print() const { 
        cout << "Pawn " << id_ << (promoted_ ? " promoted" : "") << endl; 
    }
private:
    int id_;
    bool promoted_ = false;
};

int main() {
    const int count = 8;
    Pawn* pawns[count];
    // Dynamically create pawns
    for (int i = 0; i < count; ++i) {
        pawns[i] = new Pawn(i);
    }
    // Use pawns via pointer access
    pawns[0]->promote();  // promote the first pawn
    for (int i = 0; i < count; ++i) {
        pawns[i]->print();
    }
    // Clean up: delete heap objects
    for (int i = 0; i < count; ++i) {
        delete pawns[i];
    }
    return 0;
}
```



In this example, `pawns` is an array of pointers, and each pointer is initialized with a dynamically allocated `Pawn` object\. This technique is useful for managing arrays of objects when you might need to control each object's lifetime independently or when objects are large or expensive to copy\. 



```C++
Pawn* blackPawns[8];
for (int i = 0; i < 8; ++i) {
    blackPawns[i] = new Pawn(i);
}
Pawn* whitePawns[8];
for (int i = 0; i < 8; ++i) {
    whitePawns[i] = blackPawns[i];
}
```

// Is there any problem with the above code?









**\#\#\#\# Shallow copy vs deep copy \| 浅拷贝与深拷贝（详细）**



**Shallow copy is dangerous \!**

Both arrays will try to delete the same objects, causing a crash or memory corruption\.



```C++
// Full wrong code (shallow copy)
#include <iostream>
using namespace std;

class Pawn {
public:
    Pawn(int id) : id_(id) {}
    int id() const { return id_; }
    void promote() { promoted_ = true; }
    void print() const {
        cout << "Pawn " << id_ << (promoted_ ? " promoted" : "") << endl;
    }
private:
    int id_;
    bool promoted_ = false;
};

int main() {
    Pawn* blackPawns[8];
    for (int i = 0; i < 8; ++i) {
        blackPawns[i] = new Pawn(i);
    }
    Pawn* whitePawns[8];
    for (int i = 0; i < 8; ++i) {
        whitePawns[i] = blackPawns[i]; // shallow copy: both arrays point to same objects!
    }

    whitePawns[0]->promote(); // Promotes the same Pawn(0) both arrays point to

    cout << "All pawns:\n";
    for (int i = 0; i < 8; ++i) {
        blackPawns[i]->print();
    }

    // ERROR: Both loops delete the same memory!
    for (int i = 0; i < 8; ++i) {
        delete blackPawns[i];
    }
    for (int i = 0; i < 8; ++i) {
        delete whitePawns[i]; // DOUBLE DELETE: undefined behavior!
    }
    return 0;
}
```



**What goes wrong?**

After deleting from blackPawns, all the Pawn objects are already destroyed\.

The following deletes via whitePawns\[i\] are *double deletes* \(deleting memory that's already freed\)\.

This results in undefined behavior, typically leading to a crash or subtle memory corruption\.

You must never `delete` the same heap pointer value more than once\!

**Correct code:** Each array holds independent heap objects \(deep copy\)\.



```C++
Pawn* blackPawns[8];
for (int i = 0; i < 8; ++i) {
    blackPawns[i] = new Pawn(i);
}
Pawn* whitePawns[8];
for (int i = 0; i < 8; ++i) {
    whitePawns[i] = new Pawn(i);
}
// ... use pawns ...
for (int i = 0; i < 8; ++i) {
    delete blackPawns[i];
    delete whitePawns[i];
}
```



// Moral: Always perform a deep copy when you want truly independent objects; never just duplicate pointers to the same heap object unless you have a clear ownership or sharing strategy \(like using smart pointers\)\.









**Member\-wise copy \| 逐成员拷贝**：When you do not declare your own copy constructor or copy assignment, the compiler generates **member\-wise** copies: each data member is copied “as itself\.” For \`int\` or \`double\`, that is a bitwise copy of the value\. For a **raw pointer** \`int\* data\_\`, member\-wise copy copies **only the address**, not the heap block it points to\.



**Shallow copy \| 浅拷贝**：Two objects end up **sharing the same resource** \(here, the same heap array\)\. Their \`data\_\` pointers **compare equal** after \`b = a\`\. Each object’s destructor still runs \`delete\[\] data\_\` → **double free** \(**undefined behavior**\)\. Also, if one object mutates the buffer, the other sees the change—sometimes intended with **shared ownership**, but then you need **\*\*\`std::shared\_ptr\`\*\*** or similar, not two independent destructors\.



**Deep copy \| 深拷贝**：On copy, allocate a **new** heap array of the same logical length, **copy every element** from the source into the new block, and store its address in the new object’s \`data\_\`\. After a deep copy, \`a\.data\_ \!= b\.data\_\` \(unless empty\), both **own** separate storage, and each destructor frees **its own** block exactly once\.



**3\. Encapsulating a dynamic array: motivation and class design**



**\#\#\# The Problem: fixed \`N\` is too rigid for unknown game length**



\> **Opening Question**: What if we want to record **every move** in a match, but we do not know the move count before the game ends?



**Step 1: The naive approach**



Pick a “large enough” fixed array `Move moves[5000];` and hope we never overflow; waste memory when games are short\.



**Step 2: Exploring the problem**



\> **Exploration Questions**:  

\> \- Who is responsible for **allocation**, **reallocation**, and **deallocation**?  

\> \- How do we prevent **double free** and **leaks**?



**Step 3: The solution — a small \`IntDynArray\` class \(encapsulation\)**



\> **Key idea \(要点\)**: Put **invariants** \(length, capacity, pointer to storage\) behind **constructors**, **destructor**, and **methods** so callers manipulate a **logical object**, not raw pointers\.



**Design goals \| 设计目标**



\- **Encapsulation**: \`private\` members \(\`data\_\`, \`size\_\`, \`cap\_\`\) and a **public** API \(\`push\_back\`, \`size\`, \`at\`\)\.  

\- **Invariant**: \`0 \<= size\_ \<= cap\_\`, and \`data\_\` points to a heap array of length \`cap\_\` \(or is \`nullptr\` when \`cap\_ == 0\`\)\.  

\- **Rule of Three / Five \(preview\)**: copying this type needs correct **copy semantics**; see shallow vs deep copy below\.

**\#\#\#\# Example 1: Minimal skeleton \(single responsibility\)**



```C++
#include <cstddef>
#include <stdexcept>

class IntDynArray {
public:
    IntDynArray() : data_(nullptr), size_(0), cap_(0) {}

    IntDynArray(const IntDynArray&) = delete;
    IntDynArray& operator=(const IntDynArray&) = delete;

    ~IntDynArray() {
        delete[] data_;
    }

    std::size_t size() const { return size_; }

    void push_back(int value) {
        if (size_ == cap_) {
            grow();
        }
        data_[size_] = value;
        ++size_;
    }

    int at(std::size_t i) const {
        if (i >= size_) {
            throw std::out_of_range("IntDynArray::at");
        }
        return data_[i];
    }

private:
    int* data_;
    std::size_t size_;
    std::size_t cap_;

    void grow() {
        std::size_t newCap = (cap_ == 0) ? 1 : cap_ * 2;
        int* newData = new int[newCap];
        for (std::size_t i = 0; i < size_; ++i) {
            newData[i] = data_[i];
        }
        delete[] data_;
        data_ = newData;
        cap_ = newCap;
    }
};
```



**Note**: Production code should follow **Rule of Five**, **exception safety**, and use **smart pointers** or standard containers; here the goal is **pedagogical transparency**\.

**\#\#\#\# Example 2: Basic \(chess application — record square indices\)**



```C++
#include <iostream>

// After defining IntDynArray with a working push_back:
int main() {
     IntDynArray moves;
     moves.push_back(35);  // example encoded square index
     moves.push_back(22);
     std::cout << moves.size() << "\n";
     return 0;
}
```

**\#\#\#\# Example 2: Copy constructor and assignment operator**



```C++
// If copy were not deleted, shallow copy would make this dangerous:
IntDynArray a;
a.push_back(1);
IntDynArray b = a;  // b.data_ == a.data_; double delete at end of scope → UB
```

The code above performs a shallow copy: it copies only the pointer values, not the actual objects on the heap\. This is very dangerous, because both objects \(or arrays\) now point to the same dynamic memory\. Any changes through one pointer affect the same memory as the other, and deleting the data through both will cause double\-free errors and undefined behavior\. Always use deep copy or prohibit copying when managing dynamic memory manually\.



```C++
// Example: Deep Copy Constructor and Bounds Checking

#include <iostream>
#include <stdexcept>
using namespace std;

class IntDynArray {
public:
    // Constructor: Creates a dynamic integer array of specified size
    IntDynArray(size_t size)
        : data_(size == 0 ? nullptr : new int[size]), size_(size), cap_(size) {
        for (size_t i = 0; i < size_; ++i) {
            data_[i] = 0;
        }
    }

    // Deep copy constructor
    IntDynArray(const IntDynArray& other)
        : data_(other.size_ == 0 ? nullptr : new int[other.size_]),
          size_(other.size_),
          cap_(other.size_) {
        for (size_t i = 0; i < size_; ++i) {
            data_[i] = other.data_[i];
        }
    }

    // Destructor
    ~IntDynArray() {
        delete[] data_;
    }

    // 'at' function with bounds checking
    int& at(size_t idx) {
        if (idx >= size_) {
            throw out_of_range("Index out of range");
        }
        return data_[idx];
    }

    const int& at(size_t idx) const {
        if (idx >= size_) {
            throw out_of_range("Index out of range");
        }
        return data_[idx];
    }

    size_t size() const { return size_; }

private:
    int* data_;
    size_t size_;
    size_t cap_;
};

int main() {
    IntDynArray arr(5);
    for (size_t i = 0; i < arr.size(); ++i) {
        arr.at(i) = static_cast<int>(i * 2);
    }

    IntDynArray arrCopy = arr; // Deep copy

    cout << "arrCopy elements: ";
    for (size_t i = 0; i < arrCopy.size(); ++i) {
        cout << arrCopy.at(i) << " ";
    }
    cout << endl;

    try {
        cout << arrCopy.at(100) << endl; // Out of bounds, throws exception
    } catch (const out_of_range& e) {
        cout << "Caught exception: " << e.what() << endl;
    }

    return 0;
}
```





---



**\#\# 4\. Templates: why \`IntDynArray\` is not enough**



**The Problem: we also want \`double\` scores or \`char\` symbols**



\> **Opening Question**: Do we duplicate the whole class for \`double\`, \`char\`, \`PieceTag\`, …?



**\#\#\# Step 1: The naive approach**



Copy\-paste `DoubleDynArray`, `CharDynArray`, … and fix types everywhere\.



**\#\#\# Step 2: Exploring the problem**



\> **Exploration Questions**:  

> - Which lines change when the element type changes?  
> 
> 

\> \- How can the compiler still **type\-check** each instantiation?



**\#\#\# Step 3: The solution — class templates**



\> **Key idea \(要点\)**: A **template** is a pattern with **placeholders**; the compiler **generates concrete classes** when you write \`DynArray\<int\>\`, \`DynArray\<double\>\`, etc\.



**\#\#\#\# Formal definition \| 定义**



A **class template** is a template that declares a family of classes parameterized by one or more template parameters \(commonly \`typename T\`\)\. Each **instantiation** \(\`DynArray\<int\>\`\) is a distinct class type\.



**\#\#\#\# Core syntax \| 语法格式**



```C++
template<typename T>
class DynArray {
public:
    // use T as element type
private:
    T* data_;
    std::size_t size_;
    std::size_t cap_;
};
```



**Instantiation examples**:



```Plain Text
DynArray<int> ints;
DynArray<double> scores;
```



**\#\#\#\# Example 1: Minimal template excerpt**



```C++
#include <cstddef>

template<typename T>
class DynArray {
public:
    DynArray() : data_(nullptr), size_(0), cap_(0) {}
    DynArray(const DynArray&) = delete;
    DynArray& operator=(const DynArray&) = delete;
    ~DynArray() { delete[] data_; }

    void push_back(const T& value) {
        if (size_ == cap_) {
            grow();
        }
        data_[size_] = value;
        ++size_;
    }

    std::size_t size() const { return size_; }

    const T& at(std::size_t i) const { return data_[i]; }

private:
    T* data_;
    std::size_t size_;
    std::size_t cap_;

    void grow() {
        std::size_t newCap = (cap_ == 0) ? 1 : cap_ * 2;
        T* newData = new T[newCap];
        for (std::size_t i = 0; i < size_; ++i) {
            newData[i] = data_[i];
        }
        delete[] data_;
        data_ = newData;
        cap_ = newCap;
    }
};
```



**Teaching limitations**: \`T\` must be **default\-constructible** for \`new T\[newCap\]\` as written; real \`std::vector\` uses allocator traits and uninitialized storage techniques\.



**\#\#\#\# Example 2: Basic \(chess — multiple types\)**



Place **after** the complete \`DynArray\` template from Example 1 in the same \`\.cpp\` translation unit, then compile:



```C++
#include <iostream>

int main() {
    DynArray<int> moveSquares;
    moveSquares.push_back(35);
    DynArray<double> evaluationTrace;
    evaluationTrace.push_back(0.25);
    std::cout << moveSquares.size() << " " << evaluationTrace.size() << "\n";
    return 0;
}
```



\(\`DynArray\` in Example 1 includes **\*\*\`= delete\`\*\*** on copy for the same ownership reasons as \`IntDynArray\`\.\)



**After this section \| 本节检查点**: You can list **\*\*two operations \`T\`\*\*** must support for the teaching \`DynArray\<T\>::grow\(\)\` as written \(\`new T\[\]\` \+ assignment\)\.



---



**\#\# 5\. \`std::vector\`: STL design, essential API, and mental model**



**\#\#\# The Problem: we want a standard, exception\-safe, allocator\-aware dynamic array**



\> **Opening Question**: How does the standard library unify “dynamic sequence” for arbitrary \`T\` with iterators, algorithms, and predictable complexity?



**\#\#\# Step 1: The naive approach**



Keep a handwritten \`DynArray\<T\>\` \(or C \`realloc\`\) in every project: every team reinvents **copy/move**, **exception safety** on \`push\_back\`, **iterator invalidation** rules, and **allocator** hooks differently—bugs and subtle incompatibilities follow\.



**\#\#\# Step 2: Exploring the problem**



\> **Exploration Questions**:  

> - After `push_back`, can an old `T*` or iterator to an element still be trusted?  
> 
> - What should happen if element construction throws during `insert`—is the `vector` left in a known state?
> 
> 



**\#\#\# Step 3: The solution — \`std::vector\<T, Allocator\>\`**



\> **Key idea \(要点\)**: \`vector\` is a **class template** representing a contiguous dynamic array with **size**, **capacity**, **RAII destructor**, **copy/move operations**, and **iterators** compatible with the STL\.



**Exception safety **: Standard \`vector\` member functions give **documented** guarantees: on failure they leave the \`vector\` in a **valid** state \(no leaked internal storage in normal use\)\. You avoid hand\-written \`new\[\]\`/\`delete\[\]\` rollback paths like in a minimal teaching \`DynArray\`\. Exact guarantees depend on the operation and \`T\` \(see \[vector\.cons\] / \`push\_back\` in the standard\)\.



**Iterator / reference invalidation \(必须知道\)**: Any operation that may **reallocate** storage \(e\.g\. \`push\_back\` when \`size == capacity\`, \`resize\` upward, etc\.\) **invalidates** iterators, pointers, and references to elements \(unless specified otherwise for \`erase\`/\`insert\`—see standard\)\. **Pattern**: do not cache \`\&v\[0\]\` across \`push\_back\` loops; re\-query after growth, or reserve first if you know \`N\`\.

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ODNkNmU4YmZiNjUzZTMxNTZlNzViNjVmZDE4N2EyY2FfOWE4YTVlNjc0Y2YzMTZkNWRhMDcwMTMzNzU0YTI5N2NfSUQ6NzYyODg0NjMwOTAyMTM4Nzc0MF8xNzgxMDYwMzQ5OjE3ODExNDY3NDlfVjM)



*\*Figure 3: \`std::vector\` may allocate a larger buffer, copy or move elements into it, and release the old block; \`size\(\)\` is the number of elements, \`capacity\(\)\` the allocated slots—this is the standard “dynamic contiguous array” model you hand\-rolled in §3\.\**



**\#\#\#\# Formal definition \| 定义**



`std::vector` is a sequence container storing elements contiguously, supporting **amortized constant\-time** \`push\_back\` \(when reallocation happens, it is linear, but averaged over many inserts the cost per insert remains constant\), **random access** in constant time to any element by index, and **iterator** interfaces that generalize pointers\.



**\#\#\#\# Core syntax \| 语法格式**



```C++
#include <vector>

std::vector<T> v;                 // empty vector
std::vector<T> v(n);              // n default-constructed elements
std::vector<T> v(n, value);       // n copies of value
std::vector<T> v{ a, b, c };      // initializer list (C++11)
v.push_back(x);                   // append (may reallocate)
v[i];                             // unchecked index
v.at(i);                          // bounds-checked index
v.size();                         // element count
v.capacity();                     // allocated element slots
v.begin(); v.end();               // half-open range [begin, end)
```



**\#\#\#\# Complexity notes \(accurate teaching summary\)**



\- \`push\_back\`: **amortized** O\(1\) when growth strategy is multiplicative \(implementation\-defined constant factor\)\.  

\- \`insert\`/\`erase\` in the middle: **O\(n\)** due to shifting elements in a contiguous array\.



**\*\*\`\[\]\` vs \`at\`\*\***: \`v\[i\]\` has **no** bounds check—out of range is **UB**\. \`v\.at\(i\)\` throws \`std::out\_of\_range\` when \`i \>= size\(\)\`\.



**\#\#\#\# 2D grid: nested \`std::vector\` \| 用 \`vector\` 构建二维数组**



A **matrix\-style** layout can be modeled as a **\*\*\`vector\` whose elements are themselves \`vector\`s\*\***:



```Plain Text
std::vector<std::vector<T>> grid;
```



\- **\*\*Outer \`vector\`\*\***: one entry per **row** \(or per “line” in your convention—just stay consistent\)\.  

\- **\*\*Inner \`vector\`\*\***: the **cells in that row** \(columns\)\.  

\- **Element access**: \`grid\[row\]\[col\]\` — first \`\[\]\` selects the row \(\`std::vector\<T\>\&\`\), second selects the column inside that row\.



**Construction idiom \| 构造惯用法**：Build an \`R × C\` table filled with copies of one value:



```C++
std::vector<std::vector<char>> board(
    R, std::vector<char>(C, '.'));   // R rows, each row has C chars initialized to '.'
```



Here the **inner** temporary \`std::vector\<char\>\(C, '\.'\)\` is copied into each of the **R** rows \(each row gets its **own** inner \`vector\` object\)\.



**Sizes \| 尺寸**：\`board\.size\(\)\` is the number of rows; \`board\[r\]\.size\(\)\` is the width of row \`r\` \(for a chess board you keep **\*\*\`board\[r\]\.size\(\) == BOARD\_SIZE\`\*\*** for every \`r\`\)\. You can still **resize** one row differently by mistake—treat that as a bug unless you intentionally want a **jagged** array\.



**Memory picture \| 内存图景**：The **outer** \`vector\` stores \(typically\) contiguous **\*\*\`vector\<char\>\` objects\*\*** \(each small object may hold pointer/size/capacity to a **separate** heap buffer for that row\)\. So this is **not** one single contiguous \`R\*C\` block of \`char\` like \`char flat\[R\*C\]\`; for cache\-critical numeric grids, a **flat** \`std::vector\<T\>\(R \* C\)\` plus \`index = row \* C \+ col\` is common\. For a **text chess board**, nested \`vector\` is clear and matches \`board\[row\]\[col\]\` notation\.



**Reminder \| 易混点**：**\*\*“\`vector\` 的元素连续”\*\*** 这里指的是 **\*\*每一行内部的 \`char\` 连续\*\***，以及 **外层保存的“行对象”这一层** 连续——**\*\*不要把整盘 \`R×C\` 格当成一块物理上连续的 \`R\*C\` 字节\*\***（除非你用扁平 \`vector\` 自己算下标）。



**Bounds \| 边界**：\`board\.at\(r\)\.at\(c\)\` checks **both** indices; \`board\[r\]\[c\]\` is unchecked twice\.



**\#\#\#\# Example 1: Minimal**



```C++
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v;
    v.push_back(10);
    v.push_back(20);
    std::cout << v.size() << "\n";  // 2
    return 0;
}
```



**\#\#\#\# Example 1b: Chess board as \`std::vector\<std::vector\<char\>\>\` \| 棋盘网格**



Use \`BOARD\_SIZE\` from \`chess/piece\.h\`\. Convention: **\*\*\`board\[r\]\[c\]\`\*\*** — \`r\` from **0 \(top / rank 8\)** to **7 \(bottom / rank 1\)**, \`c\` **0 = a\-file** through **7 = h\-file**\. Empty square \`'\.'\`; white pawn \`'P'\`, black pawn \`'p'\` \(same symbols as the course mini\-game\)\.



```C++
#include <iostream>
#include <vector>

#include "chess/piece.h"

void printBoard(const std::vector<std::vector<char>>& b) {
    for (int r = 0; r < BOARD_SIZE; ++r) {
        for (int c = 0; c < BOARD_SIZE; ++c) {
            std::cout << b[r][c] << ' ';
        }
        std::cout << '\n';
    }
}

int main() {
    std::vector<std::vector<char>> board(
        BOARD_SIZE, std::vector<char>(BOARD_SIZE, '.'));

    for (int c = 0; c < BOARD_SIZE; ++c) {
        board[1][c] = 'p';  // black pawns on rank 7
        board[6][c] = 'P';  // white pawns on rank 2
    }

    printBoard(board);
    return 0;
}
```



Extending this object \(add knights, read moves, validate\) is the same pattern: **\*\*mutate \`board\[toR\]\[toC\]\`\*\*** and clear the from\-square, or swap with a temporary—always keep **\*\*\`0 \<= r, c \< BOARD\_SIZE\`\*\*** before indexing \(reuse **\*\*\`inBoard\`\*\*** from §1 Example 6, or use **\*\*\`at\(\)\.at\(\)\`\*\***\)\.



**Optional OO sketch \| 可选：封装成类**：When the board grows rules \(castling, en passant, etc\.\), wrap cells in a type:



```C++
// teaching sketch — English comments only in real headers
class Board {
public:
    explicit Board();
    char cell(int row, int col) const;
    void setCell(int row, int col, char symbol);
private:
    std::vector<std::vector<char>> cells_;
};
```



The **object** owns **\*\*\`cells\_\`\*\*** and is the **only** place that should enforce “square inside 8×8\.” The course repo’s \`chess/board\.\*\`, \`chess/pawn\.\*\`, and \`chess/piece\.h\` form a minimal **pawn\-only** example: **\*\*\`Piece\`\*\*** base, **\*\*\`Pawn\`\*\*** derived, **\*\*\`Board\`\*\*** owns the grid and turn rules\.



**\#\#\#\# Example 2: Basic \(chess — capture list of square indices\)**



```C++
#include <iostream>
#include <vector>

int main() {
    std::vector<int> capturedSquares;
    capturedSquares.push_back(35);  // example square encoding
    capturedSquares.push_back(22);
    for (std::size_t i = 0; i < capturedSquares.size(); ++i) {
        std::cout << capturedSquares[i] << " ";
    }
    std::cout << "\n";
    return 0;
}
```



**\#\#\#\# Example 3: Structured \(range\-for \+ \`const\` correctness\)**



```C++
#include <iostream>
#include <vector>

void printInts(const std::vector<int>& values) {
    for (const auto& x : values) {
        std::cout << x << " ";
    }
    std::cout << "\n";
}

int main() {
    std::vector<int> material = {1, 3, 3, 5, 9};
    printInts(material);
    return 0;
}
```



**\#\#\# Step 4: Examples \(worked\) \| 示例（详解）**



**\#\#\#\# Example 4: Corner marks on the same nested\-board model \| 角格标记**



Builds the same **\*\*\`vector\<vector\<char\>\>\`\*\*** shape as Example **1b**, then marks the four corner squares \(e\.g\. for a tiny UI test or lesson diagram\)\.



```C++
#include <iostream>
#include <vector>

#include "chess/piece.h"

int main() {
    std::vector<std::vector<char>> board(
        BOARD_SIZE, std::vector<char>(BOARD_SIZE, '.'));
    board[0][0] = '+';
    board[0][BOARD_SIZE - 1] = '+';
    board[BOARD_SIZE - 1][0] = '+';
    board[BOARD_SIZE - 1][BOARD_SIZE - 1] = '+';
    for (int r = 0; r < BOARD_SIZE; ++r) {
        for (int c = 0; c < BOARD_SIZE; ++c) {
            std::cout << board[r][c];
        }
        std::cout << "\n";
    }
    return 0;
}
```



**\#\#\#\# Example 5: \`shrink\_to\_fit\` \(request tighter capacity\)**



After a long series of \`push\_back\`s followed by many \`pop\_back\`s, **\*\*\`capacity\(\)\`\*\*** may stay large while **\*\*\`size\(\)\`\*\*** is small\. **Non\-binding** request:



```C++
v.shrink_to_fit();  // implementation may reallocate smaller; invalidates iterators if it does
```



Older idiom: `std::vector<T>(v).swap(v);` to replace `v` with a tight copy\. Use when memory footprint matters more than a possible reallocation cost\.



**\#\#\#\# Example 6: Iterator loop \(same as index loop, different style\)**



```C++
void printIntsIter(const std::vector<int>& values) {
    for (auto it = values.begin(); it != values.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n";
}
```



**After this section \| 本节检查点**: You can explain **\*\*\`size\` vs \`capacity\`\*\***, why **\*\*\`push\_back\` may invalidate\*\*** saved pointers into the \`vector\`, when **\*\*\`at\`\*\*** is safer than **\*\*\`\[\]\`\*\***, and how to build an **\*\*\`R×C\`\*\*** table with **\*\*\`std::vector\<std::vector\<T\>\>\(R, std::vector\<T\>\(C, val\)\)\`\*\*** \(e\.g\. chess **\*\*\`board\[r\]\[c\]\`\*\***\)\.



---



**\#\# 6\. Analogy: \`std::string\` as \`vector\<char\>\`\-like text**



**\#\#\# The Problem: variable\-length text is also a dynamic sequence**



\> **Opening Question**: Why does \`s\[i\]\` feel like \`v\[i\]\`, and why can both use range\-\`for\`?



**\#\#\# Step 1: The naive approach**



Store text in a **\*\*fixed \`char buf\[N\]\`\*\*** and \`strcpy\`/\`strcat\`—easy to **overflow** \`N\`, easy to forget a null terminator, and no **value semantics** as a first\-class object\.



**\#\#\# Step 2: Exploring the problem**



\> **Exploration Questions**:  

> - Who owns the buffer when a function returns “a string”?  
> 
> - How do you grow the buffer when the user types a longer line than you expected?
> 
> 



**\#\#\# Step 3: The solution — \`std::basic\_string\` \(most often \`std::string\`\)**



\> **Key idea \(要点\)**: \`std::string\` is a **specialized** contiguous character sequence with **string\-specific** operations \(\`substr\`, \`find\`, \`c\_str\`\), but many core ideas match \`vector\`: **size**, **capacity\-style growth**, **iterators**, **RAII**\.



**\#\#\#\# Formal definition \| 定义**



`std::string` is a typedef for `std::basic_string<char>`: a contiguous sequence of `char` with length `size()` and null\-terminator guarantee for `c_str()` in C\+\+11 and later \(the returned C string includes `'\0'` after the data\)\.



**\*\*\`c\_str\(\)\` dangling danger \| 悬垂指针\*\***：The pointer returned by \`c\_str\(\)\` \(and \`data\(\)\` for non\-const strings in C\+\+17\+\) can be **invalidated** by any \`string\` operation that **reallocates** \(e\.g\. \`\+=\`, \`push\_back\`, \`append\`\)\. Do not save \`const char\* p = s\.c\_str\(\)\` across such mutations and then read through \`p\`\.



**Wrong pattern \| 错误示例**：



```C++
std::string s = "e4";
const char* p = s.c_str();
s += " e5";           // may reallocate; old buffer may be freed
// std::cout << p;    // UB: p may dangle — never use p after mutating s
```



**\#\#\#\# Core syntax \| 语法格式**



```C++
#include <string>

std::string s;                 // empty
std::string s = "hello";       // literal initialization
s.push_back('!');              // append one char
s += " world";                 // append string (also operator+ exists)
std::size_t n = s.size();      // length (not counting extra null for string object storage)
const char* p = s.c_str();     // pointer to null-terminated sequence
```



**\#\#\#\# Example 1: Minimal**



```C++
#include <iostream>
#include <string>

int main() {
    std::string rank = "rank";
    rank.push_back('7');
    std::cout << rank << "\n";
    return 0;
}
```



**\#\#\#\# Example 2: Basic \(chess — SAN fragment as \`string\`\)**



```C++
#include <iostream>
#include <string>

int main() {
    std::string move = "Nf3";
    for (char ch : move) {
        std::cout << ch << " ";
    }
    std::cout << "\n";
    return 0;
}
```



**\#\#\#\# Example 3: Structured \(\`vector\<string\>\` move list\)**



```C++
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> moves;
    moves.push_back("e4");
    moves.push_back("e5");
    moves.push_back("Nf3");
    for (const std::string& m : moves) {
        std::cout << m << " ";
    }
    std::cout << "\n";
    return 0;
}
```



**\#\#\# Step 4: Examples \(worked\) \| 示例（详解）**



**\#\#\#\# Example 4: \`find\` and \`npos\`**



```C++
#include <iostream>
#include <string>

int main() {
    std::string placement = "Qd1 Ke1";
    std::size_t pos = placement.find("Q");
    if (pos == std::string::npos) {
        std::cout << "no queen token\n";
    } else {
        std::cout << "Q at index " << pos << "\n";
    }
    return 0;
}
```



`std::string::npos` is a special **no\-match** value \(larger than any valid index\)\.



**\#\#\#\# Example 5: Longest name in \`std::vector\<std::string\>\`**



```C++
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> names = {"Alice", "Bob", "Carol"};
    std::size_t best = 0;
    for (std::size_t i = 1; i < names.size(); ++i) {
        if (names[i].size() > names[best].size()) {
            best = i;
        }
    }
    std::cout << "longest: " << names[best] << "\n";
    return 0;
}
```



**\#\#\#\# Example 6: One line of input with \`getline\`**



```C++
#include <iostream>
#include <string>

int main() {
    std::string line;
    std::cout << "Enter moves: ";
    if (std::getline(std::cin, line)) {
        std::cout << "read: " << line << "\n";
    }
    return 0;
}
```



**After this section \| 本节检查点**: You can relate **\*\*\`s\.size\(\)\`\*\*** to **\*\*\`std::strlen\(s\.c\_str\(\)\)\`\*\*** for normal strings, and give one example where a saved **\*\*\`c\_str\(\)\` pointer becomes invalid\*\*** after modifying \`s\`\.



*End of Chapter 8*



