#include "my_lib.h"

using namespace std;

int main() {
    string hello = "Hello, oop!";
    print(hello);
    print();
    print(2333);
    print(233 > 666);
    print("================");

    auto s = input();
    print(s);
    for (auto c:s) print(c);
    print("================");

    Array a;
    a.append(4);
    a.append(2);
    a.append(7);
    a.pop();
    a.append(5);
    print(a.getSize());
    print(a);
    return 0;
}
