#include "User.h"

User::User(const std::string& userId,
           const std::string& name,
           const std::string& gender,
           const std::string& phone)
    : userId_(userId), name_(name), gender_(gender), phone_(phone),
      registerDate_(Date::today()) {}

void User::setName(const std::string& v)   { name_ = v; }
void User::setGender(const std::string& v) { gender_ = v; }
void User::setPhone(const std::string& v)  { phone_ = v; }

// —— 学生 ——
int  Student::maxBorrowLimit() const { return 5; }
User::Type Student::userType() const { return Type::Student; }
std::string Student::typeName() const { return "学生"; }

// —— 教师 ——
int  Teacher::maxBorrowLimit() const { return 10; }
User::Type Teacher::userType() const { return Type::Teacher; }
std::string Teacher::typeName() const { return "教师"; }
