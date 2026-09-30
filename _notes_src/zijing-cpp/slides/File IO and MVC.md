# File IO and MVC





**\-\-\-**



## **Bilingual reference tables**



### **Table 1: Core concepts**



|Chinese \(中文\)|English|Description|
|---|---|---|
|文件流|File stream|`ifstream` / `ofstream` attach your program to a disk file\.|
|文本模式|Text mode|Formatted I/O; newline translation may happen on some OS\.|
|二进制模式|Binary mode|Raw bytes via `read` / `write`; use for exact layouts\.|
|序列化|Serialization|Write logical state to a file; load reconstructs it\.|
|版本标记|Version stamp|First number in a save file for format evolution\.|
|MVC 模型|Model \(MVC\)|Data \+ rules; no drawing\.|
|MVC 视图|View \(MVC\)|Renders state; read\-only access to model\.|
|MVC 控制器|Controller \(MVC\)|Maps input to model operations\.|



### **Table 2: Symbols \& APIs**



|Symbol / API|English|Chinese \(中文\)|Usage|
|---|---|---|---|
|`std::ifstream`|Input file stream|输入文件流|Read file; test `if (!in)`\.|
|`std::ofstream`|Output file stream|输出文件流|Write file; default truncates\.|
|`<<` / `>>`|Insert / extract|插入 / 提取|Text formatted I/O\.|
|`read` / `write`|Unformatted I/O|无格式读写|Binary buffers; `char*` cast\.|
|`std::getline`|Read a line|读一行|Use for strings that may contain spaces\.|
|`ignore()`|Skip characters|跳过输入|After `>>`, before `getline`\.|



### **Table 3: Chapter terms**



|English|Chinese \(中文\)|Explanation|
|---|---|---|
|Working directory|工作目录|Relative paths resolve from where you launch the program\.|
|Trivially copyable|可平凡拷贝|Safe for `write`/`read` as bytes; not `std::string`\.|
|FEN|局面记号法|One\-line text description of a chess position \(example lab\)\.|



**\-\-\-**



## **Part A — Why files?**



**Problem:** RAM disappears when the process exits — a puzzle best time or Elo rating must live on disk\.  

**Solution:** File streams write **persistent** bytes\.



**\-\-\-**



## **Part A1 — File I/O basics: concepts and syntax \(15 min\)**



### **What is a file stream?**



A **file stream** is a C\+\+ object that acts like a pipe between your program \(in RAM\) and a file \(on disk\)\. You can:

\- **Write** data from program variables → disk file \(save\)

\- **Read** data from disk file → program variables \(load\)



Think of it like a water pipe: water \(data\) flows from one side to the other\.



### **C\+\+ file I/O syntax quick reference**



*\(Expanded detail beyond the opening bilingual tables; the rest of this document is English\-only\.\)*



#### **Core file stream classes**



|Concept|Syntax|Description|
|---|---|---|
|Output file stream \(write\)|`std::ofstream`|Writes data to a file\.|
|Input file stream \(read\)|`std::ifstream`|Reads data from a file\.|
|Read/write file stream|`std::fstream`|Supports both reading and writing on the same file\.|



#### **File open modes \(\`std::ios::…\`\)**



|Concept|Flag|Role|
|---|---|---|
|Binary mode|`std::ios::binary`|Raw bytes; no newline translation or text escaping\.|
|Open at end|`std::ios::ate`|Seek to the end of the file immediately after open\.|
|Append|`std::ios::app`|Every write appends at the end of the file\.|
|Truncate|`std::ios::trunc`|Discard existing file content when opening for output\.|
|Input|`std::ios::in`|Open for reading\.|
|Output|`std::ios::out`|Open for writing\.|



> Note: combine modes with bitwise OR, for example `ios::ate | ios::binary`\.
> 
> 



#### **Common member functions**



|Concept|Syntax|Role|
|---|---|---|
|Binary block write|`stream.write(ptr, len)`|Write `len` bytes from memory to the file\.|
|Binary block read|`stream.read(ptr, len)`|Read `len` bytes from the file into memory\.|
|Read position|`stream.tellg()`|Current read position \(e\.g\. file size if opened at end\)\.|
|Write position|`stream.tellp()`|Current write position\.|
|Seek read pointer|`stream.seekg(offset, origin)`|Move the read pointer\.|
|Seek write pointer|`stream.seekp(offset, origin)`|Move the write pointer\.|
|Open succeeded?|`stream.is_open()`<br>|Whether the file was opened successfully\.|
|At end of file?|`stream.eof()`|Whether the read pointer is at EOF\.|
|Close|`stream.close()`|Release the file \(often optional when the stream is destroyed\)\.|



#### **Seek origins**



|Concept|Flag|Meaning|
|---|---|---|
|Beginning|`std::ios::beg`|Offset from the start of the file\.|
|Current|`std::ios::cur`|Offset from the current position\.|
|End|`std::ios::end`|Offset from the end of the file\.|



#### **Casts and\`sizeof\`**



|Concept|Syntax|Role|
|---|---|---|
|Reinterpret pointer to bytes|`reinterpret_cast<char*>` \(or `const char*`\)|View memory as raw bytes for `read` / `write`\.|
|Size in bytes|`sizeof(expr)` or `sizeof(T)`|How many bytes to read or write for a POD value\.|



#### **Text I/O operators**



|Concept|Syntax|Role|
|---|---|---|
|Insert \(write\)|`stream << value`|Formatted text output\.|
|Extract \(read\)|`stream >> variable`|Formatted text input\.|



#### **Typical code templates**



##### **Binary file write**

```C++
std::ofstream f("a.bin", std::ios::binary);
f.write(reinterpret_cast<const char*>(&val), sizeof(val));
```



### **Get Binary File Size**

```C++
std::ifstream f("a.bin", std::ios::ate | std::ios::binary);
long long fileSize = f.tellg();
```



### **The basic workflow \(4 steps\)**



