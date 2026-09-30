// 这么小数据范围那还说啥了，桶
// 烫完了。
#include<iostream>
using namespace std;

int n,k,t,tot=0;
int a[5001]={0};

int main(){

    cin >> n >> k;
    for(int i=1;i<=n;i++){
        cin >> t;a[t]++;
    }
    for(int i=1;i<=5000;i++){
        tot+=a[i];
        if(tot >= k){cout<<i;break;}
    }

    return 0;
}