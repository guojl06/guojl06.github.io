#pragma once

#include<iostream>
#include<vector>
#include<cmath>


template <typename T>
class MyQueriable{

    T *data;
    int size;
    
    public:
    
    MyQueriable(T *t,int _size): data(t),size(_size) {}

    // 我去，牛啊，使用迭代器就可以说明这个东西是我的auto对象
    using iterator = T*;
    iterator begin(){return data;}
    iterator end(){return data+size;}

    template <typename F>
    MyQueriable where(F f){
        int _size=0;
    
        for(T *it=data;it<data+size;it++){
            if(f(*it)){
                _size++;
            }
        }

        T *ret = new T[_size];
        T *temp= ret;
        for(T *it=data;it<data+size;it++){
            if(f(*it)){
                *temp=*it;
                temp++;
            }
        }

        return  MyQueriable<T>(ret,_size);
    }

    template <typename F>
    MyQueriable apply(F f){
        T *ret = new T[size];
        T *temp= ret;

        for(T *it=data;it<data+size;it++){
            *temp=f(*it);
            temp++;
        }

        return  MyQueriable<T>(ret,size);
    }

    T sum(){
        T s=0;
        for(T *it=data;it<data+size;it++)
            s+=*it;
        return s;
    }
    
};

// 这到底咋能想出来的，int的特性……
// niu...
// 太强了，为什么能这么写……
// 我将退学研究这份代码
template <typename S>
MyQueriable<typename S::value_type> from(S& thing) {
    using T = typename S::value_type;
    return MyQueriable<T>(thing.data(), thing.size());
}

template <typename T, int N>
MyQueriable<T> from(T (&arr)[N]) {
    return MyQueriable<T>(arr, N);
}