```C++
#include <fstream>   // Step 0: include header
#include <iostream>

int main() {
    // Step 1: Create stream object (opens file automatically)
    std::ofstream out("data.txt");   // Output stream, creates/truncates "data.txt"
    
    // Step 2: Check if open succeeded (CRITICAL!)
    if (!out) {                        // If open failed
        std::cerr << "Failed to open file!\n";
        return 1;                      // Exit with error
    }
    
    // Step 3: Write data (like using std::cout)
    out << "Hello, file!" << std::endl;  // Writes to file, not screen
    out << 42 << '\n';                   // Numbers become text
    
    // Step 4: Close (automatic via destructor, but can be explicit)
    out.close();                       // Optional: file closes when 'out' goes out of scope
    
    return 0;
}   // Destructor closes file here if not already closed
```



### **Reading from a file**



```C++
#include <fstream>
#include <iostream>
#include <string>

int main() {
    // Step 1: Create input stream
    std::ifstream in("data.txt");      // Tries to open existing file
    
    // Step 2: Check if file exists and is readable
    if (!in) {                         // Also: if (!in.is_open())
        std::cerr << "Cannot open data.txt (file may not exist)\n";
        return 1;
    }
    
    // Step 3: Read data (like using std::cin)
    std::string word;
    int number;
    
    in >> word;        // Reads one word (stops at whitespace)
    in >> number;      // Reads a number, converts from text to int
    
    std::cout << "Read: " << word << " and " << number << '\n';
    
    // Step 4: Check for errors during reading
    if (in.fail()) {
        std::cerr << "Error: expected number but got something else\n";
    }
    
    return 0;
}   // File closes automatically
```



### **Key concepts explained**



|Concept|Explanation|Code example|
|---|---|---|

\| **Constructor opens file** \| When you create \`ifstream\`/\`ofstream\` with a filename, it tries to open immediately \| \`std::ifstream in\("file\.txt"\);\` \|

\| **is\_open\(\)** \| Returns \`true\` if file successfully opened \| \`if \(in\.is\_open\(\)\) \{ /\* safe to read \*/ \}\` \|

\| **\*\*Operator \`\!\`\*\*** \| Tests if stream is in bad state \(failed to open or error\) \| \`if \(\!in\) \{ /\* handle error \*/ \}\` \|

\| **Destructor closes file** \| When stream object goes out of scope, file auto\-closes \(RAII\) \| No manual close needed \|

\| **fail\(\)** \| Returns \`true\` if last operation failed \(wrong type, EOF, etc\.\) \| \`if \(in\.fail\(\)\) \{ /\* error \*/ \}\` \|

\| **eof\(\)** \| Returns \`true\` if end\-of\-file reached \| \`while \(\!in\.eof\(\)\) \{ /\* read \*/ \}\` \|



### **Text mode vs Binary mode \(concept\)**



**Text mode** \(default\):

- Data is formatted as human\-readable text

- `42` becomes characters `'4'` and `'2'` \(2 bytes\)

- Newline characters `\n` may be converted to `\r\n` on Windows

- Use `<<` and `>>` operators

**Binary mode**:

- Data written exactly as bytes in memory

- `42` as `int` is 4 bytes \(binary representation\)

- No newline conversion — exact bytes preserved

- Use `read()` and `write()` member functions

### **Common beginner mistakes**



|Mistake|Why it fails|Correct approach|
|---|---|---|
|Forget to check if file opened|Silent failure, garbage data|Always `if (!stream)` after opening|
|Reading with `>>` for full names|Stops at first space|Use `std::getline(stream, string)` for lines|
|Not including `<fstream>`|Compiler error|Always `#include <fstream>`|
|Using file after error|Undefined behavior|Check `fail()` or test stream in while loop|



**\-\-\-**



## **Example 1 — Minimal: one integer \(\`ex01\_one\_number\.cpp\`\)**



**Chess link:** store the player’s last **rating** as one number\.



**Build:** \`g\+\+ \-std=c\+\+17 \-Wall \-o ex01 ex01\_one\_number\.cpp\`



```C++
// ex01_one_number.cpp — Minimal: write one integer, read it back.
#include <fstream>   // KEY: Must include this header to use file streams
#include <iostream>

int main() {
    const char* path = "score_ex01.txt";  // filename as const char*

    {
        // [KEY SYNTAX] ofstream constructor auto-opens file (write mode, creates if missing, truncates if exists)
        std::ofstream out(path);
        
        // [KEY CHECK] if (!out) is equivalent to if (out.fail()), checks if open failed
        if (!out) {
            std::cerr << "Cannot write " << path << '\n';
            return 1;  // Must handle open failure, otherwise subsequent writes are meaningless
        }
        
        // [KEY SYNTAX] << operator formats data as text, 42 becomes characters '4' and '2'
        out << 42;
    }  // [KEY] Right brace destroys 'out', automatically calls close()

    // [KEY SYNTAX] ifstream for reading, constructor attempts to open file
    std::ifstream in(path);
    int n = 0;
    
    // [KEY] in >> n returns reference to in, testable in if; false if EOF or type error
    if (in >> n)
        std::cout << "Read: " << n << '\n';
    else
        std::cout << "Open or read failed\n";

    return 0;
}
```



**Key Syntax Summary:**

|Syntax|Meaning|Note|
|---|---|---|
|`#include <fstream>`|Include file stream class definitions|Required, otherwise ifstream/ofstream unknown|
|`std::ofstream out(path)`|Create output stream and open file|Default ios::out, truncates existing file|
|`if (!out)`|Check open/write failure|Can also use `!out.is_open()`|
|`out << 42`|Formatted write|Becomes text "42", not 4\-byte binary int|
|Auto\-destructor close|RAII mechanism|Auto\-closes when leaving scope, no manual close\(\) needed|
|`in >> n`|Formatted read|Converts from text to int; fails if file content isn't numeric|



**\-\-\-**



## **Example 2 — Basic: many scores, one per line \(\`ex02\_highscore\_lines\.cpp\`\)**



**Chess link:** top puzzle completion times or tournament points\.



**Build:** \`g\+\+ \-std=c\+\+17 \-Wall \-o ex02 ex02\_highscore\_lines\.cpp\`



```C++
// ex02_highscore_lines.cpp
#include <fstream>
#include <iostream>
#include <vector>

