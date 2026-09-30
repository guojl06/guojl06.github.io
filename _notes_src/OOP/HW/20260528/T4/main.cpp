#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <map>
#include <stdexcept>

#include "argparser.h"

class ArgParser;

int main(int argc, char* argv[]) {
    ArgParser parser("A simple program to demonstrate argument parsing.");

    // 定义参数
    parser.addFlag('v', "verbose", "Enable verbose output.");
    parser.addValue<std::string>('f', "file", "Path to the input file.", "default.txt");
    parser.addValue<int>('l', "level", "Set the logging level.", 5);

    // 解析命令行参数
    bool success = parser.parse(argc, argv);
    if (success) {
        // 打印帮助信息（如果提供了 --help 或 -h）
        if (parser.wantsHelp()) {
            parser.printHelp();
            return 0;
        }

        // 获取并使用参数
        bool verbose = parser.get<bool>("verbose").value_or(false);
        std::string filename = parser.get<std::string>("file").value();
        int level = parser.get<int>("level").value();

        std::cout << "--- Parsed Arguments ---" << std::endl;
        std::cout << "Verbose: " << (verbose ? "true" : "false") << std::endl;
        std::cout << "File: " << filename << std::endl;
        std::cout << "Level: " << level << std::endl;
        
        // 测试获取一个不存在的参数
        auto non_existent = parser.get<float>("speed");
        if (!non_existent) {
            std::cout << "\nSuccessfully handled request for non-existent argument 'speed'." << std::endl;
        }
    }
    else {
        parser.printHelp();
    }
    return 0;
}