#include "Map.h"

Map::Map(int n){
    sz=0;
    data=new Pair[n];
    //。。。一堆未定义行为，闹马力。！！！我是弱智！！！
}

Map::~Map(){
    delete[] data;
    // 。。。一起删掉！
}

int & Map::operator[](const string & k){
    Pair * tp = data;
    for(int i=0;i<size();i++,tp++){
        if(tp->hasKey(k)){
            return tp->getVal();
        }
    }
    tp=data+sz;
    tp->reset(k,0);
    sz++;
    return tp->getVal();
}

int Map::operator[](const string & k) const{
    Pair * tp = data;
    for(int i=0;i<size();i++,tp++){
        if(tp->hasKey(k)){
            return tp->getVal();
        }
    }
    return 0;
}

int Map::size() const{
    return sz;
}