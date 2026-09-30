这是说明版

若对编译命令无特殊说明，所有题在编译时默认添加选项 --std=c++11

1.【单选】以下代码的输出结果是
```cpp
#include <iostream>
using namespace std;

class Base {
public:
    Base() { cout << "B() "; }
    Base(const Base&) { cout << "B& "; }
    virtual ~Base() { cout << "~B "; }
    virtual void who() { cout << "Base "; }
};

class Derived : public Base {
public:
    Derived() { cout << "D() "; }
    ~Derived() { cout << "~D "; }
    void who() override { cout << "Derived "; }
};

void show(Base b) { b.who(); }

int main() {
    Derived d;
    show(d);
    Base* p = &d;
    p->who();
    return 0;
}
```
A. B() D() Derived ~B Derived ~D ~B

B. B() D() B& Base ~B Derived ~D ~B

C. B() D() B& Derived ~B Derived ~D ~B

D. B() D() Base ~B Derived ~D ~B

**注意到：对象切片调用拷贝构造函数 Base(const Base&)！！！！**

B

2.【多选】关于下列代码，说法正确的是 **\*\*\*\*\***
```cpp
#include <iostream>
using namespace std;

class Base {
public:
    virtual void f() { cout << "Base::f()" << endl; }
    virtual void f(int) { cout << "Base::f(int)" << endl; }
    void f(double) { cout << "Base::f(double)" << endl; }
};

class D1 : public Base {
public:
    using Base::f;
    void f(int) override { cout << "D1::f(int)" << endl; }
};

class D2 : public Base {
public:
    void f(int) override { cout << "D2::f(int)" << endl; }
};

int main() {
    D1 d1; D2 d2;
    d1.f();     // (1)
    d1.f(1.0);  // (2)
    d2.f();     // (3)
    d2.f(1.0);  // (4)
    Base* pb = &d2;
    pb->f(1.0); // (5)
    return 0;
}
```
A. (1) 处通过 using Base::f 使 Base::f() 在 D1 中可见，输出 Base::f()

B. (2) 处调用 Base::f(double)，输出 Base::f(double)

C. (3) 处能编译通过，调用 Base::f()

D. (4) 处由于 D2 中名字 f 隐藏了基类所有 f，1.0 被隐式转换为 int，调用 D2::f(int)

E. (5) 处 pb 是 Base*，调用 Base::f(double)（非虚函数、静态绑定）

**子类的 f(int) 会把基类中所有的 f 名字全部屏蔽掉。对于 d2 来说，它的作用域里现在只有一个函数：f(int)。**

**当你使用父类指针 pb 调用时，编译器是从 Base 的作用域开始看的：！！！！！非虚函数的调用是在编译期根据指针类型（静态类型）决定的。由于 pb 是 Base*，它直接绑定到 Base::f(double)。**

ABDE

3.【单选】以下代码的输出是 \*
```cpp
#include <iostream>
using namespace std;

template <typename T>
void f(T, T) { cout << "1 "; }

template <typename T, typename U>
void f(T, U) { cout << "2 "; }

void f(int, int) { cout << "3 "; }

int main() {
    f(1, 2);          // (a)
    f(1.5, 2.5);      // (b)
    f(1, 2.0);        // (c)
    f<double>(1, 2);  // (d)
    return 0;
}



```
**完全匹配的普通函数（非模板） > 2. 完全匹配的特化/模板函数 > 3. 需要进行自动转换的普通函数。**

**对于 (d)：显式指定参数后，模板 2 的灵活性让它产生了比模板 1 更少的转换需求。**
A. 3 1 2 2

B. 1 1 2 1

C. 3 1 3 1

D. 2 2 2 2

A

4.【多选】关于下列代码，说法正确的有
```cpp
#include <iostream>
using namespace std;

class Shape {
public:
    virtual double area() const = 0;
    virtual void name() const { cout << "Shape "; }
    virtual ~Shape() = 0;
};

Shape::~Shape() { cout << "~Shape "; }

class Circle : public Shape {
    double r;
public:
    Circle(double r_) : r(r_) {}
    double area() const override { return 3.14 * r * r; }
    void name() const override {
        Shape::name();
        cout << "Circle ";
    }
    ~Circle() { cout << "~Circle "; }
};

int main() {
    Shape* s = new Circle(5.0); delete s;
    return 0;
}
```
A. Shape 是抽象类，可以拥有带函数体的纯虚析构函数，且该函数体必须在类外定义

B. 由于 Shape 的析构函数是纯虚函数，Circle 类也必定是抽象类

C. 上述代码运行时，先输出 ~Circle 再输出 ~Shape

D. Circle::name() 中可以通过 Shape::name() 显式调用基类版本，即使 name 是虚函数

