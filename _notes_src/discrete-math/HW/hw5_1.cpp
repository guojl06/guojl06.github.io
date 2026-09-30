// 孩子们我第一次试着来啊，来看看便宜算法什么东西！
#include<iostream>
#include<cmath>
#include<vector>
#include<map>
#include<algorithm>
using namespace std;

int w[6][6]={10000};
int n,m;
int tot=0;
vector<int> S;
vector<int> T;
map<int,pair<int,int>> Tp;

int main(){

    
    cin >> n >> m;
    T.push_back(1);T.push_back(1);Tp[1]=make_pair(1,1);
    cout <<'\n' <<1;
    for(int i=1;i<=n;i++) {
        w[i][i]=0;
        if(i!=1) S.push_back(i);
    }
    for(int i=1;i<=m;i++){
        int t1,t2,t3;
        cin >> t1 >> t2 >> t3;
        w[t1][t2]=t3,w[t2][t1]=t3;
    }

    int mval,ti,tj;
    while(!S.empty()){
        mval=10000;
        for(auto i:T){
            for(auto j:S){
                if(mval>w[i][j]){mval=w[i][j];ti=i,tj=j;}
            }
        }
        int t1=Tp[ti].first,t2=Tp[ti].second,t3;
        if(w[ti][t1]+w[ti][tj]+w[tj][t2]<w[ti][t2]+w[ti][tj]+w[tj][t1]){
            Tp[ti].second=tj;Tp[t2].first=tj;
            Tp[tj].first=ti,Tp[tj].second=t2;
            t3=t2;
            tot=tot-w[ti][t2]+w[ti][tj]+w[tj][t2];
        }
        else{
            Tp[ti].first=tj;Tp[t1].second=tj;
            Tp[tj].first=t1,Tp[tj].second=ti;
            t3=t1;
            tot=tot-w[ti][t1]+w[ti][tj]+w[tj][t1];
        }
        S.erase(remove(S.begin(), S.end(), t3), S.end());
        T.push_back(t3);
        cout << "->" << t3;

    }
    cout << '\n' << tot;
}