// 我不知道啊，我开始筛了
// 原来被vector坑了，气死我了
#include <iostream>
#include<vector>
int n,tot=0;
int cnt;
int vis[10001]={0};
int prime[10001]={0};
int main(){

    std::cin >> n;
    for(int i=2;i<=n;i++){
        if(!vis[i]){ prime[++tot]=i;}
        // 无敌了，这错了
        for(int j=1;j<=tot && i*prime[j]<=n;j++){    
            vis[i*prime[j]]=1;
            if(i % prime[j] == 0) break;
        }
    }
    for(cnt=2;cnt<=n && !(!vis[cnt] && !vis[n-cnt]);cnt++);
    std::cout << cnt << ' ' << n-cnt;
    return 0;
}