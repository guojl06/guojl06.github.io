#pragma once
#include "Operator.h"
#include "Constant.h"

class Plus : public Operator{
    public:
        Plus(Value *r1,Value *r2):Operator(r1,r2){}
        int calc(){return getV1()+getV2();}
};