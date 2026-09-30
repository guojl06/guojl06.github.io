#ifndef LIBRARYMS_BOOKTAB_H
#define LIBRARYMS_BOOKTAB_H

#include <QWidget>
#include <vector>
#include "../core/Library.h"

class QLineEdit;
class QComboBox;
class QTableWidget;
class QLabel;
class Book;

// 图书管理页：搜索（模糊查询）+ 表格 + 增/改/删。
class BookTab : public QWidget {
    Q_OBJECT
public:
    explicit BookTab(Library* lib, QWidget* parent = nullptr);

public slots:
    void refresh();          // 重新载入（其它页数据变化时被调用）
    void onSearch();

signals:
    void dataChanged();      // 本页修改了数据，通知其它页刷新

private slots:
    void onAdd();
    void onEdit();
    void onDelete();

private:
    void fillTable(const std::vector<const Book*>& rows);
    QString currentId() const;

    Library* lib_;
    QLineEdit* searchEdit_;
    QComboBox* fieldCombo_;
    QTableWidget* table_;
    QLabel* countLabel_;
};

#endif // LIBRARYMS_BOOKTAB_H
