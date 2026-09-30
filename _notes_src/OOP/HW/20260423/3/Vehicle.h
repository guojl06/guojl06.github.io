#ifndef VEC
#define VEC
#include<iostream>

class Vehicle{
    private:
        int wheelNum,wingNum;
        int whN=0,wiN=0;
    public:
        ~Vehicle()=default;
        void set_max_wheel_num(int whn){
            wheelNum = whn;return;
        }
        void set_max_wing_num(int win){
            wingNum = win;return;
        }
        bool finished(){return (whN==wheelNum)&&(wiN==wingNum);}
        void add_wheel(){
            if(wheelNum<= whN) return;
            whN++;
            return;
        }
        void add_wing(){
            if(wingNum<= wiN) return;
            wiN++;
            return;
        }
        virtual void run(){std::cout << "I am running\n";}
};

#endif