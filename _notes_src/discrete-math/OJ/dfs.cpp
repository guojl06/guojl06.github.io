// 教训：读完题再他妈做，第一不去重，第二不排序，你咋不去死

#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;
int v,e;

int vnum[15]={0},edges[55];
int book[15]={0};
vector<int> ans;
int cnt=0;

void dfs(int curNode){

    // cout << curNode << '\n';
    book[curNode]=1;
    ans.push_back(curNode);
    if(curNode==v-1){
        for(auto x:ans){
            cout << x;
            if(x!=v-1) cout << "->";
            cnt++;
        }
        cout << '\n'; 
    }
    else {
        int tr[15]={0};
        for(int i=vnum[curNode];i<vnum[curNode+1];i++){
            if(!book[edges[i]]&&!tr[edges[i]]){
                tr[edges[i]]=1;
                dfs(edges[i]);
            }
        }
    }
    book[curNode]=0;
    ans.pop_back();
    return;
}

int main(){

    cin >> v >> e;

    for(int i=0;i<=v;i++) cin >> vnum[i];
    for(int i=0;i<e;i++) cin >> edges[i];
    // 去重!!!!之后居然还要排序！!!!!!!!!
    for(int i=0;i<v;i++){
        sort(edges+vnum[i],edges+vnum[i+1]);
    }
    dfs(0);
    if(cnt==0) cout << 0 <<'\n';

    return 0;
}