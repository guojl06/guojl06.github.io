#import "../module/myutils.typ":*
#show : conf

= HW: OOP

#outline()

== HW 1 #datetime(day:26,month:3,year:2026).display()

=== T1

==== 题 1：删除目录命令

*题目：* 删除名为 `temp` 的目录及其中所有文件和子目录，正确命令是？

*选项：*
- A. `rm temp`
- B. `rm -r temp` ✅
- C. `mkdir temp`
- D. `ls temp`

*答案：B*

*解析：*
- `rm` 默认只能删除文件，不能删除目录，会报错。
- `rm -r` 表示递归（recursive）删除，会删除目录本身及其所有内容。
- `mkdir` 是创建目录，`ls` 是列出目录内容，均与题意无关。

---

==== 题 2：多文件编译命令

*题目：* 项目包含 `main.cpp`、`math.cpp`、`math.h`，生成可执行文件 `calculator`，以下哪些命令正确？

*选项：*
- A. `g++ main.cpp math.cpp -o calculator` ✅
- B. `g++ -c main.cpp && g++ -c math.cpp && g++ main.o math.o -o calculator` ✅
- C. `g++ main.cpp -o calculator && g++ math.cpp -o calculator`
- D. `g++ -c main.cpp math.cpp && g++ -o calculator main.o math.o` ✅

*答案：A、B、D*

*解析：*

*A 正确：* 直接将两个源文件一起交给编译器，自动完成编译和链接。

*B 正确：* 先分别用 `-c` 编译为目标文件（`.o`），再手动链接。

*C 错误：* `g++ math.cpp -o calculator` 中 `math.cpp` 没有 `main` 函数，链接阶段会报错（找不到程序入口）。

*D 正确：* `g++ -c main.cpp math.cpp` 可以同时编译多个文件，分别生成 `main.o` 和 `math.o`；然后 `g++ -o calculator main.o math.o` 完成链接。

#block(fill: luma(240), inset: 8pt, radius: 4pt)[
  *注意 `-o` 的用法：* `-o` 后面紧跟的那一个参数是输出文件名，其余均为输入文件，与顺序无关。`g++ -o calculator main.o math.o` 和 `g++ main.o math.o -o calculator` 等价。
]

---

==== 题 3：缺少源文件的编译

*题目：* 有 `main.cpp`、`math_utils.cpp`、`math_utils.h` 三个文件，执行 `g++ main.cpp -o app`，结果是？

*选项：*
- A. 编译成功并输出 "Result: 12"
- B. 编译成功但运行时报错
- C. 编译失败 ✅
- D. 程序运行但没有任何输出

*答案：C*

*解析：*

`g++ main.cpp -o app` 只编译了 `main.cpp`，而 `multiply` 函数的**实现**在 `math_utils.cpp` 中，没有被包含进来。头文件只提供声明，不提供定义。

链接阶段会报：
```
undefined reference to `multiply`
```

这个错误发生在**生成可执行文件之前**，因此根本不会产生 `app`，不存在"运行时报错"的机会。选 C 而不是 B。

---

==== 题 4：类的成员函数调用

*题目：* 以下代码运行后输出结果是？

```cpp
Counter c;
c.reset();      // count = 0
c.increment();  // count = 1
c.increment();  // count = 2
c.decrement();  // count = 1
c.increment();  // count = 2
cout << c.getCount() << endl;
```

*选项：* A. 1　B. 2 ✅　C. 3　D. 4

*答案：B*

*解析：* 按序追踪 `count` 的值：0 → 1 → 2 → 1 → 2，最终输出 `2`。

---

==== 题 5：函数重载的类型匹配

*题目：* 以下代码调用哪个重载版本？

```cpp
printTemp(25);       // int 字面量
printTemp(36.5);     // double 字面量
printTemp("Normal"); // const char* → 隐式转换为 string
```

*选项：* A ✅　B　C　D

*答案：A*

*解析：*
- `25` 是 `int` 字面量，精确匹配 `printTemp(int)`。
- `36.5` 是 `double` 字面量，精确匹配 `printTemp(double)`。
- `"Normal"` 是 `const char*`，通过隐式转换匹配 `printTemp(string)`。

