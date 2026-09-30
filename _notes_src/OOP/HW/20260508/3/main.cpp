#include <iostream>
#include <string>
#include "Value.h"
#include "Constant.h"
#include "Sub.h"
#include "Plus.h"
#include "Multiply.h"
int n;
Value *v[100001];
std::string s;
int main()
{
    std::cin >> n;
    int a, b;
    for(int i = 1; i <= n; ++i)
    {
        std::cin >> s;
        if(s == "Constant")
        {
            int temp;std::cin >> temp;
            v[i]=new Constant(temp);
        }
        else if(s == "Plus")
        {
            int t1,t2;std::cin >> t1 >> t2;
            v[i]=new Plus(v[t1],v[t2]);
        }
        else if(s == "Sub")
        {
            int t1,t2;std::cin >> t1 >> t2;
            v[i]=new Sub(v[t1],v[t2]);
        }
        else if(s == "Multiply")
        {
            int t1,t2;std::cin >> t1 >> t2;
            v[i]=new Multiply(v[t1],v[t2]);
        }
        else if(s == "Print")
        {
            int temp;std::cin >> temp;
            v[i]=v[temp];
            std::cout << v[i]->calc() << '\n';
        }
        else if(s == "Modify")
        {
        	int t,a;std::cin >> t >> a;
            delete v[t];
            v[t] = new Constant(a);
            v[i] = v[t];
        }
    }
	return 0;
}
