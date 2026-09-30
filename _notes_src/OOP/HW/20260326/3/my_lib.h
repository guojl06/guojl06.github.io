#ifndef MY_LIB_H
#define MY_LIB_H

#include <iostream>
#include <sstream>
#include <string>

void print(int x);

void print(bool x);

void print(std::string s = "");

void print(const char* s);

void print(char c);



class Array {
    int size{};
    int a[100]{};
public:
    void append(int x);

    void pop();

    int getSize();

    int operator[](int i){
        return a[i];
    }

};

class Input {
public:
    std::string cached;
    Input() { std::cin >> cached; }

    template <typename T>
    operator T() {
        std::stringstream ss(cached);
        T val;
        ss >> val;
        return val;
    }

    std::string::const_iterator begin() const { return cached.begin(); }
    std::string::const_iterator end() const { return cached.end(); }
};

Input input();

void print(Input i);

void print(Array a);

#endif
