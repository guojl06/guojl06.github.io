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