void save_scores(const char* path, const std::vector<int>& scores) {
    std::ofstream out(path);
    if (!out) {                // [KEY] Check inside function, don't assume caller checked
        std::cerr << "save failed\n";
        return;                // Early return, avoid subsequent no-op
    }
    // [KEY SYNTAX] Range-based for loop (C++11), works perfectly with vector
    for (int s : scores)
        out << s << '\n';      // Write newline after each number, "one per line"
}

std::vector<int> load_scores(const char* path) {
    std::vector<int> v;
    std::ifstream in(path);
    if (!in)
        return v;              // [KEY] Return empty vector if file doesn't exist, not an error
    
    int x = 0;
    // [KEY SYNTAX] while (in >> x) is idiomatic: continue if read succeeds, stop on EOF/failure
    while (in >> x)
        v.push_back(x);        // Dynamic append, vector auto-expands
    return v;
}

int main() {
    const char* path = "highscores_ex02.txt";
    // [KEY SYNTAX] C++11 braced initializer list, passed directly to const vector<int>& parameter
    save_scores(path, {2500, 1800, 3200});

    std::cout << "Loaded:";
    for (int s : load_scores(path))
        std::cout << ' ' << s;
    std::cout << '\n';
    return 0;
}
```



**Key syntax summary:**

|Syntax|Meaning|Note|
|---|---|---|
|`std::vector<int>&`|Pass by reference to avoid copying|`const` means the function will not modify the vector\.|
|`while (in >> x)`|Stream used as a condition|True while reads succeed; false at EOF or on failure\.|
|`v.push_back(x)`|Append at the end|`vector` manages memory; no manual pre\-allocation\.|
|`{2500,1800,3200}`|Braced initializer list \(C\+\+11\)|Temporary vector passed to a const reference parameter\.|
|`out << s << '\n'`|Chained insertions|Left\-associative, same as `(out << s) << '\n'`\.|
|Early `return`|Common error\-handling style|Avoids deep nesting of `if`\.|



**\-\-\-**



## **Example 3 — Text vs binary size \(\`ex03\_text\_vs\_binary\_size\.cpp\`\)**



**Idea:** Same value \`1000\` — text characters vs four raw bytes\.



**Build:** \`g\+\+ \-std=c\+\+17 \-Wall \-o ex03 ex03\_text\_vs\_binary\_size\.cpp\`



```C++
// ex03_text_vs_binary_size.cpp
#include <fstream>
#include <iostream>

int main() {
    const int value = 1000;

    {
        std::ofstream t("thousand_text.txt");
        t << value;  // [KEY] Text mode: 1000 becomes 4 characters '1','0','0','0'
    }
    {
        // [KEY SYNTAX] ios::binary flag, prohibits any character conversion (e.g., \n→\r\n)
        std::ofstream b("thousand.bin", std::ios::binary);
        
        // [KEY SYNTAX] reinterpret_cast forces int* to const char*, making write accept it
        // Param 1: Memory start address (byte pointer)
        // Param 2: Byte count (sizeof(int) is typically 4)
        b.write(reinterpret_cast<const char*>(&value), sizeof(value));
    }

    // [KEY SYNTAX] ios::ate = at end, seek to end immediately after opening
    // Combined with tellg() to get file size in bytes right away
    std::ifstream t("thousand_text.txt", std::ios::ate | std::ios::binary);
    std::ifstream bin("thousand.bin", std::ios::ate | std::ios::binary);
    
    // [KEY SYNTAX] tellg() returns current read position (equals file size when opened with ate)
    std::cout << "Text file bytes: " << t.tellg() << '\n';
    std::cout << "Binary file bytes: " << bin.tellg() << '\n';
    return 0;
}
```



**Key syntax summary:**

|Syntax|Meaning|Note|
|---|---|---|
|`std::ios::binary`|Binary mode flag|Pass with the filename in the stream constructor\.|
|`ios::ate`|Seek to end right after open|Often paired with `tellg()` to get file size in bytes\.|
|\`|\` \(bitwise OR\)|Combine open flags|
|`reinterpret_cast`|Reinterpret pointer type|Low\-level but needed here; only for trivial \(POD\) layouts\.|
|`sizeof(value)`|Byte size at compile time|Often 4 for `int`, but platform\-dependent\.|
|`tellg()`|Returns `streampos`|“Tell get”: current read position\.|
|`write(ptr, len)`|Raw byte write|No formatting; copies memory as bytes\.|



**Comparison:**

- Text file: `1000` is four bytes \(characters `'1'`, `'0'`, `'0'`, `'0'`\)\.

- Binary file: the `int` value 1000 is four bytes \(typical little\-endian: `0xE8 0x03 0x00 0x00`\)\.

- Note: for tiny values text size can be smaller by coincidence; for large magnitudes binary is usually more compact\.

**\-\-\-**



## **Example 4 — Trap:\`\>\>\` then \`getline\` \(\`ex04\_extract\_then\_getline\_bug\.cpp\`\)**



**Build:** \`g\+\+ \-std=c\+\+17 \-Wall \-o ex04 ex04\_extract\_then\_getline\_bug\.cpp\`



```C++
// ex04_extract_then_getline_bug.cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    const char* path = "mixed_ex04.txt";
    {
        std::ofstream out(path);
        out << "42\n";           // Write: number + newline
        out << "Hello World\n";  // Write: text + newline
    }

    std::ifstream in(path);
    int num = 0;
    std::string line1;
    std::string line2;

    // [KEY] >> reads 42 then stops, but leaves newline \n in input buffer
    in >> num;
    
    // [TRAP] getline reads the remaining \n (empty line), not "Hello World"
    std::getline(in, line1);
    
    // This one actually reads "Hello World"
    std::getline(in, line2);

    std::cout << "num=" << num << '\n';
    std::cout << "first getline len=" << line1.size() << " repr=\"" << line1 << "\"\n";
    std::cout << "second getline=\"" << line2 << "\"\n";
    return 0;
}
```



**Syntax / trap walkthrough:**

|Step|Consumed|Left in buffer|Issue|
|---|---|---|---|
|`in >> num`|`42`|`\nHello World\n`|Stops before whitespace; newline stays in the buffer\.|
|First `getline`|`\n` \(empty string\)|`Hello World\n`|Immediately hits newline; you get an empty line\.|
|Second `getline`|`Hello World`|\(empty\)|Correct text, but you are “one line off” from what you intended\.|



**Root cause:** \`\>\>\` is *formatted extraction*: it stops at whitespace but does not consume it\. \`getline\` reads from the current position up to the next newline\.



**Fix:** see the next example \(\`ex04b\`\)\.



**\-\-\-**



## **Example 4b — Fix with\`ignore\(\)\` \(\`ex04b\_extract\_then\_getline\_fix\.cpp\`\)**



**Build:** \`g\+\+ \-std=c\+\+17 \-Wall \-o ex04b ex04b\_extract\_then\_getline\_fix\.cpp\`



```C++
// ex04b_extract_then_getline_fix.cpp
#include <fstream>
#include <iostream>
#include <limits>   // [KEY] Provides numeric_limits required for max()
#include <string>

