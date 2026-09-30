#include "Validator.h"

#include <cctype>
#include <algorithm>

std::string Validator::trim(const std::string& s) {
    size_t b = 0, e = s.size();
    while (b < e && std::isspace(static_cast<unsigned char>(s[b]))) ++b;
    while (e > b && std::isspace(static_cast<unsigned char>(s[e - 1]))) --e;
    return s.substr(b, e - b);
}

bool Validator::isAllDigits(const std::string& s) {
    if (s.empty()) return false;
    for (char c : s) if (!std::isdigit(static_cast<unsigned char>(c))) return false;
    return true;
}

bool Validator::isValidName(const std::string& s) {
    std::string t = trim(s);
    return !t.empty() && t.size() <= 30;
}

bool Validator::isValidGender(const std::string& s) {
    std::string t = trim(s);
    return t == "男" || t == "女";
}

bool Validator::isValidPhone(const std::string& s) {
    std::string t = trim(s);
    return t.size() == 11 && t[0] == '1' && isAllDigits(t);
}

bool Validator::isValidISBN(const std::string& s) {
    std::string t;
    for (char c : s) {
        if (c == '-' || c == ' ') continue;
        t.push_back(c);
    }
    return (t.size() == 10 || t.size() == 13) && isAllDigits(t);
}

bool Validator::isPositiveInt(const std::string& s) {
    std::string t = trim(s);
    if (t.empty()) return false;
    // 允许一个前导符号
    size_t i = 0;
    if (t[0] == '+' || t[0] == '-') {
        if (t.size() == 1) return false;
        i = 1;
    }
    for (; i < t.size(); ++i)
        if (!std::isdigit(static_cast<unsigned char>(t[i]))) return false;
    return toInt(t, -1) > 0;
}

int Validator::toInt(const std::string& s, int fallback) {
    try {
        size_t idx = 0;
        int v = std::stoi(s, &idx);
        return v;
    } catch (...) {
        return fallback;
    }
}

bool Validator::isValidYear(int y) {
    return y >= 1000 && y <= 9999;
}
