#pragma once
#include <string>
#include <vector>

class IArgument {
public:
    char short_name_;
    std::string long_name_;
    std::string description_;

    IArgument(char short_name, const std::string& long_name, const std::string& description)
        : short_name_(short_name), long_name_(long_name), description_(description) {}
    
    virtual ~IArgument() = default;

    virtual bool parse(const std::vector<std::string>& args, size_t& index) = 0;
    virtual std::string get_info() const = 0;
    virtual bool is_flag() const { return false; }
};