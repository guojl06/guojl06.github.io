#ifndef LIBRARYMS_LIBRARY_H
#define LIBRARYMS_LIBRARY_H

#include <string>
#include <vector>
#include <map>
#include <memory>

#include "Book.h"
#include "User.h"
#include "Record.h"

// 业务操作的统一返回：成功与否 + 提示信息（+ 必要时新建对象的 ID）。
struct OpResult {
    bool ok = false;
    std::string message;
    std::string id;   // 新建图书/用户/记录时携带其 ID
};

// 系统核心：聚合所有图书、用户、借还记录，对外提供业务方法。
// 体现「面向对象」——内部用封装好的领域对象 + STL 容器，外部只关心业务语义。
class Library {
public:
    Library();

    // —— 图书管理 ——
    OpResult addBook(const std::string& title, const std::string& author,
                     const std::string& publisher, const std::string& category,
                     const std::string& isbn, int year, int totalCopies);
    OpResult updateBook(const std::string& id, const std::string& title,
                        const std::string& author, const std::string& publisher,
                        const std::string& category, const std::string& isbn,
                        int year, int totalCopies);
    OpResult removeBook(const std::string& id);
    Book* findBook(const std::string& id);
    std::vector<const Book*> allBooks() const;

    enum class BookField { All, Title, Author, Category, Isbn };
    // 模糊查询：keyword 为空返回全部；匹配方式为"包含"，不区分 ASCII 大小写。
    std::vector<const Book*> searchBooks(const std::string& keyword,
                                         BookField field = BookField::All) const;

    // —— 用户管理 ——
    OpResult addUser(User::Type type, const std::string& name,
                     const std::string& gender, const std::string& phone);
    OpResult updateUser(const std::string& id, const std::string& name,
                        const std::string& gender, const std::string& phone);
    OpResult removeUser(const std::string& id);
    User* findUser(const std::string& id);
    std::vector<const User*> allUsers() const;
    int userCurrentBorrowed(const std::string& userId) const;   // 当前未还数量

    // —— 借还 ——
    OpResult borrowBook(const std::string& userId, const std::string& bookId,
                        int borrowDays = 30);
    OpResult returnBook(const std::string& recordId);
    Record* findRecord(const std::string& id);
    std::vector<const Record*> allRecords() const;

    // —— 统计分析 ——
    struct BookStat  { std::string id; std::string title; int count; };
    struct UserStat  { std::string id; std::string name; int count; };
    struct MonthStat { std::string month; int count; };   // "YYYY-MM"

    std::vector<BookStat>  mostPopularBooks(int topN) const;  // 历史借阅次数最多的书
    std::vector<UserStat>  topBorrowers(int topN) const;      // 借阅次数最多的用户
    std::vector<MonthStat> borrowTrendByMonth(int recentMonths) const; // 近 N 个月借阅量

    // —— 时间 ——
    Date today() const { return today_; }
    void setTodayForDemo(const Date& d) { today_ = d; }  // 演示/测试用

    // —— 持久化支持（供 DataManager 调用）——
    void reloadFrom(const std::map<std::string, Book>& books,
                    std::vector<std::unique_ptr<User>> users,
                    std::vector<Record> records);
    void clearAll();

private:
    std::string genBookId();
    std::string genUserId();
    std::string genRecordId();
    void rebuildCounters();   // 从已有数据推断各 ID 计数器

    std::map<std::string, Book> books_;
    std::map<std::string, std::unique_ptr<User>> users_;
    std::vector<Record> records_;

    int bookSeq_ = 0, userSeq_ = 0, recordSeq_ = 0;
    Date today_;
};

#endif // LIBRARYMS_LIBRARY_H
