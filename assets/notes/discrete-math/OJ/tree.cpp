// 真忘差不多了我去
#include<iostream>
#include<algorithm>
using namespace std;

int n,m;
int father=-1;
int fa[5005];
int res=0,cnt=0;

struct Edge{
    int u,v,w;
}e[200005];

bool cmp(Edge &e1,Edge &e2){
    return e1.w < e2.w;    
}

int find(int num){
    if(fa[num]==num) return num;
    return fa[num] = find(fa[num]);
}

int main(){
    cin >> n >> m;

    for(int i=1;i<=n;i++) fa[i]=i;

    for(int i=1;i<=m;i++){
        cin >> e[i].u >> e[i].v >> e[i].w;
    
    }
    sort(e+1,e+m+1,cmp);
    for(int i=1;i<=m;i++){
        int fu=find(e[i].u),fv=find(e[i].v);
        if(fu!=fv){
            res+=e[i].w;
            fa[fu]=find(fv);
            cnt++;
        }
        if(cnt==n-1){
            cout << res;
            return 0;
        }
    }
    cout << -1;

    return 0;
}