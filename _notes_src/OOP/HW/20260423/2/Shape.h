#ifndef SHAPE
#define SHAPE
#define PI 3.14

#include<iostream>

class Shape {
public:
    virtual double getArea()=0;
    virtual ~Shape()=default;
};

class Rectangle :public Shape{
private:
    double width,height;
public:
    Rectangle(double w,double h) : width(w),height(h){}
    double getArea();
    ~Rectangle()=default;
};

class Circle: public Shape{
private:
    double radius;
public:
    Circle(double r) : radius(r){}
    double getArea();
    ~Circle()=default;
};

#endif