#pragma once
#include "LegacySkill.h"

class ISkill{

    public:
    virtual int cast() = 0;
    virtual ~ISkill()=default;

};

class LegacySkillAdapter : public ISkill{
    LegacySkill *LS;
    public:
    LegacySkillAdapter(LegacySkill *mLS):LS(mLS){};
    virtual ~LegacySkillAdapter(); 
    int cast();
};

class MpChecker : public ISkill{
    ISkill *IS;
    int mpInit;
    int mpCost;
    int currentMp;
    public:
    MpChecker(ISkill *_IS,int _mpInit,int _mpCost): 
        IS(_IS),mpInit(_mpInit),mpCost(_mpCost){currentMp=mpInit;};
    virtual ~MpChecker(); 
    int cast();
};

class Buff : public ISkill{
    protected:
    ISkill *_buff;

    public:
    Buff(ISkill *_b):_buff(_b){};
    virtual ~Buff();
    int cast();
};

class CritBuff : public Buff{
    public:
    CritBuff(ISkill *_b):Buff(_b){};
    virtual ~CritBuff();
    int cast();
};

class PoisonBuff : public Buff{
    public:
    PoisonBuff(ISkill *_b):Buff(_b){};
    virtual ~PoisonBuff();
    int cast();
};