#include "ComputerCollection.h"
#include <algorithm>

istream& operator>> (istream& in, ComputerCollection& cc)
{
	string temp;
	in >> temp;
	string name = "";
	
	int i = 0;
	int num = 0;
	for (; i < temp.length(); ++i) {
		if (temp[i] == '-') {
			++i;
			num = int(temp[i] - '0');
			++i;
			break;
		}
		name += temp[i];
	}
	for (; i < temp.length(); ++i) {
		if (temp[i] == '-') {
			++i;
			break;
		}
		num = num * 10 + int(temp[i] - '0');
	}
	
	int price = 0;
	for (; i < temp.length(); ++i) {
		price = price * 10 + int(temp[i] - '0');
	}

	Computer* p = cc.has_name(name);
	if (p == nullptr) {
		p = new Computer();
		cc.computers[cc.computerNum] = p;
		cc.computerNum++;
	}
	p->addInfo(name, num, price);
	
	return in;
}

ostream& operator<< (ostream& out, const ComputerCollection& cc)
{
	for (int i = 0; i < cc.computerNum; ++i) {
		out << *(cc.computers[i]) << endl;
	}
	return out;
}

Computer& ComputerCollection::operator[](const string& name)
{
	return *(this->has_name(name));
}

Computer* ComputerCollection::has_name(const string& name)
{
	for (int i = 0; i < computerNum; ++i) {
		if (computers[i]->getName() == name) {
			return computers[i];
		}
	}
	return nullptr;
}

void ComputerCollection::sortByScore()
{
	// 按库存从大到小排序，库存相同则按价格从高到低排序
	for (int i = 0; i < computerNum - 1; ++i) {
		for (int j = 0; j < computerNum - 1 - i; ++j) {
			// 使用<运算符比较：如果computers[j] < computers[j+1]，则需要交换
			// < 定义为：num小或(num相同且price小)时返回true
			if (*computers[j] < *computers[j + 1]) {
				Computer* temp = computers[j];
				computers[j] = computers[j + 1];
				computers[j + 1] = temp;
			}
		}
	}
}