int main() {
    const char* path = "mixed_ex04b.txt";
    {
        std::ofstream out(path);
        out << "42\n";
        out << "Hello World\n";
    }

    std::ifstream in(path);
    int num = 0;
    std::string line;

    in >> num;
    
    // [KEY FIX] ignore() skips until delimiter (2nd param), or max count (1st param)
    // numeric_limits<streamsize>::max() = as many as possible, until newline found
    in.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    
    // Now getline starts from "Hello World", reads correctly
    std::getline(in, line);

    std::cout << "num=" << num << '\n';
    std::cout << "getline=\"" << line << "\"\n";
    return 0;
}
```



**Key syntax:**

|API|Form|Role|Note|
|---|---|---|---|
|`ignore(n, delim)`|Skip up to `n` chars until `delim`|Clears leftover input after `>>`|The delimiter is extracted and discarded\.|
|`numeric_limits<T>::max()`|Largest value of `T`|Use as “read until delimiter” count|Requires `#include <limits>`\.|



**Fix in steps:**

1. After `in >> num`, the buffer is `\nHello World\n`\.

2. `ignore(max, '\n')` discards through and including the first `\n`\.

3. Buffer is now `Hello World\n`\.

4. `getline` reads `Hello World` as intended\.

**Alternative:** if you only need numbers, avoid mixing \`\>\>\` and \`getline\`, or read everything with \`getline\` and parse with \`stoi\` / \`stod\`\.



**\-\-\-**



## **Example 5 — Name with spaces \(\`ex05\_name\_with\_spaces\.cpp\`\)**



**Chess link:** player handle \`"Anna Lee"\` \+ numeric rating\.



**Build:** \`g\+\+ \-std=c\+\+17 \-Wall \-o ex05 ex05\_name\_with\_spaces\.cpp\`



```C++
// ex05_name_with_spaces.cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    const char* path = "player_ex05.txt";
    {
        std::ofstream out(path);
        out << "Anna Lee\n";   // String with spaces
        out << "1600\n";      // Pure number
    }

    std::ifstream in(path);
    std::string name;
    int rating = 0;
    
    // [KEY] getline reads entire line including spaces, until newline
    if (!std::getline(in, name)) {
        std::cerr << "read name failed\n";
        return 1;
    }
    // Buffer state: \n consumed, next is "1600\n"
    
    // [KEY] Use >> to read integer from next line
    if (!(in >> rating)) {
        std::cerr << "read rating failed\n";
        return 1;
    }

    std::cout << "Name: \"" << name << "\" Elo: " << rating << '\n';
    return 0;
}
```



**Syntax comparison:**

|Method|Reads|Stops at|Good for|
|---|---|---|---|
|`in >> str`|One whitespace\-delimited token|Space, tab, newline|Single words without spaces|
|`getline(in, str)`|One full line|`\n` \(consumed, not stored in `str`\)|Names or sentences with spaces|



**File layout strategy:**

- Store one text line, then one numeric line, in a fixed repeating pattern\.

\- Read order must **exactly** match write order\.

- Use `getline` for a full line of text and `>>` for a lone number on its own line; do not mix both on the same line\.

**Error\-handling pattern:**

- Check each read; on failure return an error code \(or `false`\) immediately\.

- Use `if (!(stream >> var))` to test stream state\.

**\-\-\-**



## **Example 6 — Versioned save with\`vector\` \(\`ex06\_versioned\_savegame\.cpp\`\)**





```C++
// ex06_versioned_savegame.cpp
#include <fstream>
#include <iostream>
#include <vector>

struct SaveGameV1 {
    int level = 1;               // C++11: member default initialization
    std::vector<int> inventory_ids;
};

void save(const SaveGameV1& g, const char* path) {
    std::ofstream out(path);
    // [KEY] Serialization protocol: one field per line, write version first (future compatibility)
    out << 1 << '\n';            // Line 1: format version
    out << g.level << '\n';      // Line 2: scalar value
    out << g.inventory_ids.size() << '\n';  // Line 3: vector length
    // [KEY] Write elements one by one, not whole vector (vector has internal pointers, can't write raw)
    for (int id : g.inventory_ids)
        out << id << '\n';       // Line 4+: each element on its own line
}

bool load(SaveGameV1& g, const char* path) {
    std::ifstream in(path);
    if (!in)
        return false;            // File not existing is not a fatal error
    
    int ver = 0;
    in >> ver;
    if (ver != 1)
        return false;            // [KEY] Version mismatch, reject load (prevent data corruption)
    
    in >> g.level;
    std::size_t n = 0;
    in >> n;                     // Read element count
    
    g.inventory_ids.resize(n);   // [KEY] Pre-allocate space, avoid multiple reallocations
    for (std::size_t i = 0; i < n; ++i)
        in >> g.inventory_ids[i];  // Fill directly into reserved slots
    
    // [KEY] Cast to bool to test stream state: false means read error
    return static_cast<bool>(in);
}

