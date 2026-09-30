#pragma once
#include "iargument.h"

class FlagArgument : public IArgument {
public:
    bool value = false;
    FlagArgument(char s, const std::string& l, const std::string& d)
        : IArgument(s, l, d) {}
    bool parse(const std::vector<std::string>&, size_t&) override {
        value = true;
        return true;
    }
    std::string get_info() const override {
        return "  -" + std::string(1, short_name_) + ", --" + long_name_ + "\t\t" + description_;
    }
    bool is_flag() const override {
        return true;
    }
};
