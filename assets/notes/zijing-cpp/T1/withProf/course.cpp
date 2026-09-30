#include "course.h"
#include <iostream>
using namespace std;

void Course::initialize(string c, string t, int cred, int cap) {
    code = c;
    title = t;
    credits = cred;
    capacity = cap;
    enrollmentCount = 0;

    for (int i = 0; i < 50; i++) {
        enrolledStudents[i] = 0;
    }
}

bool Course::enrollStudent(int studentID) {
    if (enrollmentCount >= capacity) {
        cout << "Error: Course " << code << " is full!" << endl;
        return false;
    }

    for (int i = 0; i < enrollmentCount; i++) {
        if (enrolledStudents[i] == studentID) {
            cout << "Error: Student " << studentID
                 << " is already enrolled in " << code << endl;
            return false;
        }
    }

    enrolledStudents[enrollmentCount] = studentID;
    enrollmentCount++;

    cout << "Success: Student " << studentID
         << " enrolled in " << code << endl;
    return true;
}

void Course::print() const {
    cout << code << ": " << title << endl;
    cout << "Credits: " << credits << endl;
    cout << "Enrollment: " << enrollmentCount << "/" << capacity << endl;

    if (enrollmentCount > 0) {
        cout << "Enrolled Students: ";
        for (int i = 0; i < enrollmentCount; i++) {
            cout << enrolledStudents[i];
            if (i < enrollmentCount - 1) {
                cout << ", ";
            }
        }
        cout << endl;
    }
}

bool Course::isFull() const {
    return enrollmentCount >= capacity;
}

int Course::getAvailableSeats() const {
    return capacity - enrollmentCount;
}
