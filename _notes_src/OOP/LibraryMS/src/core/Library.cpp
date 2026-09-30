#include "Library.h"
#include "Validator.h"

#include <algorithm>
#include <cctype>
#include <iomanip>
#include <sstream>

namespace {
// ASCII 小写化（中文字节不受影响，因此中文子串匹配仍正确）
std::string toLower(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(),
                   [](unsigned char c) { return std::tolower(c); });
    return s;
}
// 忽略大小写的"包含"
bool containsCI(const std::string& hay, const std::string& needle) {
    if (needle.empty()) return true;
    return toLower(hay).find(toLower(needle)) != std::string::npos;
}
} // namespace

Library::Library() : today_(Date::today()) {}

// —— ID 生成 ——
std::string Library::genBookId() {
    ++bookSeq_;
    std::ostringstream os;
    os << 'B' << std::setw(4) << std::setfill('0') << bookSeq_;
    return os.str();
}
std::string Library::genUserId() {
    ++userSeq_;
    std::ostringstream os;
    os << 'U' << std::setw(4) << std::setfill('0') << userSeq_;
    return os.str();
}
std::string Library::genRecordId() {
    ++recordSeq_;
    std::ostringstream os;
    os << 'R' << std::setw(4) << std::setfill('0') << recordSeq_;
    return os.str();
}

// —— 图书管理 ——
OpResult Library::addBook(const std::string& title, const std::string& author,
                          const std::string& publisher, const std::string& category,
                          const std::string& isbn, int year, int totalCopies) {
    std::string t = Validator::trim(title);
    if (t.empty()) return {false, "书名不能为空", ""};
    if (Validator::trim(author).empty()) return {false, "作者不能为空", ""};
    std::string is = Validator::trim(isbn);
    if (!is.empty() && !Validator::isValidISBN(is))
        return {false, "ISBN 格式不正确（应为 10/13 位数字，可含 -）", ""};
    if (!Validator::isValidYear(year)) return {false, "出版年份不合法", ""};
    if (totalCopies <= 0) return {false, "馆藏数量必须为正整数", ""};

    std::string id = genBookId();
    books_.emplace(id, Book(id, t, Validator::trim(author), Validator::trim(publisher),
                            Validator::trim(category), is, year, totalCopies));
    return {true, "图书添加成功", id};
}

OpResult Library::updateBook(const std::string& id, const std::string& title,
                             const std::string& author, const std::string& publisher,
                             const std::string& category, const std::string& isbn,
                             int year, int totalCopies) {
    auto it = books_.find(id);
    if (it == books_.end()) return {false, "该图书不存在", ""};

    std::string t = Validator::trim(title);
    if (t.empty()) return {false, "书名不能为空", ""};
    if (Validator::trim(author).empty()) return {false, "作者不能为空", ""};
    std::string is = Validator::trim(isbn);
    if (!is.empty() && !Validator::isValidISBN(is))
        return {false, "ISBN 格式不正确（应为 10/13 位数字，可含 -）", ""};
    if (!Validator::isValidYear(year)) return {false, "出版年份不合法", ""};
    if (totalCopies <= 0) return {false, "馆藏数量必须为正整数", ""};

    Book& b = it->second;
    b.setTitle(t);
    b.setAuthor(Validator::trim(author));
    b.setPublisher(Validator::trim(publisher));
    b.setCategory(Validator::trim(category));
    b.setIsbn(is);
    b.setYear(year);
    b.setTotalCopies(totalCopies);
    return {true, "图书信息已更新", ""};
}

OpResult Library::removeBook(const std::string& id) {
    auto it = books_.find(id);
    if (it == books_.end()) return {false, "该图书不存在", ""};
    for (const auto& r : records_)
        if (r.bookId() == id && !r.isReturned())
            return {false, "存在未归还的借阅记录，无法删除该图书", ""};
    books_.erase(it);
    return {true, "图书已删除", ""};
}

Book* Library::findBook(const std::string& id) {
    auto it = books_.find(id);
    return it == books_.end() ? nullptr : &it->second;
}

std::vector<const Book*> Library::allBooks() const {
    std::vector<const Book*> v;
    for (const auto& p : books_) v.push_back(&p.second);
    return v;
}

