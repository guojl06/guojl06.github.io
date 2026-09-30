#ifndef __ComputerCOLLECTION_H__
#define __ComputerCOLLECTION_H__

#include "Computer.h"
#include <iostream>
#include <string>
using namespace std;

class ComputerCollection
{
private:
	int computerNum = 0;
	Computer* computers[201];

public:
	friend istream& operator>> (istream& in, ComputerCollection& sc);
	friend ostream& operator<< (ostream& out, const ComputerCollection& sc);

	Computer& operator[] (const string& name);
	Computer* has_name(const string& name);
	void sortByScore();
};

#endif
