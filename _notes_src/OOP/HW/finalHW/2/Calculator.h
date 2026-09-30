#pragma once
#include <string>
#include "OccupationStrategy.h"
#include "PayStrategy.h"

class Calculator {
    OccupationStrategy *OS;
    PayStrategy *PS;								
    public:
    Calculator(OccupationStrategy *O,PayStrategy *P) :  OS(O),PS(P){};
    
    double getSalary(double base, double bonus, double level){
        return OS->getSalary(base,bonus,level);
    }
    double pay(std::string name, double money){
        return PS->pay(name, money);
    }
};