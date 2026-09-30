#ifndef PROFESSOR_H
#define PROFESSOR_H

#include <string>
using namespace std;

class Professor {
public:
    int id;
    string name;
    string courses[50];
    int courseCount;

    Professor();

    void print() const;
    void addCourse(const string& courseCode);
    void removeCourse(const string& courseCode);
};

#endif  // PROFESSOR_H
