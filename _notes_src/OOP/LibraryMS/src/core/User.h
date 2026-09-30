#ifndef LIBRARYMS_USER_H
#define LIBRARYMS_USER_H

#include <string>
#include "Date.h"

// 用户抽象基类：体现「继承 + 多态」。
// 不同用户类型的可借数量不同，由派生类通过纯虚函数决定。
class User {
public:
    enum class Type { Student, Teacher };

    User(const std::string& userId,
         const std::string& name,
         const std::string& gender,
         const std::string& phone);
    virtual ~User() = default;

    // —— 多态接口 ——
    virtual int  maxBorrowLimit() const = 0;   // 该类用户的最大借阅数
    virtual Type userType() const = 0;
    virtual std::string typeName() const = 0;  // "学生" / "教师"

    const std::string& userId() const   { return userId_; }
    const std::string& name() const     { return name_; }
    const std::string& gender() const   { return gender_; }
    const std::string& phone() const    { return phone_; }
    const Date& registerDate() const    { return registerDate_; }

    void setName(const std::string&);
    void setGender(const std::string&);
    void setPhone(const std::string&);

    friend class DataManager;   // 持久化时直接恢复注册日期

protected:
    std::string userId_, name_, gender_, phone_;
    Date registerDate_;   // 注册日期 = 创建当天
};

// 学生用户：最多借 5 本
class Student : public User {
public:
    using User::User;
    int  maxBorrowLimit() const override;
    Type userType() const override;
    std::string typeName() const override;
};

// 教师用户：最多借 10 本
class Teacher : public User {
public:
    using User::User;
    int  maxBorrowLimit() const override;
    Type userType() const override;
    std::string typeName() const override;
};

#endif // LIBRARYMS_USER_H
