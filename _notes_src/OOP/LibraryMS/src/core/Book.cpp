#include "Book.h"

Book::Book()
    : year_(0), totalCopies_(0), availableCopies_(0) {}

Book::Book(const std::string& bookId,
           const std::string& title,
           const std::string& author,
           const std::string& publisher,
           const std::string& category,
           const std::string& isbn,
           int year,
           int totalCopies)
    : bookId_(bookId), title_(title), author_(author), publisher_(publisher),
      category_(category), isbn_(isbn), year_(year),
      totalCopies_(totalCopies), availableCopies_(totalCopies) {}

int Book::borrowedCount() const { return totalCopies_ - availableCopies_; }

void Book::setTitle(const std::string& v)     { title_ = v; }
void Book::setAuthor(const std::string& v)    { author_ = v; }
void Book::setPublisher(const std::string& v) { publisher_ = v; }
void Book::setCategory(const std::string& v)  { category_ = v; }
void Book::setIsbn(const std::string& v)      { isbn_ = v; }
void Book::setYear(int y)                     { year_ = y; }

void Book::setTotalCopies(int n) {
    if (n < 0) n = 0;
    int borrowed = borrowedCount();
    if (n < borrowed) n = borrowed;   // 不能少于当前已借出的数量
    totalCopies_ = n;
    availableCopies_ = n - borrowed;
}

bool Book::borrowOut() {
    if (availableCopies_ <= 0) return false;
    --availableCopies_;
    return true;
}

bool Book::returnBack() {
    if (availableCopies_ >= totalCopies_) return false;
    ++availableCopies_;
    return true;
}
