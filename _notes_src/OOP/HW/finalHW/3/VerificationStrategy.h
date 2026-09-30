#pragma once
# include <string>

class VerificationStrategy{
public:
	virtual ~VerificationStrategy() = default;
	virtual std::string verify(std::string mes) = 0;
};

class PrefixStrategy:public VerificationStrategy{
public:
	std::string verify(std::string mes){
		return std::string("")+mes[0]+mes[1]+mes[2];
	}
};

class IntervalStrategy:public VerificationStrategy{
public:
	std::string verify(std::string mes){
		std::string ans="";
		int cnt=0;
		for(auto c:mes){
			if((++cnt)%2==1) ans+=c;
		}
		return ans;
	}
};