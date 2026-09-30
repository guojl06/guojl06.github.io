// ============================================
// FILE: main.cpp
// PURPOSE: University Course Management System Demo
// Demonstrates using Student and Course classes together
// ============================================

#include <iostream>
#include "student.h"
#include "course.h"
#include "professor.h"
using namespace std;

int main() {
    cout << "=== University Course Management System ===" << endl;
    
    // ----------------------------------------
    // Create students
    // ----------------------------------------
    Student alice, bob, carol;
    
    alice.id = 1001;
    alice.name = "Alice Chen";
    alice.major = "Computer Science";
    alice.gpa = 3.85;
    
    bob.id = 1002;
    bob.name = "Bob Smith";
    bob.major = "Computer Science";
    bob.gpa = 3.2;
    
    carol.id = 1003;
    carol.name = "Carol White";
    carol.major = "Mathematics";
    carol.gpa = 3.9;
    
    // ----------------------------------------
    // Create and set up courses
    // ----------------------------------------
    Course cs101, math201;
    
    cs101.initialize("CS101", "Intro to Programming", 3, 2);  // Capacity of 2
    math201.initialize("MATH201", "Calculus II", 4, 30);
    
    // ----------------------------------------
    // Enroll students in courses
    // ----------------------------------------
    cout << "\n--- Enrolling Students ---" << endl;
    
    cs101.enrollStudent(alice.id);   // Success
    cs101.enrollStudent(bob.id);     // Success
    cs101.enrollStudent(carol.id);   // Fail (course full)
    
    math201.enrollStudent(alice.id); // Success
    math201.enrollStudent(bob.id);   // Success

    cout << "\n--- Professor assignment ---" << endl;
    Professor prof;
    prof.id = 501;
    prof.name = "Dr. Morgan sLee";
    prof.addCourse(&cs101);
    prof.print();
    
    // ----------------------------------------
    // Print final status
    // ----------------------------------------
    cout << "\n--- Course Status ---" << endl;
    cs101.print();
    cout << endl;
    math201.print();
    
    cout << "\n--- Student Status ---" << endl;
    cout << alice.name << " - Standing: " << alice.getStanding() << endl;
    cout << bob.name << " - Standing: " << bob.getStanding() << endl;
    cout << carol.name << " - Standing: " << carol.getStanding() << endl;
    
    return 0;
}
