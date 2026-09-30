#ifndef LIBRARYMS_DATE_H
#define LIBRARYMS_DATE_H

#include <string>

// 简单日期类：封装年/月/日，提供比较、加减天数、与字符串互转。
// 体现「封装」：内部字段私有，仅通过公有接口访问。
class Date {
public:
    Date();                       // 默认构造：1-1-1（视为无效）
    Date(int y, int m, int d);    // 构造指定日期

    int year() const  { return y_; }
    int month() const { return m_; }
    int day() const   { return d_; }

    bool isValid() const;                              // 是否为合法日期
    std::string toString() const;                      // "2026-06-24"
    static Date fromString(const std::string& s);      // 解析 "2026-06-24"，失败返回无效日期
    static Date today();                               // 系统当前日期

    // 以绝对日序参与运算（公元 1-1-1 为第 1 天），便于做差与加减。
    long toDays() const;
    Date addDays(int n) const;                         // 当前日期 + n 天
    long operator-(const Date& rhs) const;             // 两个日期相差天数
    bool operator<(const Date& rhs) const;
    bool operator==(const Date& rhs) const;

private:
    int y_, m_, d_;

    static bool isLeap(int y);
    static int  daysInMonth(int y, int m);
};

#endif // LIBRARYMS_DATE_H
