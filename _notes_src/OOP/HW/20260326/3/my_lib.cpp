#include "my_lib.h"

void print(int x) {
    std::cout << x << std::endl;
}

void print(bool x) {
    std::cout << (x ? "True" : "False") << std::endl;
}

void print(std::string s) {
    std::cout << s << std::endl;
}

void print(const char* s) {
    std::cout << s << std::endl;
}

void print(char c) {
    std::cout << c << std::endl;
}


Input input(){
    return Input{};
}

void print(Input i) {
    std::cout << i.cached << std::endl;
}


// Array

void Array::append(int x) { a[size++] = x; }

void Array::pop() { size--; }

int Array::getSize() { return size; }

void print(Array a) {
    for (int i = 0; i < a.getSize(); i++)
        std::cout << a[i] << (i == a.getSize() - 1 ? '\n' : ' ');
}
