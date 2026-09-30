#ifndef LIBRARYMS_BOOK_H
#define LIBRARYMS_BOOK_H

#include <string>

// 图书类：体现「封装」——所有字段私有，外部仅通过接口读写。
// 副本数管理：borrowOut / returnBack 保证 availableCopies 始终在 [0, totalCopies]。
class Book {
public:
    Book();
    Book(const std::string& bookId,
         const std::string& title,
         const std::string& author,
         const std::string& publisher,
         const std::string& category,
         const std::string& isbn,
         int year,
         int totalCopies);

    const std::string& bookId() const     { return bookId_; }
    const std::string& title() const      { return title_; }
    const std::string& author() const     { return author_; }
    const std::string& publisher() const  { return publisher_; }
    const std::string& category() const   { return category_; }
    const std::string& isbn() const       { return isbn_; }
    int year() const                      { return year_; }
    int totalCopies() const               { return totalCopies_; }
    int availableCopies() const           { return availableCopies_; }
    int borrowedCount() const;            // 已借出 = total - available

    void setTitle(const std::string&);
    void setAuthor(const std::string&);
    void setPublisher(const std::string&);
    void setCategory(const std::string&);
    void setIsbn(const std::string&);
    void setYear(int);
    void setTotalCopies(int n);           // 调整馆藏总量，保持已借出数不变

    bool borrowOut();                     // 可用副本 -1，库存为 0 返回 false
    bool returnBack();                    // 可用副本 +1，已满返回 false

    friend class DataManager;   // 持久化时直接恢复可用副本数

private:
    std::string bookId_, title_, author_, publisher_, category_, isbn_;
    int year_;
    int totalCopies_;
    int availableCopies_;
};

#endif // LIBRARYMS_BOOK_H
