#pragma once
#include <string>
#include <vector>
#include <utility>
#include <cstdlib>
#include <cmath>

// 最小化 JSON 解析器，仅覆盖谱面所需子集
enum class JsonType { Null, Bool, Number, String, Array, Object };

struct JsonValue {
    JsonType type = JsonType::Null;
    double num = 0;
    bool bval = false;
    std::string str;
    std::vector<JsonValue> arr;
    std::vector<std::pair<std::string, JsonValue>> obj;

    const JsonValue& operator[](const char* key) const {
        for (auto& [k, v] : obj)
            if (k == key) return v;
        static JsonValue nil;
        return nil;
    }
    const JsonValue& operator[](size_t i) const {
        static JsonValue nil;
        return i < arr.size() ? arr[i] : nil;
    }
    double asNum(double def = 0) const { return type == JsonType::Number ? num : def; }
    const std::string& asStr() const { static std::string e; return type == JsonType::String ? str : e; }
    size_t size() const { return type == JsonType::Array ? arr.size() : obj.size(); }
};

class JsonParser {
    const char* p;
    void skip() {
        while (*p == ' ' || *p == '\n' || *p == '\r' || *p == '\t') p++;
    }
    char next() { skip(); return *p++; }
    char peek() { skip(); return *p; }
    void expect(char c) { next(); /* silently skip mismatches */ }

    std::string parseStr() {
        expect('"');
        std::string s;
        while (*p && *p != '"') {
            if (*p == '\\') {
                p++;
                if (*p == 'n') s += '\n';
                else if (*p == 't') s += '\t';
                else if (*p == '\\') s += '\\';
                else if (*p == '"') s += '"';
                else s += *p;
                p++;
            } else {
                s += *p++;
            }
        }
        if (*p == '"') p++;
        return s;
    }

    JsonValue parseNum() {
        char* end;
        double v = strtod(p, &end);
        p = end;
        return {JsonType::Number, v, false, "", {}, {}};
    }

    JsonValue parseValue() {
        char c = peek();
        if (c == '"') { JsonValue v; v.type = JsonType::String; v.str = parseStr(); return v; }
        if (c == '{') return parseObj();
        if (c == '[') return parseArr();
        if (c == 't') { p += 4; return {JsonType::Bool, 0, true, "", {}, {}}; }
        if (c == 'f') { p += 5; return {JsonType::Bool, 0, false, "", {}, {}}; }
        if (c == 'n') { p += 4; return {JsonType::Null, 0, false, "", {}, {}}; }
        return parseNum();
    }

    JsonValue parseArr() {
        expect('[');
        JsonValue v; v.type = JsonType::Array;
        while (peek() != ']' && *p) {
            v.arr.push_back(parseValue());
            if (peek() == ',') next();
        }
        if (peek() == ']') next();
        return v;
    }

    JsonValue parseObj() {
        expect('{');
        JsonValue v; v.type = JsonType::Object;
        while (peek() != '}' && *p) {
            std::string key = parseStr();
            expect(':');
            v.obj.push_back({key, parseValue()});
            if (peek() == ',') next();
        }
        if (peek() == '}') next();
        return v;
    }

public:
    JsonValue parse(const char* json) {
        p = json;
        return parseValue();
    }
};

inline JsonValue parseJson(const std::string& text) {
    JsonParser parser;
    return parser.parse(text.c_str());
}
