#include<iostream>
#include<vector>
#include<cmath>
#include"myqueriable.h"

using namespace std;

void test1(){
    vector<int> vec;
    for(int i = 0; i < 100; i++){
        vec.push_back(i);
    }
    int out = from(vec).sum();
    cout << out << endl;
}

void test2(){
    vector<int> arr = {53, 200, 36, 27};
    auto q = from(arr);
    for(auto item: q){
        cout << item << endl;
    }
}

void test3(){
    int prices[] = {100, 300, 2, 1000};
    auto out = from(prices).sum();
    cout << out << endl;
}

void test4(){
    vector<int> vec;
    for(int i = 0; i < 1000000; i++){
        vec.push_back(i * 2);
    }
    auto out = from(vec)
        .where([](int x){return x % 4 == 2;})
        .where([](int x){return x >= 20000;})
        .apply([](int x){return x * 3;})
        .where([](int x){return x <= 60024;})
        .sum();
    cout << out << endl;
}

void test5(){
    vector<int> vec = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    vector<float> vec2 = {1.0, 2.0, 3.0};
    int out1 = from(vec)
        .apply([](int x){return x + 1;})
        .apply([](int x){return x + 9;})
        .where([](int x){return x >= 15;})
        .apply([](int x){return x + 10;})
        .where([](int x){return x <= 28;})
        .sum();
    cout << out1 << endl;
    auto out2 = from(vec2)
        .apply([](float x){return sqrt(x);});
    for(float item: out2){
        cout << item << endl;
    }
}

int main(){
    test1();
    test2();
    test3();
    test4();
    test5();
    return 0;
}
