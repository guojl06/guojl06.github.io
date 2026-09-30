#pragma once
# include <string>

class EncryptStrategy{
public:
	virtual ~EncryptStrategy() = default;
	virtual std::string encode(std::string mes) = 0;
};

class InsertStrategy : public EncryptStrategy{
public:
	std::string encode(std::string mes){
		std::string ans="";
		for(auto c:mes) ans+=c,ans+='#';
		return ans;
	}
};

class InvertStrategy : public EncryptStrategy{
public:
	std::string encode(std::string mes){
		std::string ans="";
		for(int i=0;i<mes.size();i++) ans+=mes[mes.size()-i-1];
		return ans;
	}
};