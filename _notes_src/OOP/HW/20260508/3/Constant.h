#pragma once
#include "Value.h"

class Constant : public Value{
    int val;
    public:
        Constant(int v):val(v){}
        virtual ~Constant() override{}
        int calc(){return val;}

};