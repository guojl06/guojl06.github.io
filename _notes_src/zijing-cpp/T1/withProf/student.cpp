// ============================================
// FILE: student.cpp
// ============================================

#include "student.h"
#include <iostream>
using namespace std;

void Student::print() const {
    cout << "ID: " << id << endl;
    cout << "Name: " << name << endl;
    cout << "Major: " << major << endl;
    cout << "GPA: " << gpa << endl;
}

bool Student::isHonorStudent() const {
    return gpa >= 3.5;
}

string Student::getStanding() const {
    if (gpa >= 3.5) {
        return "Excellent";
    } else if (gpa >= 3.0) {
        return "Good";
    } else if (gpa >= 2.0) {
        return "Satisfactory";
    } else {
        return "Warning";
    }
}