int main() {
    const char* path = "save_ex06.txt";

    SaveGameV1 a;
    a.level = 7;
    a.inventory_ids = {10, 20, 30};
    save(a, path);

    SaveGameV1 b;
    if (!load(b, path)) {        // [KEY] Always check return value
        std::cerr << "load failed\n";
        return 1;
    }
    std::cout << "level=" << b.level << " items:";
    for (int x : b.inventory_ids)
        std::cout << ' ' << x;
    std::cout << '\n';
    return 0;
}
```



**Syntax / design patterns:**

|Technique|Code|Role|
|---|---|---|
|Version field|`out << 1 << '\n'`|Room to evolve the save format later\.|
|Length prefix|`out << vec.size()`|Loader knows how many elements follow\.|
|`resize` then fill|`vec.resize(n)`|One allocation instead of many `push_back` reallocations\.|
|Stream as bool|`static_cast<bool>(in)`|Concise “no failure” test \(similar to `!in.fail()`\)\.|
|Default member init|`int level = 1;`|C\+\+11: members get values before the constructor body runs\.|



**Serialization rules:**

- Never `write(&vec, sizeof(vec))` — a `vector` holds pointers; you would save meaningless addresses\.

- Scalars can be text \(`<<`\) or binary \(`write`\), but aggregates must be serialized field by field\.

\- Protocol: whatever order you write, read in the **same** order\.



**\-\-\-**



## **Example 7 — Binary POD struct \(\`ex07\_binary\_pod\_struct\.cpp\`\)**



**Rule:** only trivial layout — good for a simple \`struct\` with \`int\`/\`float\`, not \`std::string\`\.



**Build:** \`g\+\+ \-std=c\+\+17 \-Wall \-o ex07 ex07\_binary\_pod\_struct\.cpp\`



```C++
// ex07_binary_pod_struct.cpp
#include <fstream>
#include <iostream>

// [KEY] POD = Plain Old Data, only basic types, no virtual functions/pointers/string
struct PlayerPod {
    int id = 0;
    float x = 0.f;
    float y = 0.f;
};

int main() {
    const char* path = "player_ex07.bin";

    {
        PlayerPod p{1, 100.f, 200.f};  // C++11: Uniform brace initialization
        std::ofstream out(path, std::ios::binary);
        
        // [KEY] write(address, byte_count), writes entire struct as-is to file
        // &p → reinterpret_cast<const char*> → byte sequence
        out.write(reinterpret_cast<const char*>(&p), sizeof(p));
    }

    PlayerPod q{};  // Value-initialization, all members zeroed
    {
        std::ifstream in(path, std::ios::binary);
        // [KEY] read(target_address, byte_count), reads from file back to memory
        // reinterpret_cast<char*>: note no const needed here since we're writing to memory
        in.read(reinterpret_cast<char*>(&q), sizeof(q));
    }

    std::cout << "Loaded id=" << q.id << " pos=(" << q.x << ", " << q.y << ")\n";
    return 0;
}
```



**Key syntax:**

|API|Arguments|Meaning|
|---|---|---|
|`write(ptr, count)`|Source address, byte count|Copy a memory block verbatim into the file\.|
|`read(ptr, count)`|Destination address, byte count|Copy bytes from the file into memory\.|
|`sizeof(p)`|Compile\-time|Total bytes of `PlayerPod` \(often 12 on typical platforms: one `int` plus two `float`s; sizes are implementation\-defined\)\.|
|`reinterpret_cast`|Type change|Changes how the pointer is interpreted, not the underlying bits\.|



**POD / trivial\-layout checklist:**

- OK: only scalars like `int` / `float` / `double`, or structs of such types\.

- OK: no user\-defined constructors, virtual functions, or inheritance\.

- Not OK: `std::string` \(heap pointer inside\)\.

- Not OK: `std::vector` \(internal dynamic pointers\)\.

- Not OK: polymorphic classes \(vtable pointer layout\)\.

**Risks:**

- Binary layouts are not portable \(endianness, alignment, type sizes\)\.

- Adding fields to the struct breaks old saves unless you version the format\.

\- Prefer **versioned text saves** \(like \`ex06\`\) for game data when you can\.



**\-\-\-**



## **Example 8 — Whole file into\`std::string\` \(\`ex08\_whole\_file\_std\.cpp\`\)**



Teaches the “load entire file” idea in pure C\+\+\. For **raylib** \`LoadFileText\` / \`UnloadFileText\`, see \`file\_IO\.md\` §5 inside your raylib project\.



**Run from** \`ch9\_lab\_examples/\` so \`hello\.txt\` is found\.



**Build:** \`g\+\+ \-std=c\+\+17 \-Wall \-o ex08 ex08\_whole\_file\_std\.cpp\`



```C++
// ex08_whole_file_std.cpp
#include <fstream>
#include <iostream>
#include <sstream>  // [KEY] ostringstream for in-memory string building
#include <string>

std::string load_file_as_string(const char* path) {
    std::ifstream in(path, std::ios::binary);
    if (!in)
        return {};               // [KEY] Return empty string to indicate failure (nullopt style)
    
    std::ostringstream oss;      // String stream: writes like cout, but target is in memory
    
    // [KEY SYNTAX] in.rdbuf() returns the stream's internal buffer pointer (streambuf*)
    // oss << streambuf* is an overload that copies entire file content to oss
    oss << in.rdbuf();
    
    return oss.str();            // Extract all accumulated content from oss as std::string
}

