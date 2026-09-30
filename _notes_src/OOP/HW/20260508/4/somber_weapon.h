#pragma once
#include "weapon.h"
#include <iostream>
using namespace std;

class SomberWeapon : public Weapon{
    public:
    SomberWeapon(string _s) : Weapon(_s){
        cout << "Somber weapon " << _s << " was created.\n";
        return;
    }
    ~SomberWeapon(){
        if(get_level()!=0)
            cout << "Somber weapon "<<get_name()<<"+"<<get_level()<<" was destroyed.\n";
        else
            cout << "Somber weapon "<<get_name()<<" was destroyed.\n";
    }
    int gL(){return get_level();}
    string gN(){return get_name();}
    void upg(){
        upgrade();
        return;
    }

};