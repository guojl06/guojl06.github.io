#include "DataManager.h"
#include "Validator.h"

#include <fstream>
#include <vector>
#include <sys/stat.h>

namespace {
std::string joinPath(const std::string& dir, const std::string& f) {
    if (dir.empty()) return f;
    if (dir.back() == '/') return dir + f;
    return dir + "/" + f;
}
bool fileExists(const std::string& p) {
    struct stat st;
    return stat(p.c_str(), &st) == 0;
}
std::vector<std::string> split(const std::string& line, char delim) {
    std::vector<std::string> out;
    std::string cur;
    for (char c : line) {
        if (c == delim) { out.push_back(cur); cur.clear(); }
        else cur.push_back(c);
    }
    out.push_back(cur);
    return out;
}
} // namespace

DataManager::DataManager(const std::string& dataDir) : dataDir_(dataDir) {}

bool DataManager::hasData() const {
    return fileExists(joinPath(dataDir_, "books.txt"));
}

bool DataManager::save(const Library& lib) const {
    // books.txt: id|title|author|publisher|category|isbn|year|total|available
    {
        std::ofstream ofs(joinPath(dataDir_, "books.txt"));
        if (!ofs) return false;
        for (const Book* b : lib.allBooks()) {
            ofs << b->bookId() << '|' << b->title() << '|' << b->author() << '|'
                << b->publisher() << '|' << b->category() << '|' << b->isbn() << '|'
                << b->year() << '|' << b->totalCopies() << '|' << b->availableCopies() << '\n';
        }
    }
    // users.txt: id|type(S/T)|name|gender|phone|registerDate
    {
        std::ofstream ofs(joinPath(dataDir_, "users.txt"));
        if (!ofs) return false;
        for (const User* u : lib.allUsers()) {
            char t = (u->userType() == User::Type::Student) ? 'S' : 'T';
            ofs << u->userId() << '|' << t << '|' << u->name() << '|' << u->gender() << '|'
                << u->phone() << '|' << u->registerDate().toString() << '\n';
        }
    }
    // records.txt: id|userId|bookId|borrowDate|dueDate|returnDate|returned(0/1)
    {
        std::ofstream ofs(joinPath(dataDir_, "records.txt"));
        if (!ofs) return false;
        for (const Record* r : lib.allRecords()) {
            ofs << r->recordId() << '|' << r->userId() << '|' << r->bookId() << '|'
                << r->borrowDate().toString() << '|' << r->dueDate().toString() << '|';
            if (r->isReturned()) ofs << r->returnDate().toString();
            ofs << '|' << (r->isReturned() ? 1 : 0) << '\n';
        }
    }
    return true;
}

bool DataManager::load(Library& lib) const {
    std::string bp = joinPath(dataDir_, "books.txt");
    if (!fileExists(bp)) return false;     // 首次运行：无任何数据

    std::map<std::string, Book> books;
    std::vector<std::unique_ptr<User>> users;
    std::vector<Record> records;

    // —— 图书 ——
    {
        std::ifstream ifs(bp);
        std::string line;
        while (std::getline(ifs, line)) {
            if (line.empty()) continue;
            std::vector<std::string> f = split(line, '|');
            if (f.size() < 9) continue;
            Book b(f[0], f[1], f[2], f[3], f[4], f[5],
                   Validator::toInt(f[6], 0), Validator::toInt(f[7], 0));
            b.availableCopies_ = Validator::toInt(f[8], b.availableCopies_);  // friend
            books.emplace(f[0], std::move(b));
        }
    }
    // —— 用户 ——
    {
        std::ifstream ifs(joinPath(dataDir_, "users.txt"));
        std::string line;
        while (std::getline(ifs, line)) {
            if (line.empty()) continue;
            std::vector<std::string> f = split(line, '|');
            if (f.size() < 6) continue;
            std::unique_ptr<User> u;
            char t = f[1].empty() ? 'S' : f[1][0];
            if (t == 'T')
                u = std::make_unique<Teacher>(f[0], f[2], f[3], f[4]);
            else
                u = std::make_unique<Student>(f[0], f[2], f[3], f[4]);
            u->registerDate_ = Date::fromString(f[5]);   // friend
            users.push_back(std::move(u));
        }
    }
    // —— 借还记录 ——
    {
        std::ifstream ifs(joinPath(dataDir_, "records.txt"));
        std::string line;
        while (std::getline(ifs, line)) {
            if (line.empty()) continue;
            std::vector<std::string> f = split(line, '|');
            if (f.size() < 7) continue;
            Record rec(f[0], f[1], f[2], Date::fromString(f[3]), Date::fromString(f[4]));
            if (f[6] == "1") rec.markReturned(Date::fromString(f[5]));
            records.push_back(std::move(rec));
        }
    }

    lib.reloadFrom(books, std::move(users), std::move(records));
    return true;
}