int main() {
    const char* path = "hello.txt";
    std::string s = load_file_as_string(path);
    if (s.empty()) {             // [NOTE] Both empty file and failure return empty, real projects need differentiation
        std::cerr << "Could not read " << path << '\n';
        return 1;
    }
    std::cout << "---- file begin ----\n" << s << "---- file end ----\n";
    return 0;
}
```



**Key syntax:**

|Type / API|Role|Analogy|
|---|---|---|
|`std::ostringstream`|In\-memory output stream|Like `std::cout`, but builds a `std::string`\.|
|`in.rdbuf()`|Access the stream’s buffer|The “pipe” into the file’s bytes\.|
|`oss << in.rdbuf()`|Bulk copy|Faster than a character\-by\-character loop\.|
|`oss.str()`|Get the finished string|Drain everything written into the stream\.|



**\*\*vs raylib \`LoadFileText\`:\*\***

|Approach|Pros|Cons|
|---|---|---|
|This example \(standard library\)|Pure C\+\+, no extra deps, RAII `std::string`|Large files allocate a second full copy in memory\.|
|raylib `LoadFileText`|Simple, tuned API|Must pair with `UnloadFileText`; manual C\-string lifetime\.|



**Typical uses:** config files, small text assets, unit tests that assert on file contents\.



**\-\-\-**



## **Example 9 — One\-line FEN save/load \(\`ex9\_fen\_line\_io\.cpp\`\)**



**Chess link:** persist a **standard one\-line FEN** \(the usual starting position in this lab\) as plain text\.



### **What is FEN? \(Forsyth–Edwards Notation\)**



**FEN** is a *text standard* for describing a *complete chess position* in a single line\. Engines, databases, and websites use it to exchange board states\. For this course, it is a realistic “long string” to practice **text file save/load** with \`std::getline\` \(spaces are part of the data, so line\-based I/O fits well\)\.



A legal FEN string has **six fields**, separated by **spaces**:



|\#|Field|Typical example \(start position\)|Meaning \(short\)|
|---|---|---|---|

\| 1 \| **Piece placement** \| \`rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR\` \| Eight *ranks* from Black’s back rank \(**8**\) down to White’s back rank \(**1**\)\. Within each rank, read left→right \(files **a–h**\)\. A **\*\*\`/\`\*\*** starts the next lower rank\. **Uppercase** letters are White pieces, **lowercase** are Black\. **\*\*Digits \`1\`–\`8\`\*\*** mean “that many empty squares” in a row\. \|

\| 2 \| **Active color** \| \`w\` \| Side to move: **\*\*\`w\`\*\*** = White, **\*\*\`b\`\*\*** = Black\. \|

\| 3 \| **Castling availability** \| \`KQkq\` \| Which king/rook pairs may still castle from their *original* corners \(\`K\`/\`Q\` = White kingside/queenside; \`k\`/\`q\` = Black\)\. Use **\*\*\`\-\`\*\*** if nobody can castle anymore\. \|

\| 4 \| **En passant target square** \| \`\-\` \| If the last move was a pawn double\-step, this is the square *behind* that pawn \(where an en passant capture could land\); otherwise **\*\*\`\-\`\*\***\. \|

\| 5 \| **Halfmove clock** \| \`0\` \| Count of half\-moves since the last pawn move or capture \(used for the 50\-move rule in serious play\)\. \|

\| 6 \| **Fullmove number** \| \`1\` \| Starts at **1**; in standard rules it increments after Black’s move\. \|



**Piece letters in field 1:** \`P/p\` pawn, \`R/r\` rook, \`N/n\` knight, \`B/b\` bishop, \`Q/q\` queen, \`K/k\` king\.

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZTE1NTFmZGNlZWQyZDlkOWQzYzUwYmM1YTA3MzkzNDRfZjAzNDFiMDk3YzJiMWM1MTg4OWZiYjIyYmMyNzBkYWVfSUQ6NzYzOTI0MTI2NTcyNDU3NDkwNV8xNzgxMDYwMjQ3OjE3ODExNDY2NDdfVjM)

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OWM2YWZhZTgyOWZhY2ExOWNlMGExNGI1OWU1MjhhMzhfZjZmYjc3NzBhNmFkYTc1ZjdlYzU2NmI1NDM2ZjNkY2NfSUQ6NzYzOTI0MTI4ODA0MDQxODQ4Ml8xNzgxMDYwMjQ3OjE3ODExNDY2NDdfVjM)



```C++
// ex10_fen_line_io.cpp
#include <fstream>
#include <iostream>
#include <string>

bool save_fen(const char* path, const std::string& fen) {
    std::ofstream out(path);
    if (!out)
        return false;
    out << fen << '\n';
    return true;
}

bool load_fen(const char* path, std::string& fen) {
    std::ifstream in(path);
    if (!std::getline(in, fen))
        return false;
    return true;
}

int main() {
    const char* path = "board_ex10.fen";
    const std::string start =
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";

    if (!save_fen(path, start)) {
        std::cerr << "save failed\n";
        return 1;
    }
    std::string loaded;
    if (!load_fen(path, loaded)) {
        std::cerr << "load failed\n";
        return 1;
    }
    std::cout << "FEN loaded OK, length = " << loaded.size() << '\n';
    return 0;
}
```



**Key Syntax \& Design:**



|Function|Return Type|Parameter Passing|Purpose|
|---|---|---|---|
|`save_fen`|`bool`|`const std::string&` \(const reference\)|Returns success/failure; uses reference to avoid copying long string|
|`load_fen`|`bool`|`std::string&` \(non\-const reference\)|Passes output parameter by reference; writes result to caller's variable|
|`std::getline`|`bool`|stream \+ string reference|Reads entire line including spaces; returns false on EOF or error|



**Reference Passing Patterns:**

- `const std::string& fen` \(input\): read\-only, no copy, efficient for large strings

- `std::string& fen` \(output\): allows function to write result back to caller

**Why use output parameter instead of return value?**

```C++
// Option A: return by value (copies the string)
std::string load_fen(const char* path) { ... }

