#include "RecordTab.h"
#include "../core/Record.h"
#include "../core/User.h"
#include "../core/Book.h"

#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QFormLayout>
#include <QGroupBox>
#include <QComboBox>
#include <QSpinBox>
#include <QPushButton>
#include <QTableWidget>
#include <QHeaderView>
#include <QLabel>
#include <QMessageBox>
#include <QAbstractItemView>
#include <QBrush>
#include <QColor>

RecordTab::RecordTab(Library* lib, QWidget* parent)
    : QWidget(parent), lib_(lib) {
    // —— 借书区 ——
    auto* borrowGroup = new QGroupBox("借书");
    auto* borrowLay = new QHBoxLayout(borrowGroup);
    userCombo_ = new QComboBox;
    userCombo_->setMinimumWidth(240);
    bookCombo_ = new QComboBox;
    bookCombo_->setMinimumWidth(280);
    daysSpin_ = new QSpinBox;
    daysSpin_->setRange(1, 180);
    daysSpin_->setValue(30);
    daysSpin_->setSuffix(" 天");
    auto* borrowBtn = new QPushButton("借出");
    borrowLay->addWidget(new QLabel("读者:"));
    borrowLay->addWidget(userCombo_, 3);
    borrowLay->addWidget(new QLabel("图书:"));
    borrowLay->addWidget(bookCombo_, 4);
    borrowLay->addWidget(new QLabel("借期:"));
    borrowLay->addWidget(daysSpin_);
    borrowLay->addWidget(borrowBtn);

    // —— 记录表格区 ——
    auto* tableBar = new QHBoxLayout;
    auto* returnBtn = new QPushButton("归还选中记录");
    auto* refreshBtn = new QPushButton("刷新");
    tableBar->addWidget(returnBtn);
    tableBar->addStretch();
    tableBar->addWidget(refreshBtn);

    table_ = new QTableWidget;
    table_->setColumnCount(8);
    table_->setHorizontalHeaderLabels(
        {"编号", "读者", "图书", "借出日", "到期日", "归还日", "状态", "逾期"});
    table_->setSelectionBehavior(QAbstractItemView::SelectRows);
    table_->setEditTriggers(QAbstractItemView::NoEditTriggers);
    table_->setAlternatingRowColors(true);
    table_->horizontalHeader()->setStretchLastSection(true);
    table_->verticalHeader()->setDefaultSectionSize(26);
    table_->setColumnWidth(0, 70);
    table_->setColumnWidth(2, 220);
    // 让新记录出现在最上方更直观：按编号降序
    table_->setSortingEnabled(true);
    table_->sortByColumn(0, Qt::DescendingOrder);

    countLabel_ = new QLabel;

    auto* mainLay = new QVBoxLayout(this);
    mainLay->addWidget(borrowGroup);
    mainLay->addLayout(tableBar);
    mainLay->addWidget(table_);
    mainLay->addWidget(countLabel_);

    connect(borrowBtn, &QPushButton::clicked, this, &RecordTab::onBorrow);
    connect(returnBtn, &QPushButton::clicked, this, &RecordTab::onReturn);
    connect(refreshBtn, &QPushButton::clicked, this, &RecordTab::refresh);

    refresh();
}

void RecordTab::reloadCombos() {
    // 读者下拉
    userCombo_->clear();
    for (const User* u : lib_->allUsers()) {
        int cur = lib_->userCurrentBorrowed(u->userId());
        QString text = QString("%1 (%2)  [%3/%4]")
                           .arg(QString::fromStdString(u->name()))
                           .arg(QString::fromStdString(u->userId()))
                           .arg(cur).arg(u->maxBorrowLimit());
        userCombo_->addItem(text, QString::fromStdString(u->userId()));
    }
    // 图书下拉（只列出尚有可借副本的）
    bookCombo_->clear();
    for (const Book* b : lib_->allBooks()) {
        if (b->availableCopies() <= 0) continue;
        QString text = QString("%1 (%2)  [可借 %3]")
                           .arg(QString::fromStdString(b->title()))
                           .arg(QString::fromStdString(b->bookId()))
                           .arg(b->availableCopies());
        bookCombo_->addItem(text, QString::fromStdString(b->bookId()));
    }
}

