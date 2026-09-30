# OOP 第四次作业

> 来源：TUOJ - 面向对象程序设计基础（黄民烈老师）2026春
> Contest: https://oj.cs.tsinghua.edu.cn/course/90/contest/1002

---

## T1 模拟动物

**题目链接：** https://oj.cs.tsinghua.edu.cn/course/90/contest/1002/problem/1

你需要使用 C++ 继承和多态的特性来模拟动物。有以下一段代码：

**main.cpp**

```cpp
string name1, name2;
cin >> name1 >> name2;

Animal *myBird = new Bird(name1), *myFish = new Fish(name2);

myBird->action();
myFish->action();

delete myBird;
delete myFish;
```

**Bird 和 Fish 类都已经写好**

```cpp
class Bird: public Animal
{
public:
    using Animal::Animal;
    ~Bird() {
        std::cout << "bird " << name << " has gone." << std::endl;
    }
    void speak() {
        std::cout << "bird " << name << " is singing." << std::endl;
    }
    void swim() {
        std::cout << "bird " << name << " can't swim." << std::endl;
    }
};
class Fish: public Animal
{
public:
    using Animal::Animal;
    ~Fish() {
        std::cout << "fish " << name << " has gone." << std::endl;
    }
    void speak() {
        std::cout << "fish " << name << " can't speak." << std::endl;
    }
    void swim() {
        std::cout << "fish " << name << " is swimming." << std::endl;
    }
};
```

你需要补充头文件 `animal.h`，使得程序能够编译通过。

### 输入说明

输入是两个字符串，分别是 bird 和 fish 的名字。

### 输出说明

输出一共六行，请观察样例。

### 输入样例

```
alice bob
```

### 输出样例

```
bird alice is singing.
bird alice can't swim.
fish bob can't speak.
fish bob is swimming.
bird alice has gone.
fish bob has gone.
```

### 提交格式

你只能提交头文件 `animal.h`，请以压缩包 `.zip` 形式上传。

我们会将你提交的文件和我们预先设置好的 `main.cpp`, `bird.h`, `fish.h` 一起编译运行。

### 评分标准

一共两个测试点，每个测试点占 50%。为避免你不去使用 Bird 和 Fish 中的函数，在第二个测试点中，我们会略微修改 Bird 和 Fish 中的字符串，以检查你是否真正完成了设计。

本题 100% 为 OJ 评分。

---

## T2 计算图

**题目链接：** https://oj.cs.tsinghua.edu.cn/course/90/contest/1002/problem/2

### 题目描述

计算图描述了一种计算方式：一个计算图可以看做一个有向无环图，其中每个结点要么是一个常数，要么是一个运算符。一个常数结点入度为 0，其值是一个可设定的常数。一个运算符结点入度为其运算数个数，其值为入结点经过该运算符运算后的值。

本题中要求你实现一个非常简单的运算图，支持常数和加法、减法、乘法三种运算符。例如：加法运算的结点入度为 2，其值为两个运算符的和。

我们提供了计算图的结点类 `Value` 和运算符结点类 `Operator` 的定义，请你完善其实现，并以其为基础实现常数节点以及加法、减法、乘法运算符。

在运算图上，我们还要求你支持两种操作：修改操作和输出操作。修改操作会修改一个常数节点的数值，而输出操作要求输出一个节点目前的数值。为了方便起见，如果之后的运算引用了操作所在的结点，我们强制定义操作所在的结点和它们修改或输出的结点一致。（如果你不理解，可以看样例的最后一个操作）。

提示：需要使用虚函数

### 输入格式

第一行为运算图中节点的个数 $n$。

接下来 $n$ 行，每行描述一个节点。首先是一个字符串，可能是 `Constant`、`Plus`、`Sub`、`Multiply`、`Modify`、`Print` 中的一个，分别表示常数节点、加法节点、减法节点、乘法节点和修改、输出操作。对于常数节点，之后是一个整数表示常数的数值。对于加法、减法、乘法节点，之后是两个整数表示两个操作节点。对于修改操作，之后是两个整数 $x$ 和 $a$，表示将 $x$ 常数节点的值修改为 $a$。对于输出操作，之后是一个整数 $x$ 表示输出节点 $x$ 的值。

