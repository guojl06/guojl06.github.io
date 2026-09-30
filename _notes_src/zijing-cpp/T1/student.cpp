// ============================================
// FILE: student.cpp
// PURPOSE: Implements the Student class functions
// Defines HOW each function works
// ============================================

#include "student.h"      // Include the declaration (must match exactly!)
#include <iostream>
using namespace std;

// ============================================
// MEMBER FUNCTION IMPLEMENTATIONS
// Syntax: ReturnType ClassName::FunctionName(parameters) { body }
// The :: is the "scope resolution operator" - it says "this belongs to Student"
// ============================================

// Print all student information
void Student::print() const {
    cout << "ID: " << id << endl;
    cout << "Name: " << name << endl;
    cout << "Major: " << major << endl;
    cout << "GPA: " << gpa << endl;
}

// Check if honor student (GPA >= 3.5)
bool Student::isHonorStudent() const {
    return gpa >= 3.5;    // Simple comparison, returns true or false
}

// Get academic standing based on GPA
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
