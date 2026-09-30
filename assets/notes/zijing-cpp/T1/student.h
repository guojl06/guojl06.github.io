// ============================================
// FILE: student.h
// PURPOSE: Declares the Student class interface
// This is like a contract ¡ª it tells other files what Student can do
// ============================================

#ifndef STUDENT_H  // Header guard: prevents double inclusion
#define STUDENT_H

#include <string>
using namespace std;

// ============================================
// STUDENT CLASS DECLARATION
// ============================================
class Student {
 public:
  // ----------------------------------------
  // MEMBER VARIABLES (Data)
  // Each Student object gets its own copy of these
  // ----------------------------------------
  int id;        // Student ID number
  string name;   // Full name
  string major;  // Field of study
  double gpa;    // Grade point average

  // ----------------------------------------
  // MEMBER FUNCTIONS (Behavior)
  // These operate on a specific Student object's data
  // ----------------------------------------

  // Print all student information
  // 'const' means this function promises NOT to modify the object
  void print() const;

  // Check if student is on honor roll (GPA >= 3.5)
  bool isHonorStudent() const;

  // Get academic standing: "Excellent", "Good", "Warning"
  string getStanding() const;
};

#endif  // STUDENT_H#pragma once
