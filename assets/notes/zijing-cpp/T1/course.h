#ifndef COURSE_H
#define COURSE_H

#include <string>
#include "student.h"      // Need to know about Student class
using namespace std;

// ============================================
// COURSE CLASS DECLARATION
// ============================================
class Course {
public:
    // ----------------------------------------
    // MEMBER VARIABLES
    // ----------------------------------------
    string code;            // Course code (e.g., "CS101")
    string title;           // Course title (e.g., "Introduction to Programming")
    int credits;            // Credit hours
    int capacity;           // Maximum enrollment
    
    // Array of enrolled students (store student IDs)
    int enrolledStudents[50];  // Fixed-size array
    int enrollmentCount;       // Current number of enrolled students
    
    // ----------------------------------------
    // MEMBER FUNCTIONS
    // ----------------------------------------
    
    // Initialize course (like a setup function)
    void initialize(string c, string t, int cred, int cap);
    
    // Try to enroll a student (by ID)
    // Returns true if successful, false if course is full
    bool enrollStudent(int studentID);
    
    // Print course information
    void print() const;
    
    // Check if course is full
    bool isFull() const;
    
    // Get number of available seats
    int getAvailableSeats() const;
};

#endif // COURSE_H
