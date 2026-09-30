#include "Record.h"

Record::Record() : returned_(false) {}

Record::Record(const std::string& recordId,
               const std::string& userId,
               const std::string& bookId,
               const Date& borrowDate,
               const Date& dueDate)
    : recordId_(recordId), userId_(userId), bookId_(bookId),
      borrowDate_(borrowDate), dueDate_(dueDate), returned_(false) {}

Record::Status Record::status(const Date& today) const {
    if (returned_) return Status::Returned;
    if (today - dueDate_ > 0) return Status::Overdue;   // 超过到期日 -> 逾期
    return Status::Borrowed;
}

std::string Record::statusString(const Date& today) const {
    switch (status(today)) {
        case Status::Returned: return "已归还";
        case Status::Overdue:  return "已逾期";
        default:               return "借阅中";
    }
}

int Record::overdueDays(const Date& today) const {
    if (returned_) return 0;
    long diff = today - dueDate_;
    return diff > 0 ? static_cast<int>(diff) : 0;
}

void Record::markReturned(const Date& d) {
    returned_ = true;
    returnDate_ = d;
}