// Option B: output parameter (no copy, more efficient)
bool load_fen(const char* path, std::string& result) { ... }
```



**Error Handling Strategy:**

- Always check file open before writing

- `getline` returns bool: test it immediately

- Return `false` on any failure so caller can decide what to do

**FEN recap:** The program stores exactly **one line** containing all six fields \(see *What is FEN?* and Figures 1–2 above\)\. That matches \`out \<\< fen \<\< '\\n'\` plus \`std::getline\` on load: portable, human\-readable, and easy to inspect in a text editor\.



**\-\-\-**



## **Part B — MVC Architecture and Game Design \(30 min\)**



### **B1\. The Problem: Spaghetti Code**



**Typical beginner raylib game:**



```C++
int main() {
    InitWindow(800, 600, "Game");
    int playerX = 400, playerY = 300, score = 0;
    
    while (!WindowShouldClose()) {
        // Input + Logic + Drawing ALL MIXED
        if (IsKeyDown(KEY_RIGHT)) playerX += 5;
        if (IsKeyDown(KEY_LEFT))  playerX -= 5;
        
        if (CheckCollision(playerX, playerY, coinX, coinY)) {
            score += 10;  // Logic buried in game loop
            coinX = GetRandomValue(0, 700);
        }
        
        BeginDrawing();
        ClearBackground(RAYWHITE);
        DrawRectangle(playerX, playerY, 40, 40, BLUE);  // Drawing in main
        DrawText(TextFormat("Score: %i", score), 10, 10, 20, BLACK);
        EndDrawing();
    }
}
```



**Problems:**

- Cannot unit test `score += 10` without initializing a window

- Change drawing order → may break collision logic

- Add a second player → copy\-paste variables everywhere

- Save game state → hard to extract what's "data" vs "temporary"

**\-\-\-**



### **B2\. MVC: Separation of Concerns**



**MVC** splits a program into three independent parts:



|Component|Responsibility|What it KNOWS|What it DOES|Chess Analogy|
|---|---|---|---|---|

\| **Model** \| Data \+ Rules \| Game state \(positions, scores, whose turn\) \| Enforce rules, update state \| The chess position \+ legal move rules \|

\| **View** \| Presentation \| Nothing about rules; only how to draw \| Render model on screen \| The physical board and pieces you see \|

\| **Controller** \| Input Handling \| User actions \(clicks, keys\) \| Translate input → model commands \| The player moving pieces \|



**Key principle:**

\- **Model** knows **nothing** about graphics \(no \`Color\`, no \`DrawRectangle\`\)

\- **View** reads **only** from Model \(const reference\), never modifies it

\- **Controller** is the **only** part that modifies Model, through well\-defined methods



**\-\-\-**



### **B3\. Data Flow Diagram**



```Plain Text
User Input (keyboard/mouse)
       ↓
┌─────────────┐
│ Controller  │  → Validates input, calls Model methods
└─────────────┘
       ↓
┌─────────────┐
│    Model    │  → Updates state, enforces rules ("is this move legal?")
└─────────────┘
       ↓ (const reference)
┌─────────────┐
│    View     │  → Reads Model, draws with raylib
└─────────────┘
       ↓
   Screen
```



**Golden Rules:**

1\. **View never calls Model setters** — only getters

2\. **Model never calls raylib** — pure C\+\+ data and logic

3\. **Controller never draws** — only handles input and calls Model



**\-\-\-**



### **B4\. MVC in raylib: "Eat the Coin" Example**



**Game:** Player \(blue square\) moves with arrows to collect gold coins\. Each coin = \+10 points\.



#### **4\.1 Model \(\`GameModel\`\)**



```C++
// GameModel.h - NO raylib includes!
#pragma once

class GameModel {
public:
    // Constants (game rules)
    static constexpr int PLAYER_SIZE = 40;
    static constexpr int COIN_RADIUS = 15;
    static constexpr int WINDOW_W = 800;
    static constexpr int WINDOW_H = 600;
    static constexpr int SPEED = 5;
    
    // Constructor sets initial state
    GameModel();
    
    // Queries (View uses these)
    int getPlayerX() const { return playerX_; }
    int getPlayerY() const { return playerY_; }
    int getCoinX()   const { return coinX_; }
    int getCoinY()   const { return coinY_; }
    int getScore()   const { return score_; }
    
    // Commands (Controller calls these)
    void movePlayer(int dx, int dy);  // Clamps to window bounds
    void update();                      // Checks collision, respawns coin
    void saveToFile(const char* path) const;  // Uses fstream
    bool loadFromFile(const char* path);      // Returns success
    
private:
    int playerX_, playerY_;
    int coinX_, coinY_;
    int score_;
    
    bool checkCollision() const;
    void respawnCoin();
};
```



```C++
// GameModel.cpp
#include "GameModel.h"
#include <algorithm>  // std::clamp
#include <cstdlib>    // rand
#include <fstream>

GameModel::GameModel()
    : playerX_(WINDOW_W/2), playerY_(WINDOW_H/2),
      coinX_(200), coinY_(200), score_(0) {
    respawnCoin();
}

void GameModel::movePlayer(int dx, int dy) {
    playerX_ += dx;
    playerY_ += dy;
    // Enforce boundary rules
    playerX_ = std::clamp(playerX_, 0, WINDOW_W - PLAYER_SIZE);
    playerY_ = std::clamp(playerY_, 0, WINDOW_H - PLAYER_SIZE);
}

bool GameModel::checkCollision() const {
    int px = playerX_ + PLAYER_SIZE/2;
    int py = playerY_ + PLAYER_SIZE/2;
    int dx = px - coinX_;
    int dy = py - coinY_;
    int distSq = dx*dx + dy*dy;
    int threshold = (PLAYER_SIZE/2 + COIN_RADIUS);
    return distSq <= threshold * threshold;
}

void GameModel::update() {
    if (checkCollision()) {
        score_ += 10;      // Rule: coin gives 10 points
        respawnCoin();     // Rule: coin moves randomly
    }
}

void GameModel::respawnCoin() {
    coinX_ = rand() % (WINDOW_W - 2*COIN_RADIUS) + COIN_RADIUS;
    coinY_ = rand() % (WINDOW_H - 2*COIN_RADIUS) + COIN_RADIUS;
}

// Save: version 1 format
void GameModel::saveToFile(const char* path) const {
    std::ofstream out(path);
    out << 1 << '\n';           // version
    out << playerX_ << ' ' << playerY_ << '\n';
    out << coinX_ << ' ' << coinY_ << '\n';
    out << score_ << '\n';
}

