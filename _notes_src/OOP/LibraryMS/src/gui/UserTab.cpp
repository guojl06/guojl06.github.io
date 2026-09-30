#include "UserTab.h"
#include "../core/User.h"

#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QFormLayout>
#include <QLineEdit>
#include <QComboBox>
#include <QPushButton>
#include <QTableWidget>
#include <QHeaderView>
#include <QLabel>
#include <QDialog>
#include <QDialogButtonBox>
#include <QMessageBox>
#include <QAbstractItemView>
#include <QBrush>
#include <QColor>

namespace {
class UserDialog : public QDialog {
public:
    UserDialog(QWidget* parent, const User* user, bool lockType)
        : QDialog(parent) {
        setWindowTitle(user ? "编辑用户" : "添加用户");
        setMinimumWidth(340);

        auto* form = new QFormLayout;
        typeCombo_ = new QComboBox;
        typeCombo_->addItem("学生", static_cast<int>(User::Type::Student));
        typeCombo_->addItem("教师", static_cast<int>(User::Type::Teacher));
        nameEdit_ = new QLineEdit;
        genderCombo_ = new QComboBox;
        genderCombo_->addItems({"男", "女"});
        phoneEdit_ = new QLineEdit;
        phoneEdit_->setPlaceholderText("11 位手机号，以 1 开头");

        form->addRow("用户类型:", typeCombo_);
        form->addRow("姓名:", nameEdit_);
        form->addRow("性别:", genderCombo_);
        form->addRow("手机号:", phoneEdit_);

        auto* btns = new QDialogButtonBox(QDialogButtonBox::Ok | QDialogButtonBox::Cancel);
        connect(btns, &QDialogButtonBox::accepted, this, &QDialog::accept);
        connect(btns, &QDialogButtonBox::rejected, this, &QDialog::reject);

        auto* lay = new QVBoxLayout(this);
        lay->addLayout(form);
        lay->addWidget(btns);

        if (user) {
            typeCombo_->setCurrentIndex(
                user->userType() == User::Type::Teacher ? 1 : 0);
            nameEdit_->setText(QString::fromStdString(user->name()));
            genderCombo_->setCurrentText(QString::fromStdString(user->gender()));
            phoneEdit_->setText(QString::fromStdString(user->phone()));
        }
        typeCombo_->setEnabled(!lockType);   // 编辑时类型不可改（决定借阅上限）
    }

    User::Type type() const {
        return static_cast<User::Type>(typeCombo_->currentData().toInt());
    }
    QString name() const   { return nameEdit_->text(); }
    QString gender() const { return genderCombo_->currentText(); }
    QString phone() const  { return phoneEdit_->text(); }

private:
    QComboBox* typeCombo_, *genderCombo_;
    QLineEdit* nameEdit_, *phoneEdit_;
};
} // namespace

UserTab::UserTab(Library* lib, QWidget* parent)
    : QWidget(parent), lib_(lib) {
    auto* top = new QHBoxLayout;
    searchEdit_ = new QLineEdit;
    searchEdit_->setPlaceholderText("按姓名 / 手机号 / 编号搜索…");
    auto* searchBtn  = new QPushButton("搜索");
    auto* showAllBtn = new QPushButton("显示全部");
    auto* addBtn  = new QPushButton("添加用户");
    auto* editBtn = new QPushButton("编辑");
    auto* delBtn  = new QPushButton("删除");

    top->addWidget(new QLabel("关键字:"));
    top->addWidget(searchEdit_, 3);
    top->addWidget(searchBtn);
    top->addWidget(showAllBtn);
    top->addSpacing(12);
    top->addWidget(addBtn);
    top->addWidget(editBtn);
    top->addWidget(delBtn);

    table_ = new QTableWidget;
    table_->setColumnCount(8);
    table_->setHorizontalHeaderLabels(
        {"编号", "类型", "姓名", "性别", "手机号", "注册日期", "当前借阅", "借阅上限"});
    table_->setSelectionBehavior(QAbstractItemView::SelectRows);
    table_->setEditTriggers(QAbstractItemView::NoEditTriggers);
    table_->setAlternatingRowColors(true);
    table_->horizontalHeader()->setStretchLastSection(true);
    table_->verticalHeader()->setDefaultSectionSize(26);
    table_->setColumnWidth(0, 70);
    table_->setColumnWidth(4, 120);

    countLabel_ = new QLabel("共 0 人");

    auto* mainLay = new QVBoxLayout(this);
    mainLay->addLayout(top);
    mainLay->addWidget(table_);
    mainLay->addWidget(countLabel_);

    connect(searchBtn, &QPushButton::clicked, this, &UserTab::onSearch);
    connect(showAllBtn, &QPushButton::clicked, this, [this] { searchEdit_->clear(); onSearch(); });
    connect(searchEdit_, &QLineEdit::returnPressed, this, &UserTab::onSearch);
    connect(addBtn, &QPushButton::clicked, this, &UserTab::onAdd);
    connect(editBtn, &QPushButton::clicked, this, &UserTab::onEdit);
    connect(delBtn, &QPushButton::clicked, this, &UserTab::onDelete);
    connect(table_, &QTableWidget::cellDoubleClicked, this, &UserTab::onEdit);

    refresh();
}

