#include "Date.h"

#include <ctime>
#include <sstream>

// ---- 静态辅助：闰年与每月天数 ----
bool Date::isLeap(int y) {
    return (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
}

int Date::daysInMonth(int y, int m) {
    static const int dm[] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (m == 2 && isLeap(y)) return 29;
    return dm[m];
}

// ---- 构造 ----
Date::Date() : y_(1), m_(1), d_(1) {}

Date::Date(int y, int m, int d) : y_(y), m_(m), d_(d) {}

bool Date::isValid() const {
    if (y_ < 1) return false;
    if (m_ < 1 || m_ > 12) return false;
    if (d_ < 1 || d_ > daysInMonth(y_, m_)) return false;
    return true;
}

// ---- 绝对日序：从 1-1-1 累加 ----
long Date::toDays() const {
    long days = 0;
    for (int y = 1; y < y_; ++y) days += isLeap(y) ? 366 : 365;
    for (int m = 1; m < m_; ++m) days += daysInMonth(y_, m);
    days += d_;
    return days;
}

Date Date::addDays(int n) const {
    long total = toDays() + n;
    int y = 1;
    while (total > (isLeap(y) ? 366 : 365)) {
        total -= isLeap(y) ? 366 : 365;
        ++y;
    }
    int m = 1;
    while (total > daysInMonth(y, m)) {
        total -= daysInMonth(y, m);
        ++m;
    }
    return Date(y, m, static_cast<int>(total));
}

long Date::operator-(const Date& rhs) const {
    return this->toDays() - rhs.toDays();
}

bool Date::operator<(const Date& rhs) const { return toDays() < rhs.toDays(); }
bool Date::operator==(const Date& rhs) const {
    return y_ == rhs.y_ && m_ == rhs.m_ && d_ == rhs.d_;
}

// ---- 字符串互转 ----
std::string Date::toString() const {
    std::ostringstream os;
    os << y_ << '-';
    if (m_ < 10) os << '0';
    os << m_ << '-';
    if (d_ < 10) os << '0';
    os << d_;
    return os.str();
}

Date Date::fromString(const std::string& s) {
    // 接受 "2026-06-24" / "2026/6/24" 形式
    int y = 0, m = 0, d = 0;
    char sep1 = 0, sep2 = 0;
    std::istringstream is(s);
    is >> y >> sep1 >> m >> sep2 >> d;
    if (is.fail() || (sep1 != '-' && sep1 != '/') ||
        (sep2 != '-' && sep2 != '/')) {
        return Date();  // 解析失败 -> 无效日期
    }
    return Date(y, m, d);
}

Date Date::today() {
    std::time_t t = std::time(nullptr);
    std::tm* lt = std::localtime(&t);
    return Date(lt->tm_year + 1900, lt->tm_mon + 1, lt->tm_mday);
}
