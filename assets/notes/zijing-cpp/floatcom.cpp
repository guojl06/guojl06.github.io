#include<iostream>
#define eps 1e-9
int main(){

    float a,b;
    std::cin>>a>>b;
    std::cout<< (a-b> eps ? "x is greater than y" : (b-a > eps ? "x is less than y" : "x is equal to y"));

    return 0;
}