std::vector<const Book*> Library::searchBooks(const std::string& keyword,
                                              BookField field) const {
    std::string kw = Validator::trim(keyword);
    std::vector<const Book*> v;
    for (const auto& p : books_) {
        const Book& b = p.second;
        bool match = kw.empty();
        if (!match) {
            switch (field) {
                case BookField::Title:    match = containsCI(b.title(), kw); break;
                case BookField::Author:   match = containsCI(b.author(), kw); break;
                case BookField::Category: match = containsCI(b.category(), kw); break;
                case BookField::Isbn:     match = containsCI(b.isbn(), kw); break;
                case BookField::All:
                    match = containsCI(b.title(), kw) || containsCI(b.author(), kw) ||
                            containsCI(b.category(), kw) || containsCI(b.isbn(), kw) ||
                            containsCI(b.publisher(), kw) || containsCI(b.bookId(), kw);
                    break;
            }
        }
        if (match) v.push_back(&b);
    }
    return v;
}

// —— 用户管理 ——
OpResult Library::addUser(User::Type type, const std::string& name,
                          const std::string& gender, const std::string& phone) {
    if (!Validator::isValidName(name))
        return {false, "姓名不能为空且不超过 30 字", ""};
    if (!Validator::isValidGender(gender))
        return {false, "性别只能填 \"男\" 或 \"女\"", ""};
    if (!Validator::isValidPhone(phone))
        return {false, "手机号需为 11 位数字且以 1 开头", ""};

    std::string id = genUserId();
    std::unique_ptr<User> u;
    if (type == User::Type::Student)
        u = std::make_unique<Student>(id, name, gender, phone);
    else
        u = std::make_unique<Teacher>(id, name, gender, phone);
    users_.emplace(id, std::move(u));
    return {true, "用户添加成功", id};
}

OpResult Library::updateUser(const std::string& id, const std::string& name,
                             const std::string& gender, const std::string& phone) {
    auto it = users_.find(id);
    if (it == users_.end()) return {false, "该用户不存在", ""};
    if (!Validator::isValidName(name))
        return {false, "姓名不能为空且不超过 30 字", ""};
    if (!Validator::isValidGender(gender))
        return {false, "性别只能填 \"男\" 或 \"女\"", ""};
    if (!Validator::isValidPhone(phone))
        return {false, "手机号需为 11 位数字且以 1 开头", ""};

    it->second->setName(name);
    it->second->setGender(gender);
    it->second->setPhone(phone);
    return {true, "用户信息已更新", ""};
}

OpResult Library::removeUser(const std::string& id) {
    auto it = users_.find(id);
    if (it == users_.end()) return {false, "该用户不存在", ""};
    for (const auto& r : records_)
        if (r.userId() == id && !r.isReturned())
            return {false, "该用户有未归还的图书，无法删除", ""};
    users_.erase(it);
    return {true, "用户已删除", ""};
}

User* Library::findUser(const std::string& id) {
    auto it = users_.find(id);
    return it == users_.end() ? nullptr : it->second.get();
}

std::vector<const User*> Library::allUsers() const {
    std::vector<const User*> v;
    for (const auto& p : users_) v.push_back(p.second.get());
    return v;
}

int Library::userCurrentBorrowed(const std::string& userId) const {
    int n = 0;
    for (const auto& r : records_)
        if (r.userId() == userId && !r.isReturned()) ++n;
    return n;
}

// —— 借还 ——
OpResult Library::borrowBook(const std::string& userId, const std::string& bookId,
                             int borrowDays) {
    User* u = findUser(userId);
    if (!u) return {false, "用户不存在", ""};
    Book* b = findBook(bookId);
    if (!b) return {false, "图书不存在", ""};
    if (b->availableCopies() <= 0)
        return {false, "《" + b->title() + "》暂无可用副本", ""};
    if (userCurrentBorrowed(userId) >= u->maxBorrowLimit())
        return {false, "已达借阅上限（" + std::to_string(u->maxBorrowLimit()) + " 本）", ""};
    for (const auto& r : records_)
        if (r.userId() == userId && r.bookId() == bookId && !r.isReturned())
            return {false, "您已借阅该书且尚未归还", ""};

    int days = (borrowDays > 0) ? borrowDays : 30;
    b->borrowOut();
    Date due = today_.addDays(days);
    std::string rid = genRecordId();
    records_.emplace_back(rid, userId, bookId, today_, due);
    return {true, "借阅成功，到期日 " + due.toString(), rid};
}

