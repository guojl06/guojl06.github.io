#pragma once
#include "smithing_stone.h"
#include <iostream>
using namespace std;

class NormalSmithingStone : public SmithingStone{
    int number=0;
    public:
        NormalSmithingStone(int _level) : SmithingStone(_level){
            cout << "Normal smithing stone " << _level << " was created." << endl;
        }
        ~NormalSmithingStone(){
            cout << "Normal smithing stone " << get_level() << " was destroyed." << endl;
        }

        void change_amount(int amount){
            number+=amount;
            add_amount(amount);
            if(amount>0)
                cout  << "Normal smithing stone "<< get_level() << " was added with " << amount << '.' << endl;
            else
                cout  << "Normal smithing stone "<< get_level() << " was subtracted with " << 0-amount << '.' << endl; 
        }
        int get_number(){
            return number;
        }

};