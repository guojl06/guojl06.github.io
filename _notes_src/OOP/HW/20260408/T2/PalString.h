#ifndef PAL_STRING
#define PAL_STRING

#include<iostream>
#include<cstring>
//坑死了！！！！
using namespace std;

class PalString{
    //const char* 不适合作为需要管理生命周期的成员变量!!!!!!!!
    char* text;
    // 几乎全部要写在public里面！！！
    public:
        PalString(const char* tmp){
            text=new char[strlen(tmp)*2];
            for(int i=0;i<strlen(tmp);i++){
                text[i]=tmp[i];
                text[strlen(tmp)*2-1-i]=tmp[i];
            }
        }
        PalString(const PalString& obj){
            text=new char[strlen(obj.text)];
            strcpy(text,obj.text);
        }
        ~PalString(){delete[] text;}

        const char* getString() const{
        // 特别注意！！！！需要添加 const 才能被const对象调用！
            return text;
        }
        void changeString(const char* newText){
            delete[] text;
            text=new char[strlen(newText)*2];
            for(int i=0;i<strlen(newText);i++){
                text[i]=newText[i];
                text[strlen(newText)*2-1-i]=newText[i];
            }
        }
};

ostream& operator<<(ostream &os,const PalString& obj){
    os << obj.getString();
    return os;
} 

#endif

// 注意关键点：
/*
1. char*的特殊性，本质指针，需要复制！
2. 内存的删除与再分配非常重要！！！！尤其对于这种指针
3.拷贝构造的时候也记得删除！！！
*/