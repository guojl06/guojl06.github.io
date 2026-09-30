#ifndef LIBRARYMS_STATSTAB_H
#define LIBRARYMS_STATSTAB_H

#include <QWidget>
#include "../core/Library.h"

class ChartWidget;
class QLabel;
class QSpinBox;

// 统计分析页：最受欢迎图书、借阅最多读者、借阅量月度趋势。
class StatsTab : public QWidget {
    Q_OBJECT
public:
    explicit StatsTab(Library* lib, QWidget* parent = nullptr);

public slots:
    void refresh();

private:
    Library* lib_;
    ChartWidget* bookChart_;
    ChartWidget* userChart_;
    ChartWidget* trendChart_;
    QLabel* summaryLabel_;
    QSpinBox* topNSpin_;
    QSpinBox* monthsSpin_;
};

#endif // LIBRARYMS_STATSTAB_H
