#include<iostream>
#include<vector>
using namespace std;
int v,e;

int vnum[15]={0},edges[55];
int book[15]={0};
vector<int> ans;
int tail=0;

void dfs(int curNode){
    // cout << curNode << '\n';
    book[curNode]=1;
    ans.push_back(curNode);
    if(curNode==v-1){
        for(auto x:ans){
            cout << x;
            if(x!=v-1) cout << "->";
        }
        cout << '\n'; 
    }
    else {
        for(int i=vnum[curNode];i<vnum[curNode+1];i++){
            if(!book[edges[i]]&&edges[i]!=tail){
                dfs(edges[i]);
            }
        }
    }
    book[curNode]=0;
    tail=ans.back();
    ans.pop_back();
    return;
}

int main(){

    cin >> v >> e;

    for(int i=0;i<=v;i++) cin >> vnum[i];
    for(int i=0;i<e;i++) cin >> edges[i];
    dfs(0);
    

    return 0;
}