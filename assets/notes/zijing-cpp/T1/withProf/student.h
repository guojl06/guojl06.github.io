// ============================================
// FILE: student.h
// PURPOSE: Declares the Student class interface
// ============================================

#ifndef STUDENT_H
#define STUDENT_H

#include <string>
using namespace std;

class Student {
 public:
  int id;
  string name;
  string major;
  double gpa;

  void print() const;
  bool isHonorStudent() const;
  string getStanding() const;
};

#endif  // STUDENT_H
