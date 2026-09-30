#include<iostream>
using namespace std;

long long T,n,t1,t2,t;
int main(){

    cin >> T;
    while(T--){
        cin >> n;
        if(n==0 || n==1) cout << 1 << '\n';
        else{
            t1=1,t2=1;
            for(int i=2;i<=n;i++){
                t=t1+t2;
                t1=t2;t2=t;
                // cout << t1 << ' ' << t2 << ' ' <<t << '\n';
            }
            cout << t << '\n';
        }
    }

    return 0;
}