#pragma once
#include "iargument.h"
#include <optional>
#include <sstream>
#include <iostream>

template<typename T>
class ValueArgument : public IArgument {
public:
    std::optional<T> value;
    T default_value;
    ValueArgument(char s, const std::string& l, const std::string& d, T def_val)
        : IArgument(s, l, d), value(def_val), default_value(def_val) {}
    bool parse(const std::vector<std::string>& args, size_t& index) override {
        if (index + 1 >= args.size()) {
            std::cout << "Error: Argument " << long_name_ << " requires a value." << std::endl;
            return false;
        }
        index++;
        std::istringstream iss(args[index]);
        T val;
        iss >> val;
        value = val;
        return true;
    }
    std::string get_info() const override {
        std::ostringstream oss;
        oss << "  -" << short_name_ << ", --" << long_name_ << "=<value>\t" << description_ << " (default: " << default_value << ")";
        return oss.str();
    }
};
