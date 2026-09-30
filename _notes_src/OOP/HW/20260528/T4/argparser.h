#pragma once
#include "flagargument.h"
#include "valueargument.h"
#include <memory>
#include <map>
#include <iostream>
#include <optional>
#include <type_traits>

class ArgParser {
private:
    std::string program_description_;
    std::vector<std::unique_ptr<IArgument>> arguments_;
    std::map<std::string, IArgument*> long_name_map_;
    std::map<char, IArgument*> short_name_map_;
    bool help_wanted_ = false;

public:
    ArgParser(const std::string& description) : program_description_(description) {
        addFlag('h', "help", "Show this help message.");
    }

    void addFlag(char s, const std::string& l, const std::string& d) {
        auto flag = std::make_unique<FlagArgument>(s, l, d);
        short_name_map_[s] = flag.get();
        long_name_map_[l] = flag.get();
        arguments_.push_back(std::move(flag));
    }
    template<typename T>
    void addValue(char s, const std::string& l, const std::string& d, T def_val) {
        auto val = std::make_unique<ValueArgument<T>>(s, l, d, def_val);
        short_name_map_[s] = val.get();
        long_name_map_[l] = val.get();
        arguments_.push_back(std::move(val));
    }
    bool parse(int argc, char* argv[]) {
        std::vector<std::string> args;
        for (int i = 1; i < argc; i++) {
            std::string a = argv[i];
            if (a.size() > 2 && a.substr(0, 2) == "--") {
                auto eq = a.find('=');
                if (eq != std::string::npos) {
                    args.push_back(a.substr(0, eq));
                    args.push_back(a.substr(eq + 1));
                    continue;
                }
            }
            args.push_back(a);
        }
        for (size_t i = 0; i < args.size(); i++) {
            const std::string& arg = args[i];
            if (arg == "-h" || arg == "--help") {
                help_wanted_ = true;
                continue;
            }
            IArgument* target = nullptr;
            if (arg.size() > 2 && arg.substr(0, 2) == "--") {
                auto it = long_name_map_.find(arg.substr(2));
                if (it != long_name_map_.end()) target = it->second;
            } else if (arg.size() == 2 && arg[0] == '-') {
                auto it = short_name_map_.find(arg[1]);
                if (it != short_name_map_.end()) target = it->second;
            }
            if (!target) {
                std::cout << "Error: Unknown argument: " << arg << std::endl;
                return false;
            }
            if (!target->parse(args, i)) {
                return false;
            }
        }
        return true;
    }
    template<typename T>
    std::optional<T> get(const std::string& name) const {
        auto it = long_name_map_.find(name);
        if (it == long_name_map_.end()) return std::nullopt;
        if constexpr (std::is_same_v<T, bool>) {
            auto* flag = dynamic_cast<FlagArgument*>(it->second);
            if (flag) return flag->value;
        }
        auto* val = dynamic_cast<ValueArgument<T>*>(it->second);
        if (val) return val->value;
        return std::nullopt;
    }

    bool wantsHelp() const { return help_wanted_; }
    void printHelp() const {
        std::cout << program_description_ << "\n\nUsage:\n";
        for (const auto& arg : arguments_) {
            std::cout << arg->get_info() << std::endl;
        }
    }
};
