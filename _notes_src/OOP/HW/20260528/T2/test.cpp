#include<iostream>
#include<vector>
#include<cmath>
#include"myqueriable.h"

using namespace std;

int main(){
    vector<float> vec = {2.0, 3.0, 4.0, 5.0};
    auto it = from(vec)
        .apply([](float x){return sqrt(x);});
    for(auto x: it){
        cout << x << endl;
    }
}
