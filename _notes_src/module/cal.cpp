#include <iostream>
#include <string>
#include <regex>

using namespace std;

// 自动复制到剪贴板
void copyToClipboard(const string& text) {
#ifdef _WIN32
    string cmd = "echo " + text + " | clip";
    system(cmd.c_str());
#elif __APPLE__
    FILE* pipe = popen("pbcopy", "w");
    if (pipe) {
        fputs(text.c_str(), pipe);
        pclose(pipe);
    }
#else
    string cmd = "echo -n \"" + text + "\" | xclip -selection clipboard";
    system(cmd.c_str());
#endif
}

int main() {
    string input;
    // 匹配变量，排除数学函数
    regex var_regex("\\b(?!sqrt|sin|cos|tan|log|ln|exp|abs|pow|pi|calc|round)[a-zA-Z_][a-zA-Z0-9_]*\\b");

    while (true) {
        cout << "请输入：";
        if (!getline(cin, input) || input == "exit") break;
        if (input.empty()) continue;

        // 核心转换逻辑
        string fmt = regex_replace(input, var_regex, "\"+str($&)+\"");
        string final_str = "\"" + fmt + "\"";
        
        // 清理冗余引号拼接
        final_str = regex_replace(final_str, regex("\"\"\\+"), "");
        final_str = regex_replace(final_str, regex("\\+\"\""), "");
        
        // 组装最终字符串
        string result = "cal(" + final_str + ", result: 1)";
        
        copyToClipboard(result);

        cout << "typst：" << result << " (已存入剪贴板)" << endl;
        cout << "下一个：" << endl;
    }
    return 0;
}