void UserTab::refresh() { onSearch(); }

void UserTab::onSearch() {
    QString kw = searchEdit_->text().trimmed().toLower();
    std::vector<const User*> rows;
    for (const User* u : lib_->allUsers()) {
        if (kw.isEmpty()) { rows.push_back(u); continue; }
        QString name  = QString::fromStdString(u->name()).toLower();
        QString phone = QString::fromStdString(u->phone());
        QString id    = QString::fromStdString(u->userId()).toLower();
        if (name.contains(kw) || phone.contains(kw) || id.contains(kw))
            rows.push_back(u);
    }
    fillTable(rows);
}

void UserTab::fillTable(const std::vector<const User*>& rows) {
    table_->setRowCount(0);
    for (const User* u : rows) {
        int r = table_->rowCount();
        table_->insertRow(r);
        auto set = [&](int col, const QString& s) { table_->setItem(r, col, new QTableWidgetItem(s)); };
        set(0, QString::fromStdString(u->userId()));
        set(1, QString::fromStdString(u->typeName()));
        set(2, QString::fromStdString(u->name()));
        set(3, QString::fromStdString(u->gender()));
        set(4, QString::fromStdString(u->phone()));
        set(5, QString::fromStdString(u->registerDate().toString()));
        int cur = lib_->userCurrentBorrowed(u->userId());
        set(6, QString::number(cur));
        set(7, QString::number(u->maxBorrowLimit()));

        for (int c = 0; c <= 5; ++c) table_->item(r, c)->setTextAlignment(Qt::AlignCenter);
        for (int c = 6; c <= 7; ++c) table_->item(r, c)->setTextAlignment(Qt::AlignCenter);
        // 达到借阅上限的，"当前借阅"列标红
        if (cur >= u->maxBorrowLimit())
            table_->item(r, 6)->setForeground(QBrush(QColor(200, 0, 0)));
    }
    countLabel_->setText(QString("共 %1 人").arg(rows.size()));
}

QString UserTab::currentId() const {
    int row = table_->currentRow();
    if (row < 0) return {};
    QTableWidgetItem* it = table_->item(row, 0);
    return it ? it->text() : QString();
}

void UserTab::onAdd() {
    UserDialog dlg(this, nullptr, false);
    if (dlg.exec() != QDialog::Accepted) return;
    OpResult r = lib_->addUser(dlg.type(), dlg.name().toStdString(),
                               dlg.gender().toStdString(), dlg.phone().toStdString());
    if (!r.ok) {
        QMessageBox::warning(this, "添加失败", QString::fromStdString(r.message));
        return;
    }
    refresh();
    emit dataChanged();
    QMessageBox::information(this, "成功",
                             QString::fromStdString(r.message) +
                                 "\n新用户编号: " + QString::fromStdString(r.id));
}

void UserTab::onEdit() {
    QString id = currentId();
    if (id.isEmpty()) {
        QMessageBox::information(this, "提示", "请先选择一行。");
        return;
    }
    User* u = lib_->findUser(id.toStdString());
    if (!u) return;
    UserDialog dlg(this, u, true);
    if (dlg.exec() != QDialog::Accepted) return;
    OpResult r = lib_->updateUser(id.toStdString(), dlg.name().toStdString(),
                                  dlg.gender().toStdString(), dlg.phone().toStdString());
    if (!r.ok) {
        QMessageBox::warning(this, "更新失败", QString::fromStdString(r.message));
        return;
    }
    refresh();
    emit dataChanged();
    QMessageBox::information(this, "成功", QString::fromStdString(r.message));
}

void UserTab::onDelete() {
    QString id = currentId();
    if (id.isEmpty()) {
        QMessageBox::information(this, "提示", "请先选择一行。");
        return;
    }
    auto btn = QMessageBox::question(this, "确认删除",
                                     "确定要删除用户 " + id + " 吗？");
    if (btn != QMessageBox::Yes) return;
    OpResult r = lib_->removeUser(id.toStdString());
    if (!r.ok) {
        QMessageBox::warning(this, "删除失败", QString::fromStdString(r.message));
        return;
    }
    refresh();
    emit dataChanged();
    QMessageBox::information(this, "成功", QString::fromStdString(r.message));
}