注意第 $i$ 行描述的为 $i$ 号节点，其操作节点必定为小于 $i$ 的节点。

### 输出格式

对每个输出操作，输出对应节点的数值。

### 样例输入

```
9
Constant 1
Constant 2
Plus 1 2
Multiply 3 2
Sub 4 1
Print 5
Print 4
Modify 1 5
Print 6
```

### 样例输出

```
5
6
9
```

### 样例解释

- 1 号节点：常数节点，其值为 1
- 2 号节点：常数节点，其值为 2
- 3 号节点：加法运算节点，其运算节点为 1 号和 2 号，因此值为 $1+2=3$
- 4 号节点：乘法运算节点，其运算节点为 3 号和 2 号，因此值为 $3 \times 2=6$
- 5 号节点：减法运算节点，其运算节点为 4 号和 1 号，因此值为 $6-1=5$
- 6 号节点：输出操作，输出 5 号节点的值 5
- 7 号节点：输出操作，输出 4 号节点的值 6
- 8 号节点：修改操作，将 1 号节点的值修改为 5
- 9 号节点：输出操作，输出 6 号节点的值，由于我们的强制定义，实际上它就是 5 号节点（因为 6 号操作是输出 5 号节点的值）。现在它的值为 $(5+2) \times 2 - 5 = 9$

### 要求

- 不修改 `Value.h`、`Operator.h`
- 完善 `Operator.cpp`、`main.cpp` 中的实现
- 编写加法、减法、乘法、常数节点的类，并据此修改 Makefile

### 限制与约定

- $2 \le n \le 10000$
- 所有常数在 int 范围内。注意运算结果可能会超出这个范围，因此所有运算均使用 int 类型，以保证溢出一致
- 时间限制：1s，空间限制：256MB

### 提交格式

你应该将除 `Value.h`、`Operator.h` 以外的所有文件（至少包括一个 Makefile，生成的可执行文件名为 `main`）打包成一个 zip 压缩包并上传，我们会将 `Value.h`、`Operator.h` 复制进你上传的文件中编译并运行。

### 评分标准

OJ 评分占 100%

---

## T3 褪色者的锻造工坊

**题目链接：** https://oj.cs.tsinghua.edu.cn/course/90/contest/1002/problem/3

### 题目描述

《艾尔登法环 (Elden Ring)》是一款由日本开发商 From Software 开发、Bandai Namco 发行的黑暗幻想风格动作角色扮演游戏，玩家将扮演被称作"褪色者" (Tarnished) 的角色去战斗、探索、拯救或毁灭世界。不要慌，这个作业既不需要你玩过这款游戏，也不会让你开发这款游戏，只是需要你基于已有代码实现点儿简单的武器锻造模拟而已。

褪色者在游戏中会收集到各式各样的武器，并且会利用锻造石来强化它们。

武器分为普通武器 与失色武器，它们有各自的"武器名"。武器默认为零级，我们可以把它们强化到更高的等级，一般会在武器名后加上一个 `+x` 后缀表示（$x \ge 1$），为避免歧义我们将这种表示称作"扩展武器名"，特别的，没有强化过的武器的扩展武器名与武器名相同。

普通武器可以由普通锻造石 k (Normal Smithing Stone k) 可以锻造出 `+(3*k-2)` 到 `+(3*k)`，分别需要 2、4、6 个（$1 \le k \le 8$）普通锻造石 k。失色武器由 1 个失色锻造石 k (Somber Smithing Stone k) 可以锻造出 `+k`（$1 \le k \le 8$）。

例如一把普通武器匕首，可以通过 2 个普通锻造石 1 强化到 `+1`，此时它的扩展武器名会变为 `匕首+1`；接下来用 4 个普通锻造石 1、6 个普通锻造石 1、2 个普通锻造石 2 可以依次将它强化到 `匕首+2`、`匕首+3`、`匕首+4`。强化需要按照从低到高的顺序依次强化，不能跳步。

