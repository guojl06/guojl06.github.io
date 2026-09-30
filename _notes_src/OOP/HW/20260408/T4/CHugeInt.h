#pragma once
#include <cstring>
#include <iostream>
using namespace std;

const int MAX = 220; 
class CHugeInt {
    int digit[MAX]={0};
    int sz=0;
    public:
        friend ostream& operator<<(ostream &os,const CHugeInt &num);
        
// 构造函数，用于从字符串初始化CHugeInt对象
// 接收一个const char*类型的字符串参数s
        CHugeInt(const char* s);
        CHugeInt(const int n);
        CHugeInt operator+(CHugeInt& b);
        CHugeInt operator+(int& b);
        CHugeInt& operator+=(CHugeInt& b);
        CHugeInt& operator+=(int& tmp);
        CHugeInt& operator++();
        CHugeInt& operator++(int);

        friend CHugeInt operator+(int &tmp,CHugeInt &a);

        const int size()const;
        // const int getDigit(int index){}
        void changeDigit(int index);
// 在此处补充你的代码
};

ostream& operator<<(ostream &os,const CHugeInt &num);