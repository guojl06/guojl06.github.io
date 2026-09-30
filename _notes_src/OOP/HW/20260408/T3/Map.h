#pragma once
#include "Pair.h"

class Map{
    Pair * data;
    int sz;
public:
    Map(int n);
    // TODO
    ~Map();
    int size() const;
    int & operator [](const string & k);
    int operator [](const string & k) const;
    // 这么安全？！？！？！
};