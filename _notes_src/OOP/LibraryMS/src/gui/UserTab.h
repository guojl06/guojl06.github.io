#ifndef LIBRARYMS_USERTAB_H
#define LIBRARYMS_USERTAB_H

#include <QWidget>
#include <vector>
#include "../core/Library.h"

class QLineEdit;
class QTableWidget;
class QLabel;
class User;

// 用户管理页：搜索 + 表格 + 增/改/删。
// 不同用户类型（学生/教师）的可借数量不同——多态在此体现。
class UserTab : public QWidget {
    Q_OBJECT
public:
    explicit UserTab(Library* lib, QWidget* parent = nullptr);

public slots:
    void refresh();
    void onSearch();

signals:
    void dataChanged();

private slots:
    void onAdd();
    void onEdit();
    void onDelete();

private:
    void fillTable(const std::vector<const User*>& rows);
    QString currentId() const;

    Library* lib_;
    QLineEdit* searchEdit_;
    QTableWidget* table_;
    QLabel* countLabel_;
};

#endif // LIBRARYMS_USERTAB_H
