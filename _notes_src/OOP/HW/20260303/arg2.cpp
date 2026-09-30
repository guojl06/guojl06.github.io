#include<iostream>
#include<cstdio> //atoi

// using of argv & argc
int ADD(int a,int b);
//former definition!
int main(int argc, char** argv){

    //argc: num of argv
    //argv: 0 is name of exe, others are your input value
    //we can make it to have error detect
    if(argc != 3){
        std :: cout << "Usage:" << argv[0] << " op1 op2 \n";
        return 1;
    }
    int a,b;
    a = atoi(argv[1]);
    b = atoi(argv[2]);
    std :: cout << a+b << "\n";

    return 0;
}