褪色者会把东西放到自己的物品栏中（即 Tarnished 的各个成员数组中的元素，用空指针表示物品栏为空），物品栏中的一个格子可以存放若干个同一种锻造石或者一把武器（不存在同名武器）。物品栏不会显示数量为 0 的物品，因此如果某种锻造石消耗一空，则你应该销毁（析构）对应的物品（对象）。

### 你需要完成的事情

- 实现普通武器类 `NormalWeapon` 和失色武器类 `SomberWeapon`，它们继承自基类武器类 `Weapon`
- 实现普通锻造石类 `NormalSmithingStone` 和失色锻造石 `SomberSmithingStone`，它们继承自基类锻造石类 `SmithingStone`
- 褪色者类 `Tarnished` 的定义已经给出，它将由普通/失色武器/锻造石类进行组合，你需要完成它的成员函数定义
- 所有操作结束后，褪色者会销毁（析构）所有物品，销毁不同武器时，按照获得顺序析构；销毁不同等级锻造石时，按照等级从低到高顺序销毁；总的销毁顺序为普通锻造石、失色锻造石、普通武器、失色武器
- 所有框架函数中实现的基类（即 `Weapon` 与 `SmithingStone`）的非常量成员函数（包括构造/析构函数、`Weapon::upgrade`、`SmithingStone::add_amount`）在被外部调用时都应该有新的输出
- 根据格式说明、样例展示和设计模式在你的程序的合适位置进行输出

### 输入格式

第一行输入两个正整数 $n$ 和 $m$，表示有 $n$ 次操作，全局 magic number 为 $m$。

接下来有 $2n$ 行输入，每 2 行为一次操作，一次操作内部第一行为一个数字 operation，第二行内容由 operation 决定：

- **operation = 0**：褪色者获得了若干锻造石。第二行有 3 个数字 `type, level, number`：type 为 0 表示普通锻造石，为 1 表示失色锻造石；level 表示锻造石等级，number 表示数量
- **operation = 1**：褪色者得了一把武器。第二行有一个数字 `type` 和一个字符串 `name`：type 为 0 表示普通武器，为 1 表示失色武器；name 表示武器名（仅由大小写字母组成，保证两两不同）
- **operation = 2**：褪色者试图强化一把武器。第二行有一个数字 `target` 和一个字符串 `name`
  - 强化成功：输出 `Upgrade <x> to <y> Successfully.`
  - 锻造石不足：输出 `Upgrade failed for lacking <xxx>.`（缺少的最低等级锻造石名字，如 `normal smithing stone 2`）
  - 没有该武器：输出 `You don't have the right!`
  - target 不大于武器当前等级：输出 `Stay calm!`

如果锻造石足够则成功强化并消耗锻造石；否则根本不强化。成功强化时注意每消耗一级的锻造石应立刻完成一级强化，不能一次消耗完连续强化若干级。

### 输出格式

输出内容即上述各类操作中的输出，一句话一行。

### 输入样例

```
13 1234
1
1 CrystalSword
2
1 ShortSord
1
0 ShortSord
0
0 1 12
2
4 ShortSord
2
2 ShortSord
0
0 2 7
2
5 ShortSord
2
4 ShortSord
0
1 1 2
0
1 2 1
0
1 3 1
2
2 CrystalSword
```

### 输出样例