bool GameModel::loadFromFile(const char* path) {
    std::ifstream in(path);
    if (!in) return false;
    int ver;
    in >> ver;
    if (ver != 1) return false;
    in >> playerX_ >> playerY_;
    in >> coinX_ >> coinY_;
    in >> score_;
    return static_cast<bool>(in);
}
```



#### **4\.2 View \(\`GameView\`\)**



```C++
// GameView.h
#pragma once
#include "GameModel.h"
#include "raylib.h"

class GameView {
public:
    // Takes const reference - View cannot modify Model!
    void draw(const GameModel& model) const;
    
private:
    void drawPlayer(const GameModel& m) const;
    void drawCoin(const GameModel& m) const;
    void drawUI(const GameModel& m) const;
};
```



```C++
// GameView.cpp
#include "GameView.h"

void GameView::draw(const GameModel& model) const {
    ClearBackground(RAYWHITE);
    drawCoin(model);
    drawPlayer(model);
    drawUI(model);
}

void GameView::drawPlayer(const GameModel& m) const {
    DrawRectangle(
        m.getPlayerX(), 
        m.getPlayerY(),
        GameModel::PLAYER_SIZE,
        GameModel::PLAYER_SIZE,
        BLUE
    );
}

void GameView::drawCoin(const GameModel& m) const {
    DrawCircle(
        m.getCoinX(),
        m.getCoinY(),
        GameModel::COIN_RADIUS,
        GOLD
    );
}

void GameView::drawUI(const GameModel& m) const {
    DrawText(
        TextFormat("Score: %i", m.getScore()),
        10, 10, 20, BLACK
    );
    DrawText("Press S to save, L to load", 10, 40, 20, DARKGRAY);
}
```



#### **4\.3 Controller \(\`GameController\`\)**



```C++
// GameController.h
#pragma once
#include "GameModel.h"

class GameController {
public:
    // Process one frame of input
    void handleInput(GameModel& model);
    
    // Called every frame (handles timing, AI, etc.)
    void update(GameModel& model);
};
```



```C++
// GameController.cpp
#include "GameController.h"
#include "raylib.h"

void GameController::handleInput(GameModel& model) {
    int dx = 0, dy = 0;
    if (IsKeyDown(KEY_RIGHT)) dx += GameModel::SPEED;
    if (IsKeyDown(KEY_LEFT))  dx -= GameModel::SPEED;
    if (IsKeyDown(KEY_DOWN))  dy += GameModel::SPEED;
    if (IsKeyDown(KEY_UP))    dy -= GameModel::SPEED;
    
    // Only Controller modifies Model!
    if (dx != 0 || dy != 0)
        model.movePlayer(dx, dy);
    
    // Save/Load triggered by Controller
    if (IsKeyPressed(KEY_S))
        model.saveToFile("savegame.txt");
    if (IsKeyPressed(KEY_L))
        model.loadFromFile("savegame.txt");
}

void GameController::update(GameModel& model) {
    // Run game logic (collision, scoring)
    model.update();
}
```



#### **4\.4 Main \(wires everything together\)**



```C++
// main.cpp
#include "raylib.h"
#include "GameModel.h"
#include "GameView.h"
#include "GameController.h"

int main() {
    InitWindow(GameModel::WINDOW_W, GameModel::WINDOW_H, "MVC Demo");
    SetTargetFPS(60);
    
    GameModel model;        // Pure data + rules
    GameView view;          // Pure drawing
    GameController ctrl;    // Pure input handling
    
    while (!WindowShouldClose()) {
        // Phase 1: Input → Model updates
        ctrl.handleInput(model);
        ctrl.update(model);
        
        // Phase 2: View renders (never modifies)
        BeginDrawing();
        view.draw(model);
        EndDrawing();
    }
    
    CloseWindow();
    return 0;
}
```



**\-\-\-**



### **B5\. MVC Benefits \(Why bother?\)**



|Without MVC|With MVC|
|---|---|
|Test collision by launching window|Test `model.update()` in console unit test|
|Change blue to green → search whole file|Change one line in `drawPlayer()`|
|Add save/load → spaghetti code|Add `saveToFile()` in Model, trigger from Controller|
|Port to console → rewrite everything|Write `ConsoleView` that prints numbers|
|Two players → copy\-paste mess|Create `Player` class in Model, View draws vector|



**\-\-\-**



### **B6\. MVC \+ File I/O Integration**



**Where does save/load fit?**



```Plain Text
┌─────────────┐         ┌─────────────┐
│ Controller  │──S/L──→│   Model     │
│ (detects    │         │ (has        │
│  key press) │         │  save/load  │
└─────────────┘         │  methods)   │
                        └──────┬──────┘
                               │
                        ┌──────▼──────┐
                        │  File on    │
                        │  Disk       │
                        └─────────────┘
```



**Rule:** View never touches files\. Controller initiates, Model knows the format\.



**In our raylib example:**

\- Press **S** → Controller calls \`model\.saveToFile\("savegame\.txt"\)\`

\- Press **L** → Controller calls \`model\.loadFromFile\("savegame\.txt"\)\`

- Model writes: version, player pos, coin pos, score \(one per line\)

**\-\-\-**



### **B7\. Common MVC Mistakes**



|Mistake|Why Wrong|Correct|
|---|---|---|
|`Texture2D` inside Model|Model depends on raylib, hard to test|Store `int textureID`, load in View|
|View calls `model.setScore(999)`|View modifies state → bugs|Controller validates, then calls setter|
|Controller calls `DrawText`|Mixes input and rendering|Controller only modifies Model; View draws|
|One giant class "Game" with everything|No separation|Three distinct classes with clear interfaces|



**\-\-\-**



### **B8\. Summary: MVC in 3 Lines**



\> **Model** = What is true? \(positions, scores, rules\)  

\> **View** = What do you see? \(colors, shapes, text\)  

\> **Controller** = What did the user do? \(keys, clicks → commands\)



**Next step:** Take your raylib project, separate variables into \`Model\`, move \`Draw\*\` calls into \`View\`, put input handling in \`Controller\`\. The save/load from Part A plugs right into the Model\.





