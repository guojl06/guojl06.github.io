#include "professor.h"
#include <iostream>
using namespace std;

static const int MAX_COURSES = 50;

Professor::Professor() : id(0), courseCount(0) {
    for (int i = 0; i < MAX_COURSES; i++) {
        courses[i] = "";
    }
}

void Professor::addCourse(const string& courseCode) {
    if (courseCode.empty()) {
        return;
    }
    if (courseCount >= MAX_COURSES) {
        cout << "Error: Professor " << name << " cannot take more courses." << endl;
        return;
    }
    for (int i = 0; i < courseCount; i++) {
        if (courses[i] == courseCode) {
            cout << "Note: " << name << " already teaches " << courseCode << endl;
            return;
        }
    }
    courses[courseCount] = courseCode;
    courseCount++;
}

void Professor::removeCourse(const string& courseCode) {
    for (int i = 0; i < courseCount; i++) {
        if (courses[i] == courseCode) {
            for (int j = i; j < courseCount - 1; j++) {
                courses[j] = courses[j + 1];
            }
            courses[courseCount - 1] = "";
            courseCount--;
            return;
        }
    }
}

void Professor::print() const {
    cout << "Professor: " << name << " (ID: " << id << ")" << endl;
    if (courseCount == 0) {
        cout << "Assigned courses: (none)" << endl;
        return;
    }
    cout << "Assigned courses: ";
    for (int i = 0; i < courseCount; i++) {
        cout << courses[i];
        if (i < courseCount - 1) {
            cout << ", ";
        }
    }
    cout << endl;
}
