#include "StatsTab.h"
#include "ChartWidget.h"
#include "../core/Record.h"

#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QLabel>
#include <QSpinBox>
#include <QPushButton>
#include <QScrollArea>

namespace {
// 把过长的标签截短，避免柱状图横轴标签重叠
QString shortLabel(const std::string& s, int max = 6) {
    QString q = QString::fromStdString(s);
    return q.size() > max ? q.left(max) + "…" : q;
}
} // namespace

StatsTab::StatsTab(Library* lib, QWidget* parent)
    : QWidget(parent), lib_(lib) {
    // —— 控制栏 ——
    auto* ctrl = new QHBoxLayout;
    ctrl->addWidget(new QLabel("排行 Top:"));
    topNSpin_ = new QSpinBox;
    topNSpin_->setRange(3, 20);
    topNSpin_->setValue(10);
    ctrl->addWidget(topNSpin_);
    ctrl->addSpacing(12);
    ctrl->addWidget(new QLabel("趋势月数:"));
    monthsSpin_ = new QSpinBox;
    monthsSpin_->setRange(3, 24);
    monthsSpin_->setValue(6);
    ctrl->addWidget(monthsSpin_);
    auto* calcBtn = new QPushButton("重新统计");
    ctrl->addWidget(calcBtn);
    ctrl->addStretch();

    summaryLabel_ = new QLabel;
    summaryLabel_->setStyleSheet(
        "font-size:13px; padding:8px; background:#f6f6f6; border:1px solid #ddd; border-radius:4px;");

    bookChart_  = new ChartWidget;
    userChart_  = new ChartWidget;
    trendChart_ = new ChartWidget;
    bookChart_->setMinimumHeight(280);
    userChart_->setMinimumHeight(280);
    trendChart_->setMinimumHeight(280);

    auto* grid = new QGridLayout;
    grid->addWidget(bookChart_, 0, 0);
    grid->addWidget(userChart_, 0, 1);
    grid->addWidget(trendChart_, 1, 0, 1, 2);
    grid->setColumnStretch(0, 1);
    grid->setColumnStretch(1, 1);

    // 内容放进可滚动区域，避免窗口太矮时图表被压缩
    auto* content = new QWidget;
    auto* contentLay = new QVBoxLayout(content);
    contentLay->addWidget(summaryLabel_);
    contentLay->addLayout(grid);
    contentLay->addStretch();
    auto* scroll = new QScrollArea;
    scroll->setWidgetResizable(true);
    scroll->setWidget(content);

    auto* mainLay = new QVBoxLayout(this);
    mainLay->addLayout(ctrl);
    mainLay->addWidget(scroll);

    connect(calcBtn, &QPushButton::clicked, this, &StatsTab::refresh);
    connect(topNSpin_, static_cast<void(QSpinBox::*)(int)>(&QSpinBox::valueChanged),
            this, &StatsTab::refresh);
    connect(monthsSpin_, static_cast<void(QSpinBox::*)(int)>(&QSpinBox::valueChanged),
            this, &StatsTab::refresh);

    refresh();
}

void StatsTab::refresh() {
    int topN = topNSpin_->value();
    int months = monthsSpin_->value();

    // —— 概览 ——
    int nb = static_cast<int>(lib_->allBooks().size());
    int nu = static_cast<int>(lib_->allUsers().size());
    int nr = static_cast<int>(lib_->allRecords().size());
    int totalCopies = 0;
    for (const Book* b : lib_->allBooks()) totalCopies += b->totalCopies();
    Date today = lib_->today();
    int borrowed = 0, overdue = 0;
    for (const Record* r : lib_->allRecords()) {
        if (r->isReturned()) continue;
        ++borrowed;
        if (r->status(today) == Record::Status::Overdue) ++overdue;
    }
    summaryLabel_->setText(
        QString("图书：%1 种 / %2 册    用户：%3 人    借阅记录：%4 条    "
                "当前借阅中：%5    已逾期：%6")
            .arg(nb).arg(totalCopies).arg(nu).arg(nr).arg(borrowed).arg(overdue));

    // —— 最受欢迎图书 ——
    auto books = lib_->mostPopularBooks(topN);
    QStringList bLabels;
    QVector<int> bValues;
    for (const auto& s : books) {
        bLabels << shortLabel(s.title);
        bValues << s.count;
    }
    bookChart_->setBarData(bLabels, bValues,
                           QString("最受欢迎图书 Top %1（按历史借阅次数）").arg(books.size()));

    // —— 借阅最多读者 ——
    auto users = lib_->topBorrowers(topN);
    QStringList uLabels;
    QVector<int> uValues;
    for (const auto& s : users) {
        uLabels << shortLabel(s.name);
        uValues << s.count;
    }
    userChart_->setBarData(uLabels, uValues,
                           QString("借阅最多读者 Top %1").arg(users.size()));

    // —— 月度借阅趋势 ——
    auto trend = lib_->borrowTrendByMonth(months);
    QStringList mLabels;
    QVector<int> mValues;
    for (const auto& m : trend) {
        mLabels << QString::fromStdString(m.month);
        mValues << m.count;
    }
    trendChart_->setLineData(mLabels, mValues,
                             QString("近 %1 个月借阅量趋势").arg(trend.size()));
}
