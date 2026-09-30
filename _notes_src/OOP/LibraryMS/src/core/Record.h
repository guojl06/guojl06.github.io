#ifndef LIBRARYMS_RECORD_H
#define LIBRARYMS_RECORD_H

#include <string>
#include "Date.h"

// 借还记录：一条记录 = 某用户借了某本书 + 借出/到期/归还日期 + 状态。
// 状态是动态计算的：是否逾期取决于"今天"。
class Record {
public:
    enum class Status { Borrowed, Returned, Overdue };

    Record();
    Record(const std::string& recordId,
           const std::string& userId,
           const std::string& bookId,
           const Date& borrowDate,
           const Date& dueDate);

    const std::string& recordId() const { return recordId_; }
    const std::string& userId() const   { return userId_; }
    const std::string& bookId() const   { return bookId_; }
    const Date& borrowDate() const      { return borrowDate_; }
    const Date& dueDate() const         { return dueDate_; }
    const Date& returnDate() const      { return returnDate_; }
    bool isReturned() const             { return returned_; }

    Status status(const Date& today) const;            // 综合状态
    std::string statusString(const Date& today) const; // 中文状态文本
    int overdueDays(const Date& today) const;          // 逾期天数（未逾期为 0）
    void markReturned(const Date& returnDate);         // 标记归还

private:
    std::string recordId_, userId_, bookId_;
    Date borrowDate_, dueDate_, returnDate_;
    bool returned_;
};

#endif // LIBRARYMS_RECORD_H
