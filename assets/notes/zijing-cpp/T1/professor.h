#ifndef PROFESSOR_H  // Header guard: prevents double inclusion
#define PROFESSOR_H

#include<string>
#include<map>
#include "course.h"

class Professor{
    public:
        int id;
        int cnt=0;
        std::string name;
    std::map<std::string,Course*> courses;
    void print();
    void addCourse(Course* course);
    void removeCourse(std::string courseName);
};

#endif