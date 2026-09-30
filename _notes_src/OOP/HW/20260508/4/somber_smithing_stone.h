#pragma once
#include "smithing_stone.h"
#include <iostream>
using namespace std;

class SomberSmithingStone : public SmithingStone{

    int number=0;
    public:
        SomberSmithingStone(int _level) : SmithingStone(_level){
            cout << "Somber smithing stone " << _level << " was created." << endl;
        }
        ~SomberSmithingStone(){
            cout << "Somber smithing stone " << get_level() << " was destroyed." << endl;
        }
        void change_amount(int amount)
        {
            add_amount(amount);
            number += amount;
            if(amount>0)
                cout  << "Somber smithing stone "<< get_level() << " was added with " << amount << '.' << endl;
            else
                cout  << "Somber smithing stone "<< get_level() << " was subtracted with " << 0-amount << '.' << endl;    
        }
        int get_number(){
            return number;
        }

};