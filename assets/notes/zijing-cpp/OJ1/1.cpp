#include<iostream>
int main(){

    int a;
    do{
        std::cin >> a;
        if(a==42) return 0;
        std::cout << a << '\n';
    }while(1);

    return 0;
}