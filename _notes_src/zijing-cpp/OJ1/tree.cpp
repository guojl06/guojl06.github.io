//  我是傻弗啊哥们
// 退化了，哥们。
#include<iostream>
int n;
int tmp,min=100000,max=0,profit=0;
int main(){

    std::cin >> n;
    for(int i=1;i<=n;i++){
        std::cin >> tmp;
        if(min > tmp) {min=tmp;max=tmp;continue;}
        if(tmp > max){max=tmp;if(profit < max - min) profit=max-min;}
    }
    std::cout << profit;

    return 0;
}