OpResult Library::returnBook(const std::string& recordId) {
    Record* r = findRecord(recordId);
    if (!r) return {false, "借阅记录不存在", ""};
    if (r->isReturned()) return {false, "该记录已归还", ""};
    Book* b = findBook(r->bookId());
    if (b) b->returnBack();
    r->markReturned(today_);
    return {true, "归还成功", ""};
}

Record* Library::findRecord(const std::string& id) {
    for (auto& r : records_)
        if (r.recordId() == id) return &r;
    return nullptr;
}

std::vector<const Record*> Library::allRecords() const {
    std::vector<const Record*> v;
    for (const auto& r : records_) v.push_back(&r);
    return v;
}

// —— 统计分析 ——
std::vector<Library::BookStat> Library::mostPopularBooks(int topN) const {
    std::map<std::string, int> cnt;
    for (const auto& r : records_) cnt[r.bookId()]++;
    std::vector<BookStat> v;
    for (const auto& p : cnt) {
        auto it = books_.find(p.first);
        std::string title = (it != books_.end()) ? it->second.title() : "(已删除)";
        v.push_back({p.first, title, p.second});
    }
    std::sort(v.begin(), v.end(),
              [](const BookStat& a, const BookStat& b) { return a.count > b.count; });
    if (static_cast<int>(v.size()) > topN) v.resize(topN);
    return v;
}

std::vector<Library::UserStat> Library::topBorrowers(int topN) const {
    std::map<std::string, int> cnt;
    for (const auto& r : records_) cnt[r.userId()]++;
    std::vector<UserStat> v;
    for (const auto& p : cnt) {
        auto it = users_.find(p.first);
        std::string name = (it != users_.end()) ? it->second->name() : "(已删除)";
        v.push_back({p.first, name, p.second});
    }
    std::sort(v.begin(), v.end(),
              [](const UserStat& a, const UserStat& b) { return a.count > b.count; });
    if (static_cast<int>(v.size()) > topN) v.resize(topN);
    return v;
}

std::vector<Library::MonthStat> Library::borrowTrendByMonth(int recentMonths) const {
    std::vector<MonthStat> res;
    if (recentMonths <= 0) return res;
    int y = today_.year(), m = today_.month();
    std::vector<std::pair<int, int>> months;
    for (int i = recentMonths - 1; i >= 0; --i) {
        int ty = y, tm = m - i;
        while (tm <= 0) { tm += 12; --ty; }
        months.emplace_back(ty, tm);
    }
    std::map<std::pair<int, int>, int> cnt;
    for (const auto& mm : months) cnt[mm] = 0;
    for (const auto& r : records_) {
        std::pair<int, int> key{r.borrowDate().year(), r.borrowDate().month()};
        auto it = cnt.find(key);
        if (it != cnt.end()) it->second++;
    }
    for (const auto& mm : months) {
        std::ostringstream os;
        os << mm.first << '-';
        if (mm.second < 10) os << '0';
        os << mm.second;
        res.push_back({os.str(), cnt[mm]});
    }
    return res;
}

// —— 持久化 ——
void Library::reloadFrom(const std::map<std::string, Book>& books,
                         std::vector<std::unique_ptr<User>> users,
                         std::vector<Record> records) {
    books_ = books;
    records_ = std::move(records);
    users_.clear();
    for (auto& u : users) {
        std::string id = u->userId();
        users_.emplace(id, std::move(u));
    }
    rebuildCounters();
}

void Library::clearAll() {
    books_.clear();
    users_.clear();
    records_.clear();
    bookSeq_ = userSeq_ = recordSeq_ = 0;
}

void Library::rebuildCounters() {
    auto parseSeq = [](const std::string& id) -> int {
        int i = static_cast<int>(id.size()) - 1, val = 0, mult = 1;
        while (i >= 0 && std::isdigit(static_cast<unsigned char>(id[i]))) {
            val += (id[i] - '0') * mult;
            mult *= 10;
            --i;
        }
        return val;
    };
    int b = 0, u = 0, r = 0;
    for (const auto& p : books_)  b = std::max(b, parseSeq(p.first));
    for (const auto& p : users_)  u = std::max(u, parseSeq(p.first));
    for (const auto& rec : records_) r = std::max(r, parseSeq(rec.recordId()));
    bookSeq_ = b;
    userSeq_ = u;
    recordSeq_ = r;
}
