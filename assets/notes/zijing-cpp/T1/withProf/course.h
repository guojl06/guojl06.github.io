#ifndef COURSE_H
#define COURSE_H

#include <string>
#include "student.h"
using namespace std;

class Course {
public:
    string code;
    string title;
    int credits;
    int capacity;

    int enrolledStudents[50];
    int enrollmentCount;

    void initialize(string c, string t, int cred, int cap);
    bool enrollStudent(int studentID);
    void print() const;
    bool isFull() const;
    int getAvailableSeats() const;
};

#endif  // COURSE_H
