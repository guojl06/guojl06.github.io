#pragma once

class OccupationStrategy {		
	public:
	virtual ~OccupationStrategy() = default;
	virtual double getSalary(double base, double bonus, double level)=0;
};

class SalesmanStrategy : public OccupationStrategy {
	double getSalary(double base, double bonus, double level){
		double realBonus=0;
		if(60 <= level && level < 70) realBonus = bonus * 0.6;
		else if(70 <= level && level < 80) realBonus = bonus * 0.7;
		else if(80 <= level && level <= 100) realBonus = bonus;
		return base+realBonus;
	}
	
};

class DeveloperStrategy : public OccupationStrategy {	
	double getSalary(double base, double bonus, double level){
		return base+bonus*level*0.01;
	}
};