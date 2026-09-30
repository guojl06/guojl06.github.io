#pragma once
#include "weapon.h"
#include <iostream>
using namespace std;

class NormalWeapon : public Weapon{
    public:
        ~NormalWeapon(){
            if(get_level()!=0)
                cout << "Normal weapon "<<get_name()<<"+"<<get_level()<<" was destroyed.\n";
            else
                cout << "Normal weapon "<<get_name()<<" was destroyed.\n";
        }
        NormalWeapon(string _s) : Weapon(_s){
            cout << "Normal weapon "<<_s<<" was created.\n";
            return;
        }
        string gN(){
            return get_name();
        }
        int gL(){
            return get_level();
        }
        void upg(){
            upgrade();
            return;
        }

};