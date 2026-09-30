#include "BookTab.h"
#include "../core/Book.h"

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
#include <QSpinBox>
#include <QDialogButtonBox>
#include <QMessageBox>
#include <QAbstractItemView>
#include <QDate>

namespace {
// 添加 / 编辑图书的对话框（本文件内部使用，无需独立头文件）
class BookDialog : public QDialog {
public:
    BookDialog(QWidget* parent, const Book* book)
        : QDialog(parent) {
        setWindowTitle(book ? "编辑图书" : "添加图书");
        setMinimumWidth(360);

        auto* form = new QFormLayout;
        titleEdit_     = new QLineEdit;
        authorEdit_    = new QLineEdit;
        publisherEdit_ = new QLineEdit;
        categoryEdit_  = new QLineEdit;
        isbnEdit_      = new QLineEdit;
        yearEdit_ = new QSpinBox;
        yearEdit_->setRange(1000, 9999);
        yearEdit_->setValue(QDate::currentDate().year());
        copiesEdit_ = new QSpinBox;
        copiesEdit_->setRange(1, 99999);
        copiesEdit_->setValue(3);

        form->addRow("书名:", titleEdit_);
        form->addRow("作者:", authorEdit_);
        form->addRow("出版社:", publisherEdit_);
        form->addRow("分类:", categoryEdit_);
        form->addRow("ISBN:", isbnEdit_);
        form->addRow("出版年份:", yearEdit_);
        form->addRow("馆藏数量:", copiesEdit_);

        auto* btns = new QDialogButtonBox(QDialogButtonBox::Ok | QDialogButtonBox::Cancel);
        connect(btns, &QDialogButtonBox::accepted, this, &QDialog::accept);
        connect(btns, &QDialogButtonBox::rejected, this, &QDialog::reject);

        auto* lay = new QVBoxLayout(this);
        lay->addLayout(form);
        lay->addWidget(btns);

        if (book) {
            titleEdit_->setText(QString::fromStdString(book->title()));
            authorEdit_->setText(QString::fromStdString(book->author()));
            publisherEdit_->setText(QString::fromStdString(book->publisher()));
            categoryEdit_->setText(QString::fromStdString(book->category()));
            isbnEdit_->setText(QString::fromStdString(book->isbn()));
            yearEdit_->setValue(book->year());
            copiesEdit_->setValue(book->totalCopies());
        }
    }

    QString title() const     { return titleEdit_->text(); }
    QString author() const    { return authorEdit_->text(); }
    QString publisher() const { return publisherEdit_->text(); }
    QString category() const  { return categoryEdit_->text(); }
    QString isbn() const      { return isbnEdit_->text(); }
    int year() const          { return yearEdit_->value(); }
    int totalCopies() const   { return copiesEdit_->value(); }

private:
    QLineEdit* titleEdit_, *authorEdit_, *publisherEdit_, *categoryEdit_, *isbnEdit_;
    QSpinBox* yearEdit_, *copiesEdit_;
};
} // namespace

BookTab::BookTab(Library* lib, QWidget* parent)
    : QWidget(parent), lib_(lib) {
    // —— 顶部工具条 ——
    auto* top = new QHBoxLayout;
    searchEdit_ = new QLineEdit;
    searchEdit_->setPlaceholderText("输入关键字进行模糊搜索…");
    fieldCombo_ = new QComboBox;
    fieldCombo_->addItems({"全部字段", "书名", "作者", "分类", "ISBN"});
    auto* searchBtn  = new QPushButton("搜索");
    auto* showAllBtn = new QPushButton("显示全部");
    auto* addBtn  = new QPushButton("添加图书");
    auto* editBtn = new QPushButton("编辑");
    auto* delBtn  = new QPushButton("删除");

    top->addWidget(new QLabel("关键字:"));
    top->addWidget(searchEdit_, 3);
    top->addWidget(fieldCombo_);
    top->addWidget(searchBtn);
    top->addWidget(showAllBtn);
    top->addSpacing(12);
    top->addWidget(addBtn);
    top->addWidget(editBtn);
    top->addWidget(delBtn);

    // —— 表格 ——
    table_ = new QTableWidget;
    table_->setColumnCount(10);
    table_->setHorizontalHeaderLabels(
        {"编号", "书名", "作者", "出版社", "分类", "ISBN", "年份", "馆藏", "可借", "已借"});
    table_->setSelectionBehavior(QAbstractItemView::SelectRows);
    table_->setEditTriggers(QAbstractItemView::NoEditTriggers);
    table_->setAlternatingRowColors(true);
    table_->horizontalHeader()->setStretchLastSection(true);
    table_->verticalHeader()->setDefaultSectionSize(26);
    table_->setColumnWidth(0, 70);
    table_->setColumnWidth(1, 220);
    table_->setColumnWidth(2, 110);

    countLabel_ = new QLabel("共 0 本");

    auto* mainLay = new QVBoxLayout(this);
    mainLay->addLayout(top);
    mainLay->addWidget(table_);
    mainLay->addWidget(countLabel_);

    connect(searchBtn, &QPushButton::clicked, this, &BookTab::onSearch);
    connect(showAllBtn, &QPushButton::clicked, this, [this] { searchEdit_->clear(); onSearch(); });
    connect(searchEdit_, &QLineEdit::returnPressed, this, &BookTab::onSearch);
    connect(addBtn, &QPushButton::clicked, this, &BookTab::onAdd);
    connect(editBtn, &QPushButton::clicked, this, &BookTab::onEdit);
    connect(delBtn, &QPushButton::clicked, this, &BookTab::onDelete);
    connect(table_, &QTableWidget::cellDoubleClicked, this, &BookTab::onEdit);

    refresh();
}