void RecordTab::refresh() {
    reloadCombos();
    fillTable(lib_->allRecords());
}

void RecordTab::fillTable(const std::vector<const Record*>& rows) {
    Date today = lib_->today();
    table_->setSortingEnabled(false);   // 填充时关闭排序
    table_->setRowCount(0);
    int borrowed = 0, overdue = 0;
    for (const Record* r : rows) {
        int i = table_->rowCount();
        table_->insertRow(i);
        auto set = [&](int c, const QString& s) { table_->setItem(i, c, new QTableWidgetItem(s)); };
        set(0, QString::fromStdString(r->recordId()));
        const User* u = lib_->findUser(r->userId());
        const Book* b = lib_->findBook(r->bookId());
        set(1, u ? QString::fromStdString(u->name()) : "(已删除)");
        set(2, b ? QString::fromStdString(b->title()) : "(已删除)");
        set(3, QString::fromStdString(r->borrowDate().toString()));
        set(4, QString::fromStdString(r->dueDate().toString()));
        set(5, r->isReturned() ? QString::fromStdString(r->returnDate().toString()) : "—");
        set(6, QString::fromStdString(r->statusString(today)));
        int od = r->overdueDays(today);
        set(7, od > 0 ? QString::number(od) + " 天" : "—");

        Record::Status s = r->status(today);
        if (s == Record::Status::Overdue) {
            table_->item(i, 6)->setForeground(QBrush(QColor(200, 0, 0)));
            table_->item(i, 7)->setForeground(QBrush(QColor(200, 0, 0)));
            ++overdue;
        } else if (!r->isReturned()) {
            ++borrowed;
        } else {
            // 已归还整行置灰
            for (int c = 0; c < 8; ++c)
                table_->item(i, c)->setForeground(QBrush(QColor(150, 150, 150)));
        }
        for (int c = 0; c < 8; ++c) table_->item(i, c)->setTextAlignment(Qt::AlignCenter);
    }
    table_->setSortingEnabled(true);
    table_->sortByColumn(0, Qt::DescendingOrder);
    countLabel_->setText(QString("共 %1 条记录 ｜ 借阅中 %2 条 ｜ 已逾期 %3 条")
                             .arg(rows.size()).arg(borrowed).arg(overdue));
}

void RecordTab::onBorrow() {
    if (userCombo_->count() == 0) {
        QMessageBox::information(this, "提示", "系统中还没有读者，请先在「用户管理」添加。");
        return;
    }
    if (bookCombo_->count() == 0) {
        QMessageBox::information(this, "提示", "当前没有可借的图书。");
        return;
    }
    QString uid = userCombo_->currentData().toString();
    QString bid = bookCombo_->currentData().toString();
    OpResult r = lib_->borrowBook(uid.toStdString(), bid.toStdString(), daysSpin_->value());
    if (!r.ok) {
        QMessageBox::warning(this, "借阅失败", QString::fromStdString(r.message));
        return;
    }
    refresh();
    emit dataChanged();
    QMessageBox::information(this, "成功", QString::fromStdString(r.message));
}

void RecordTab::onReturn() {
    int row = table_->currentRow();
    if (row < 0) {
        QMessageBox::information(this, "提示", "请先在表格中选择一条未归还的记录。");
        return;
    }
    QTableWidgetItem* it = table_->item(row, 0);
    if (!it) return;
    QString rid = it->text();
    OpResult r = lib_->returnBook(rid.toStdString());
    if (!r.ok) {
        QMessageBox::warning(this, "归还失败", QString::fromStdString(r.message));
        return;
    }
    refresh();
    emit dataChanged();
    QMessageBox::information(this, "成功", QString::fromStdString(r.message));
}
