#include<iostream>
#include "professor.h"


static const int MAX_COURSES = 50;

void Professor::addCourse(Course* course){
    if(courses.count(course->code)){cout << "Note: " << name << " already teaches " << course->code << endl;return;}
    if (cnt>= MAX_COURSES) { cout << "Error: Professor " << name << " cannot take more courses." << endl;return;}
    courses[course->code] = course;
    cnt++;
    return;
}

void Professor::removeCourse(std::string courseName){
    if(courses.count(courseName)) courses.erase(courseName);
    cnt--;
    return;
}

void Professor::print(){
    cout << "Professor: " << name << " " << "(ID: " << id << ")\n";
    cout << "Assigned courses: ";
    int i=1;
    if(cnt == 0){ cout << "(none)" << endl;return;}
    for(auto course:courses){
        cout << course.second->code;
        if(i!=cnt) cout << ", "; 
        i++;
    }
    cout << endl;
    return;
}

