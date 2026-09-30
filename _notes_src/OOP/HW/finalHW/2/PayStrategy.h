#pragma once
#include <string>
#include<unordered_map>

class PayStrategy {			
	protected:
	std::unordered_map<std::string,double> moneyList;
	public:
	virtual ~PayStrategy() = default;
	virtual double pay(std::string name, double money)=0;
};


class NormalStrategy : public PayStrategy {	
	double pay(std::string name, double money){
		moneyList[name] += money;
		return moneyList[name];
	}	
};

class SwiftStrategy : public PayStrategy {	
	double pay(std::string name, double money){
		double realMoney=0;
		if(money<=10000) realMoney=money-10;
		else realMoney=money*0.001 < 20 ? money*0.999 : money - 20;
		moneyList[name] += realMoney;
		return moneyList[name];
	}	
};

class BitcoinStrategy : public PayStrategy {	
	double pay(std::string name, double money){
		double realMoney=0;
		realMoney = money-(name.size()+8) * 0.01;
		moneyList[name] += realMoney;
		return moneyList[name];
	}	
};