```
[magic=1234] Weapon created: CrystalSword
Somber weapon CrystalSword was created.
You don't have the right!
[magic=1234] Weapon created: ShortSord
Normal weapon ShortSord was created.
[magic=1234] Smithing stone 1 was created
Normal smithing stone 1 was created.
[magic=1234] Smithing stone 1 from 0 to 12
Normal smithing stone 1 was added with 12.
Upgrade failed for lacking normal smithing stone 2.
[magic=1234] Smithing stone 1 from 12 to 10
Normal smithing stone 1 was subtracted with 2.
[magic=1234] Weapon upgraded: ShortSord
Normal weapon ShortSord was upgraded to ShortSord+1.
[magic=1234] Smithing stone 1 from 10 to 6
Normal smithing stone 1 was subtracted with 4.
[magic=1234] Weapon upgraded: ShortSord
Normal weapon ShortSord+1 was upgraded to ShortSord+2.
Upgrade ShortSord to ShortSord+2 Successfully.
[magic=1234] Smithing stone 2 was created
Normal smithing stone 2 was created.
[magic=1234] Smithing stone 2 from 0 to 7
Normal smithing stone 2 was added with 7.
[magic=1234] Smithing stone 1 from 6 to 0
Normal smithing stone 1 was subtracted with 6.
Normal smithing stone 1 was destroyed.
[magic=1234] Smithing stone 1(0) was destroyed
[magic=1234] Weapon upgraded: ShortSord
Normal weapon ShortSord+2 was upgraded to ShortSord+3.
[magic=1234] Smithing stone 2 from 7 to 5
Normal smithing stone 2 was subtracted with 2.
[magic=1234] Weapon upgraded: ShortSord
Normal weapon ShortSord+3 was upgraded to ShortSord+4.
[magic=1234] Smithing stone 2 from 5 to 1
Normal smithing stone 2 was subtracted with 4.
[magic=1234] Weapon upgraded: ShortSord
Normal weapon ShortSord+4 was upgraded to ShortSord+5.
Upgrade ShortSord+2 to ShortSord+5 Successfully.
Stay calm!
[magic=1234] Smithing stone 1 was created
Somber smithing stone 1 was created.
[magic=1234] Smithing stone 1 from 0 to 2
Somber smithing stone 1 was added with 2.
[magic=1234] Smithing stone 2 was created
Somber smithing stone 2 was created.
[magic=1234] Smithing stone 2 from 0 to 1
Somber smithing stone 2 was added with 1.
[magic=1234] Smithing stone 3 was created
Somber smithing stone 3 was created.
[magic=1234] Smithing stone 3 from 0 to 1
Somber smithing stone 3 was added with 1.
[magic=1234] Smithing stone 1 from 2 to 1
Somber smithing stone 1 was subtracted with 1.
[magic=1234] Weapon upgraded: CrystalSword
Somber weapon CrystalSword was upgraded to CrystalSword+1.
[magic=1234] Smithing stone 2 from 1 to 0
Somber smithing stone 2 was subtracted with 1.
Somber smithing stone 2 was destroyed.
[magic=1234] Smithing stone 2(0) was destroyed
[magic=1234] Weapon upgraded: CrystalSword
Somber weapon CrystalSword+1 was upgraded to CrystalSword+2.
Upgrade CrystalSword to CrystalSword+2 Successfully.
Normal smithing stone 2 was destroyed.
[magic=1234] Smithing stone 2(1) was destroyed
Somber smithing stone 1 was destroyed.
[magic=1234] Smithing stone 1(1) was destroyed
Somber smithing stone 3 was destroyed.
[magic=1234] Smithing stone 3(1) was destroyed
Normal weapon ShortSord+5 was destroyed.
[magic=1234] Weapon destroyed: ShortSord
Somber weapon CrystalSword+2 was destroyed.
[magic=1234] Weapon destroyed: CrystalSword
```

> 注：为便于区分，所有框架自带的输出都有 `[magic=xxxx]` 的前缀且末尾没有标点符号，你需要完成的输出则没有前缀且末尾有标点符号。

### 要求

- `main.cpp`、`tarnished.h`、`weapon.cpp/h`、`smithing_stone.cpp/h` 已经被预置，你不应也不能修改这些文件
- 在已有代码的基础上编写 `NormalWeapon`、`SomberWeapon`、`NormalSmithingStone`、`SomberSmithingStone`、`Tarnished` 类，请合理设计几个类的组合与继承关系
- 你需要提交 Makefile，且生成的可执行文件名为 `main`

### 限制与约定

- $1 \le n \le 1000$
- $0 \le type \le 1$
- $1 \le name.length \le 50$
- $1 \le number \le 100$
- $1 \le level \le 8$
- 对普通武器 $1 \le target \le 24$，对失色武器 $1 \le target \le 8$
