#include "course.h"
#include <iostream>
using namespace std;

// Initialize all course data
void Course::initialize(string c, string t, int cred, int cap) {
    code = c;
    title = t;
    credits = cred;
    capacity = cap;
    enrollmentCount = 0;    // Start with no students enrolled
    
    // Initialize all array elements to 0 (good practice)
    for (int i = 0; i < 50; i++) {
        enrolledStudents[i] = 0;
    }
}

// Try to enroll a student
bool Course::enrollStudent(int studentID) {
    // Check if course is full
    if (enrollmentCount >= capacity) {
        cout << "Error: Course " << code << " is full!" << endl;
        return false;
    }
    
    // Check if student already enrolled
    for (int i = 0; i < enrollmentCount; i++) {
        if (enrolledStudents[i] == studentID) {
            cout << "Error: Student " << studentID 
                 << " is already enrolled in " << code << endl;
            return false;
        }
    }
    
    // Add student to array
    enrolledStudents[enrollmentCount] = studentID;
    enrollmentCount++;
    
    cout << "Success: Student " << studentID 
         << " enrolled in " << code << endl;
    return true;
}

// Print course information
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

// Check if course is full
bool Course::isFull() const {
    return enrollmentCount >= capacity;
}

// Get available seats
int Course::getAvailableSeats() const {
    return capacity - enrollmentCount;
}
