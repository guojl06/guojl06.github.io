#ifndef CONTAINER_H
#define CONTAINER_H
#include "BasicContainer.h"
#include <vector>
#include <iostream>
#include <algorithm>
#include <map>

using std::vector;
using std::map;

template<class A>
struct Point {
    Pos pos;
    A value;
    Point (Pos p, A v): pos(p), value(v) {}
};

template<class A, class C>
class Container : public BasicContainer<A> {
public:
    void insert(const Pos &p, const A &v) {};
    A* find(Pos p) { return NULL; };
};




template <class A>
class Compare{
    public:
    bool operator()(const Point<A>& a,const Point<A>& b) const{
        if(a.pos.first < b.pos.first) return 1;
        if(a.pos.first > b.pos.first) return 0;
        if(a.pos.second < b.pos.second) return 1;
        return 0;
    }
};

// template <class A>
// class Container<A, vector<A> > : public BasicContainer<A> {
//     vector< Point<A> > base;
//     Compare<A> comp=Compare<A>();
    
// public:

//     void insert(const Pos &p, const A &v) {
//         base.push_back(Point<A>(p, v));
//         sort(base.begin(),base.end(),comp);
//     }

//     A* find(Pos p) {
        
        


//         //  二分？！
//         auto it = std::lower_bound(base.begin(), base.end(),p,[](const Point<A>& element, const Pos& target_pos) {
//             return element.pos < target_pos; 
//         });
//         if (it != base.end() && it->pos == p) {
//             return &(it->value); // 找到了，返回棋子名字
//         }

//         // for(auto t = base.begin(); t != base.end(); ++t) {
//         //     if(p == t->pos) return &(t->value);
//         // }
//         return NULL;
//     }
// };

template <class A>
class Container<A, vector<A> > : public BasicContainer<A> {
    vector< Point<A> > base;
    Compare<A> comp = Compare<A>();
    bool is_sorted = true; // 缓存标记
    
public:
    void insert(const Pos &p, const A &v) {
        base.push_back(Point<A>(p, v)); 
        is_sorted = false;              // 标记数据现在变脏了
    }

    A* find(Pos p) {
        // 只有在数据无序时才排序
        if (!is_sorted) {
            std::sort(base.begin(), base.end(), comp);
            is_sorted = true;
        }

        auto it = std::lower_bound(base.begin(), base.end(), p, [](const Point<A>& element, const Pos& target_pos) {
            if (element.pos.first != target_pos.first) return element.pos.first < target_pos.first;
            return element.pos.second < target_pos.second;
        });

        if (it != base.end() && it->pos == p) {
            return &(it->value);
        }
        return NULL;
    }
};

template <class A>
class Container<A, map<Pos,A> > : public BasicContainer<A> {
    map<Pos,A> base;
    
public:
    void insert(const Pos &p, const A &v) {
        base[p]=v;
    }

    A* find(Pos p) {
        auto it = base.find(p);
        if (it != base.end()) {
            // map 里面存的是 pair，it->second 才是我们要的那个 value
            return &(it->second); 
        }
        return nullptr;
    }
};

#endif
