#pragma once

#include <iostream>
#include <string>

class Animal{
    public:
        std::string name;
        virtual ~Animal(){};
        Animal(std::string N) : name(N){}
        virtual void speak(){};
        virtual void swim(){};
        void action(){
            speak();
            swim();
            return;
        }
};