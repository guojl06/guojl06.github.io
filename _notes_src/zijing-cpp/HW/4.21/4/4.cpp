#include<iostream>
#include<string>
#include<cmath>
using namespace std;

string Move(string piece,int x1,int y1,int x2,int y2){
    if(piece=="king")
        if(abs(x1-x2)+abs(y1-y2)==1 || (abs(x1-x2)==abs(y1-y2) && abs(x1-x2)==1))
            return "Yes";
    if (piece=="queen")
        if((x1 == x2 && y1 != y2) || (y1 == y2 && x1 != x2) || (abs(x1-x2)==abs(y1-y2) && x1 != x2))
            return "Yes";
    if (piece=="rook")
        if((x1 == x2 && y1 != y2) || (y1 == y2 && x1 != x2))
            return "Yes";
    if (piece=="bishop")
        if(abs(x1-x2)==abs(y1-y2) && x1 != x2)
            return "Yes";
    if (piece=="knight")
        if((abs(x1-x2)==2 && abs(y1-y2)==1)||(abs(x1-x2)==1 && abs(y1-y2)==2))
            return "Yes"; 
    if (piece=="pawn")
        if(x2-x1==1 && y1==y2)
            return "Yes";   
    return "No";
}

int main(){

    int n,m,Q,x1,y1,x2,y2;
    string piece;
    cin >> n >> m >> Q;
    while(Q--){
        cin >> piece >> x1 >> y1 >> x2 >> y2;
        // cout << piece << ' ' << x1 << ' ' << y1 << ' ' << x2 << ' ' << y2 << '\n';
        if(x1 < 1 || x1 > n || x2 < 1 || x2 > n || y1 < 1 || y1 > m || y2 < 1 || y2 > m) cout << "No" << '\n';
        else cout << Move(piece,x1,y1,x2,y2) << '\n';
    }

    return 0;
}

//无敌了全弱智错误