输出：
```
Temperature (int): 25
Temperature (double): 36.5
Temperature status: Normal
```

---

==== 题 6：运算符重载

*题目：* 关于 `Vector2D` 的 `operator+` 重载，哪个描述正确？

*选项：*
- A. `+` 不能被重载，代码无法编译
- B. `v1 + v2` 等价于 `v1.operator+(v2)` ✅
- C. 运算符重载函数必须声明为 `static`
- D. 重载会改变 `+` 对所有类型的含义

*答案：B*

*解析：*
- *A 错：* C++ 中绝大多数运算符都可以重载，`+` 完全可以。
- *B 正确：* `v1 + v2` 是 `v1.operator+(v2)` 的语法糖，这是运算符重载的本质。
- *C 错：* 成员函数形式的运算符重载不能是 `static`（需要访问 `this`）。
- *D 错：* 重载只对该类的对象生效，不影响内置类型（如 `int + int`）。

---

==== 题 7：无法编译的原因【多选】

*题目：* 以下代码无法编译的原因有哪些？

```cpp
class P {
    int data = 1;
    void func(P a);
    int func(int a, int b=1) { data += a - b; return data; }
    int func(int i, int j=2) { data += i + j; return data; }
    int func2(float i) { data += i; return data; }
};
void P::func(P a) { data += a.data; }

int main() {
    P a;
    a.func2(1);
    return 0;
}
```

*选项：*
- A. 没有设置成员变量、成员函数的访问权限 ✅
- B. `P` 中 `func(int, int)` 函数重复定义 ✅
- C. 类 `P` 的 `func(P a)` 中修改了私有成员变量
- D. `main()` 函数中调用了 `a` 的私有成员函数 ✅

*答案：A、B、D*

*各选项详细解析：*

*A ✅（原因）：* `class` 中默认访问权限是 `private`，代码没有写任何 `public:`，导致 `func2` 等所有成员全部私有。A 是 D 能成立的**根本原因**，题目问的是"原因"而非"错误本身"，因此 A 成立。

*B ✅（直接编译错误）：*
```cpp
int func(int a, int b=1) { ... }
int func(int i, int j=2) { ... }
```
两个函数的**参数类型列表完全相同**（都是 `int, int`），参数名不同不影响函数签名，构成重复定义，编译器无法区分。

*C ❌：* 成员函数内部访问同类任意对象的私有成员是**合法**的，不论是 `this->data` 还是 `a.data`（其中 `a` 也是 `P` 类型）。这是 C++ 的基本规则：访问控制以**类**为单位，而非以**对象**为单位。

*D ✅（直接编译错误）：* `func2` 是私有成员函数，`main` 在类外调用它会直接报编译错误。

---

==== 题 8：宏与内联函数

*题目：* 关于以下代码，哪个描述正确？

```cpp
#define SQUARE(x) ((x) * (x))

inline int square(int x) {
    return x * x;
}

int a = 5;
int result1 = SQUARE(a + 1);  // Line X
int result2 = square(a + 1);  // Line Y
```

*选项：*
- A. Line X 和 Line Y 都会产生相同的汇编代码
- B. Line X 和 Line Y 的执行结果不同
- C. `square` 函数不会被内联，因为复杂性超出编译器优化能力
- D. 宏 `SQUARE` 可能产生非预期副作用，而内联函数不会 ✅

*答案：D*

*各选项详细解析：*

*A 错：* `inline` 只是给编译器的**提示**，不保证一定内联展开。宏是文本替换，inline 函数是正常编译流程，两者生成的汇编**不一定相同**，不能说"必然相同"。

*B 错：* 本题中两者结果相同——`SQUARE(a+1)` 展开为 `((a+1)*(a+1))` = 36，`square(a+1)` = 36。

*C 错：* `square` 函数极其简单（单条 return），编译器完全有能力内联。

*D ✅：* 宏是纯文本替换，参数可能被**多次求值**，例如：
```cpp
SQUARE(a++)  // 展开为 ((a++) * (a++))，a 被自增两次 → 未定义行为
square(a++)  // 参数只求值一次，结果确定，行为安全
```
inline 函数和普通函数一样，参数只求值一次，不会有副作用问题。这是原理层面的结论，与编译器实现无关。
