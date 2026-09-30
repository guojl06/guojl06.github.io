// 真忘差不多了我去

#include<iostream>
#include<queue>
#include<vector>
#include<unordered_map>
#include<algorithm>
using namespace std;

int n,m;
queue<int> ans;
unordered_map<int, vector<int>> edge;
int book[15];
int step=0;

int main(){

    for(int i=0;i<15;i++) book[i]=-1;
    cin >> n >> m;
    for(int i=1;i<=m;i++){
        int t1,t2;
        cin >> t1 >> t2;
        edge[t1].push_back(t2);
    }
    for(int i=0;i<n;i++){
        sort(edge[i].begin(),edge[i].end());
    }
    // for(int i=0;i<n;i++){
    //     for(auto x:edge[i])
    //         cout << x << ' ';
    //     cout << '\n';
    // }

    ans.push(0);
    bool flag=false;
    while(!ans.empty()&&!flag){
        int size=ans.size();
        for(int i=1;i<=size&&!flag;i++){
            for(auto x:edge[ans.front()]){
                // cout << x << ' ' << book[x] << '\n';
                if(book[x]<0 && x != 0){
                    ans.push(x);
                    book[x]=ans.front();
                    if(x==n-1){
                        flag=true;
                        break;
                    }
                }
            }
            ans.pop();
        }
        // cout << ans.back() << '\n';
    }

    // cout << ans.back() << '\n';
    if(!flag) cout << 0 << '\n';
    else{
        vector<int> res;
        int t=n-1;
        while(t!=-1){
            res.push_back(t);
            t=book[t];
        }
        int size=res.size();
        for(int i=1;i<=size;i++){
            cout << res.back();
            if(i<size) cout << "->";
            res.pop_back();
        }
        cout << '\n';
    }


    return 0;
}