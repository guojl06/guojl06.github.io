#include "CHugeInt.h"
#include<iostream>

CHugeInt::CHugeInt(const char * s){
    sz=strlen(s);
    for(int i=0;i<sz;i++){
        digit[i]=s[sz-1-i]-'0';
    }
}
CHugeInt::CHugeInt(int n){
    if(n==0) sz=1;
    else{
        for(int i=0;i<220 && n>0;i++){
            digit[i]=(n%10);
            n/=10;
            sz++;
        }
    }  
}
const int CHugeInt::size() const{
    return sz;
}

// const int CHugeInt::getDigit(int index){return digit[index];}

ostream& operator<<(ostream &os,const CHugeInt &num){
    // 调试行：看看 sz 是不是正常的数字（比如 1, 2, 10 等）
    // cout << "[Debug: sz=" << num.size() << "]" << endl;
    int sz=num.size();
    for(int i=0;i<sz;i++){
        os << num.digit[sz-1-i];
    }
    return os;
}


// 最恐怖的运算来了
CHugeInt CHugeInt::operator+(CHugeInt& b){
    CHugeInt res(0);
    // int minsz=(size()>b.size() ? b.size() : size());
    int maxsz=(size()<b.size() ? b.size() : size());
    
    for(int i=0;i<=maxsz;i++){
        res.digit[i]+=(digit[i]+b.digit[i]);
        res.digit[i+1]+=(res.digit[i])/10;
        res.digit[i]%=10;
    }
    // cout << res.digit[maxsz] << endl;
    if(res.digit[maxsz]!=0) res.sz=maxsz+1;
    else res.sz=maxsz;
    return res;
}
CHugeInt CHugeInt::operator+(int &tmp){
    CHugeInt b(tmp);
    // CHugeInt res(0);
    
    return *this+b;
}
CHugeInt operator+(int &tmp,CHugeInt &a){
    CHugeInt b(tmp);
    return a+b;
}


CHugeInt& CHugeInt::operator+=(CHugeInt& b){
    // cout << b << "test" << endl;
    // int minsz=(size()>b.size() ? b.size() : size());
    int maxsz=(size()<b.size() ? b.size() : size());
    
    for(int i=0;i<maxsz;i++){
        digit[i]+=(b.digit[i]);
        digit[i+1]+=(digit[i])/10;
        digit[i]%=10;
    }
    if(digit[maxsz]!=0) sz=maxsz+1;
    else sz=maxsz;
    return *this;
}
CHugeInt& CHugeInt::operator+=(int& tmp){
    
    CHugeInt b(tmp);
    // cout << b << "test" << endl;
    // int minsz=(size()>b.size() ? b.size() : size());
    int maxsz=(size()<b.size() ? b.size() : size());
    
    for(int i=0;i<maxsz;i++){
        digit[i]+=(b.digit[i]);
        digit[i+1]+=(digit[i])/10;
        digit[i]%=10;
        // cout << digit[i] << "this is " << i << endl;
    }
    if(digit[maxsz]!=0) sz=maxsz+1;
    else sz=maxsz;
    // cout << *this << "f"<< endl;
    return *this;
}

CHugeInt& CHugeInt::operator++(){
    CHugeInt b(1);
    // cout << b << "test" << endl;
    // int minsz=(size()>b.size() ? b.size() : size());
    int maxsz=(size()<b.size() ? b.size() : size());
    
    for(int i=0;i<maxsz;i++){
        digit[i]+=(b.digit[i]);
        digit[i+1]+=(digit[i])/10;
        digit[i]%=10;
    }
    if(digit[maxsz]!=0) sz=maxsz+1;
    else sz=maxsz;
    return *this;
}
CHugeInt& CHugeInt::operator++(int){
    CHugeInt *tmp=new CHugeInt(0);
    *tmp = *this;
    CHugeInt b(1);
    // cout << b << "test" << endl;
    int minsz=(size()>b.size() ? b.size() : size());
    int maxsz=(size()<b.size() ? b.size() : size());
    
    for(int i=0;i<minsz;i++){
        digit[i]+=(b.digit[i]);
        digit[i+1]+=(digit[i])/10;
        digit[i]%=10;
    }
    if(digit[maxsz]!=0) sz=maxsz+1;
    else sz=maxsz;
    return *tmp;
}