E. 若把 Shape::~Shape() 在类外的定义删除，上述代码在链接阶段会报错

**函数体：普通的纯虚函数通常不需要函数体，但纯虚析构函数必须提供函数体。这是因为子类在析构时，无论如何都会层层向上调用父类的析构函数。如果没有函数体，链接时就会找不到实现**

**类外定义：语法规定，纯虚函数的函数体必须定义在类定义体之外（不能直接写在类内大括号里）。**

ACDE

5.【多选】关于下列代码，说法正确的是
```cpp
#include <iostream>
using namespace std;

class Animal {
public:
    virtual void speak() { cout << "Animal "; }
    virtual ~Animal() {}
};

class Dog : public Animal {
public:
    void speak() override { cout << "Dog "; }
    void fetch() { cout << "fetch "; }
};

class Cat : public Animal {
public:
    void speak() override { cout << "Cat "; }
};
```
A. Animal* a = new Cat(); Dog* d = dynamic_cast<Dog*>(a); 得到的 d 为 nullptr

B. Animal* a = new Cat(); Dog* d = static_cast<Dog*>(a); 无法通过编译

C. Cat c; Animal& r = c; Dog& d = dynamic_cast<Dog&>(r); 会抛出 std::bad_cast 异常

D. dynamic_cast 要求源类型必须是多态类型（含虚函数），否则编译错误

E. Dog* d = new Dog(); Animal* a = static_cast<Animal*>(d); 编译通过且安全

**指针失败变空（nullptr），引用失败报警（异常）；静转（static）不管死活，动转（dynamic）必须有虚。**

ACDE

6.【单选】关于下列代码，说法错误的是
```cpp
class Base {
public:
    virtual Base* clone() const { return new Base(*this); }
    virtual void f() { }
    virtual void g() final { }
    virtual ~Base() = default;
};

class Derived : public Base {
public:
    Derived* clone() const override { return new Derived(*this); }
    void f() override { }
};
```
A. Derived::clone() 的返回类型与 Base::clone() 不同仍能构成重写覆盖，这是协变返回类型

B. 在 Derived 中添加 void g() override {} 会导致编译错误，因为 Base::g() 被 final 修饰

C. 若将 Base::clone() 返回类型改为 Base&，Derived::clone() 返回类型改为 Derived&，仍能构成协变返回

D. 若 Derived 中写 void f() const override {}，能覆盖 Base::f()，因为 const 只是限定符，不影响重写

D

要构成虚函数重写，必须满足：

函数名相同。

参数列表完全相同（包括参数个数、类型、顺序）。

常量性（const 属性）必须完全相同。

唯一的例外：就是 A 和 C 提到的返回类型可以在满足继承关系的指针或引用间“协变”。

7.【多选】关于下列代码，说法正确的是
```cpp
#include <iostream>
using namespace std;

template <typename T, typename U = int>
class Box {
    T a; U b;
public:
    Box(T x, U y) : a(x), b(y) {}
    void show() { cout << a << "," << b << " "; }
};

template <>
class Box<double, double> {
    double a, b;
public:
    Box(double x, double y) : a(x), b(y) {}
    void show() { cout << "DD:" << a + b << " "; }
};

int main() {
    Box<int> b1(1, 2);                // (1)
    Box<double> b2(1.5, 2);           // (2)
    Box<double, double> b3(1.5, 2.5); // (3)
    b1.show(); b2.show(); b3.show();
    return 0;
}
```
A. (1) 处 Box<int> 中模板参数 U 取默认值 int，等价于 Box<int, int>

B. (2) 处 Box<double> 会匹配到 Box<double, double> 的特化版本，输出 DD:3.5

C. 程序的输出是 1,2 1.5,2 DD:4

D. 若删除 Box<double, double> 的特化定义，(3) 处仍可通过主模板正常工作

E. 类模板可以有默认模板参数，但类模板不能像函数模板那样被重载

ACDE

8.【单选】下列关于函数模板和类模板的描述中，错误的是

A. 定义函数模板时，template <typename T> 与 template <class T> 作用完全相同，typename 可以替换为 class

B. 对模板的处理发生在编译期——每当编译器遇到对模板的一种参数的使用，就会生成对应参数的一份代码，因此模板的声明与定义通常必须一起放在头文件中

C. 类模板的"非类型参数"（如 template<typename T, unsigned size> 中的 size）必须在编译期就能确定，可以是整型常量或字面值，但不能使用在运行时才有取值的普通变量

D. 对于函数模板 template<typename T> T sum(T a, T b)，当两个实参类型不一致时，编译器会自动将较窄的类型提升为较宽的类型来推导 T，例如 sum(9, 2.1) 会被推导成 T = double 并正常编译运行

D