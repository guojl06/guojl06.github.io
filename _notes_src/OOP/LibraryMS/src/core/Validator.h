#ifndef LIBRARYMS_VALIDATOR_H
#define LIBRARYMS_VALIDATOR_H

#include <string>

// 输入校验工具：全部为静态函数，集中处理"非法输入"。
// 调用方据此弹出友好的错误提示，而不是让程序崩溃或写入脏数据。
class Validator {
public:
    // 去除首尾空白
    static std::string trim(const std::string& s);
    // 是否全为数字（不含空串）
    static bool isAllDigits(const std::string& s);

    // 姓名等：非空且长度合理
    static bool isValidName(const std::string& s);
    // 性别：仅接受 男/女
    static bool isValidGender(const std::string& s);
    // 中国大陆手机号：11 位数字、以 1 开头
    static bool isValidPhone(const std::string& s);
    // ISBN：去除 - 与空格后，为 10 位或 13 位数字
    static bool isValidISBN(const std::string& s);
    // 正整数（如库存、年份范围内的整数）
    static bool isPositiveInt(const std::string& s);
    // 把字符串安全转成 int，失败返回 fallback
    static int toInt(const std::string& s, int fallback = 0);
    // 年份范围
    static bool isValidYear(int y);
};

#endif // LIBRARYMS_VALIDATOR_H
