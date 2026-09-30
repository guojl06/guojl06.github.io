#pragma once
#include "Operator.h"
#include "Constant.h"

class Sub : public Operator{
    public:
    Sub(Value *r1,Value *r2):Operator(r1,r2){}
    int calc(){return getV1()-getV2();}
};