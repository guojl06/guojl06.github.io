#include <iostream>
#include <string>
using namespace std;

// 函数重载声明
void printTemp(int t);
void printTemp(double t);
void printTemp(string t);

int main() {
    printTemp(25);      
    printTemp(36.5);    
    printTemp("Normal");  

    return 0;
}

// 函数重载定义
void printTemp(int t) {
    cout << "Temperature (int): " << t << endl;
}

void printTemp(double t) {
    cout << "Temperature (double): " << t << endl;
}

void printTemp(string t) {
    cout << "Temperature status: " << t << endl;
}