void BookTab::refresh() {
    onSearch();
}

void BookTab::onSearch() {
    std::string kw = searchEdit_->text().toStdString();
    Library::BookField f;
    switch (fieldCombo_->currentIndex()) {
        case 1:  f = Library::BookField::Title; break;
        case 2:  f = Library::BookField::Author; break;
        case 3:  f = Library::BookField::Category; break;
        case 4:  f = Library::BookField::Isbn; break;
        default: f = Library::BookField::All;
    }
    fillTable(lib_->searchBooks(kw, f));
}

void BookTab::fillTable(const std::vector<const Book*>& rows) {
    table_->setRowCount(0);
    for (const Book* b : rows) {
        int r = table_->rowCount();
        table_->insertRow(r);
        auto set = [&](int col, const QString& s) { table_->setItem(r, col, new QTableWidgetItem(s)); };
        set(0, QString::fromStdString(b->bookId()));
        set(1, QString::fromStdString(b->title()));
        set(2, QString::fromStdString(b->author()));
        set(3, QString::fromStdString(b->publisher()));
        set(4, QString::fromStdString(b->category()));
        set(5, QString::fromStdString(b->isbn()));
        set(6, QString::number(b->year()));
        set(7, QString::number(b->totalCopies()));
        set(8, QString::number(b->availableCopies()));
        set(9, QString::number(b->borrowedCount()));
        // 库存为 0 的行，"可借"列标红
        if (b->availableCopies() == 0) {
            QTableWidgetItem* it = table_->item(r, 8);
            it->setForeground(QBrush(QColor(200, 0, 0)));
        }
        // 编号居中
        table_->item(r, 0)->setTextAlignment(Qt::AlignCenter);
        table_->item(r, 6)->setTextAlignment(Qt::AlignCenter);
        for (int c = 7; c <= 9; ++c) table_->item(r, c)->setTextAlignment(Qt::AlignCenter);
    }
    countLabel_->setText(QString("共 %1 本（合计馆藏 %2 册）")
                             .arg(rows.size())
                             .arg([rows] {
                                 int t = 0;
                                 for (auto* b : rows) t += b->totalCopies();
                                 return t;
                             }()));
}

QString BookTab::currentId() const {
    int row = table_->currentRow();
    if (row < 0) return {};
    QTableWidgetItem* it = table_->item(row, 0);
    return it ? it->text() : QString();
}

void BookTab::onAdd() {
    BookDialog dlg(this, nullptr);
    if (dlg.exec() != QDialog::Accepted) return;
    OpResult r = lib_->addBook(dlg.title().toStdString(), dlg.author().toStdString(),
                               dlg.publisher().toStdString(), dlg.category().toStdString(),
                               dlg.isbn().toStdString(), dlg.year(), dlg.totalCopies());
    if (!r.ok) {
        QMessageBox::warning(this, "添加失败", QString::fromStdString(r.message));
        return;
    }
    refresh();
    emit dataChanged();
    QMessageBox::information(this, "成功",
                             QString::fromStdString(r.message) +
                                 "\n新图书编号: " + QString::fromStdString(r.id));
}

void BookTab::onEdit() {
    QString id = currentId();
    if (id.isEmpty()) {
        QMessageBox::information(this, "提示", "请先选择一行。");
        return;
    }
    Book* b = lib_->findBook(id.toStdString());
    if (!b) return;
    BookDialog dlg(this, b);
    if (dlg.exec() != QDialog::Accepted) return;
    OpResult r = lib_->updateBook(id.toStdString(), dlg.title().toStdString(),
                                  dlg.author().toStdString(), dlg.publisher().toStdString(),
                                  dlg.category().toStdString(), dlg.isbn().toStdString(),
                                  dlg.year(), dlg.totalCopies());
    if (!r.ok) {
        QMessageBox::warning(this, "更新失败", QString::fromStdString(r.message));
        return;
    }
    refresh();
    emit dataChanged();
    QMessageBox::information(this, "成功", QString::fromStdString(r.message));
}

void BookTab::onDelete() {
    QString id = currentId();
    if (id.isEmpty()) {
        QMessageBox::information(this, "提示", "请先选择一行。");
        return;
    }
    auto btn = QMessageBox::question(this, "确认删除",
                                     "确定要删除图书 " + id + " 吗？");
    if (btn != QMessageBox::Yes) return;
    OpResult r = lib_->removeBook(id.toStdString());
    if (!r.ok) {
        QMessageBox::warning(this, "删除失败", QString::fromStdString(r.message));
        return;
    }
    refresh();
    emit dataChanged();
    QMessageBox::information(this, "成功", QString::fromStdString(r.message));
}
