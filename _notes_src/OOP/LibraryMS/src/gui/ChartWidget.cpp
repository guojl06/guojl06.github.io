#include "ChartWidget.h"

#include <QPainter>
#include <QPainterPath>
#include <QRect>
#include <algorithm>

ChartWidget::ChartWidget(QWidget* parent) : QWidget(parent) {
    // 让背景能被样式表/擦除正常工作
    setAttribute(Qt::WA_OpaquePaintEvent, false);
}

void ChartWidget::clear() {
    labels_.clear();
    values_.clear();
    title_.clear();
    update();
}

void ChartWidget::setBarData(const QStringList& labels, const QVector<int>& values,
                             const QString& title) {
    type_ = Type::Bar;
    labels_ = labels;
    values_ = values;
    title_ = title;
    update();
}

void ChartWidget::setLineData(const QStringList& labels, const QVector<int>& values,
                              const QString& title) {
    type_ = Type::Line;
    labels_ = labels;
    values_ = values;
    title_ = title;
    update();
}

void ChartWidget::paintEvent(QPaintEvent*) {
    QPainter p(this);
    p.setRenderHint(QPainter::Antialiasing, true);

    const int W = width(), H = height();
    p.fillRect(rect(), Qt::white);

    const int marginLeft = 48, marginRight = 16, marginTop = 36, marginBottom = 46;
    const int plotW = W - marginLeft - marginRight;
    const int plotH = H - marginTop - marginBottom;
    if (plotW <= 10 || plotH <= 10) return;

    // 标题
    if (!title_.isEmpty()) {
        QFont tf = p.font();
        tf.setBold(true);
        tf.setPointSize(11);
        p.setFont(tf);
        p.setPen(Qt::black);
        p.drawText(QRect(0, 4, W, 28), Qt::AlignCenter, title_);
    }

    const int n = values_.size();
    if (n == 0) {
        p.setPen(Qt::gray);
        p.drawText(rect(), Qt::AlignCenter, "暂无数据");
        return;
    }

    int maxV = *std::max_element(values_.constBegin(), values_.constEnd());
    if (maxV <= 0) maxV = 1;
    int step = std::max(1, maxV / 5);   // y 轴刻度间隔

    // 坐标轴
    p.setPen(QPen(Qt::darkGray, 1));
    p.drawLine(marginLeft, marginTop, marginLeft, marginTop + plotH);              // y
    p.drawLine(marginLeft, marginTop + plotH, marginLeft + plotW, marginTop + plotH); // x

    QFont small = p.font();
    small.setPointSize(8);
    p.setFont(small);

    // 网格线 + y 刻度
    for (int v = 0; v <= maxV; v += step) {
        int y = marginTop + plotH - static_cast<int>(plotH * static_cast<double>(v) / maxV);
        p.setPen(QPen(QColor(225, 225, 225), 1, Qt::DashLine));
        p.drawLine(marginLeft, y, marginLeft + plotW, y);
        p.setPen(Qt::darkGray);
        p.drawText(QRect(2, y - 8, marginLeft - 6, 16),
                   Qt::AlignRight | Qt::AlignVCenter, QString::number(v));
    }

    if (type_ == Type::Bar) {
        const double unit = static_cast<double>(plotW) / n;
        const double barW = unit * 0.62;
        for (int i = 0; i < n; ++i) {
            int x = marginLeft + static_cast<int>(i * unit + unit * 0.19);
            int h = static_cast<int>(plotH * static_cast<double>(values_[i]) / maxV);
            QRect bar(x, marginTop + plotH - h, static_cast<int>(barW), h);
            QColor c = QColor::fromHsv((i * 47 + 30) % 360, 160, 205);
            p.setBrush(c);
            p.setPen(QPen(c.darker(150)));
            p.drawRect(bar);
            // 数值
            p.setPen(Qt::black);
            p.drawText(QRect(x - 8, bar.top() - 16, static_cast<int>(barW) + 16, 16),
                       Qt::AlignCenter, QString::number(values_[i]));
            // x 标签
            if (i < labels_.size()) {
                p.drawText(QRect(x - 12, marginTop + plotH + 4,
                                 static_cast<int>(barW) + 24, marginBottom - 4),
                           Qt::AlignCenter | Qt::AlignTop | Qt::TextWordWrap, labels_[i]);
            }
        }
    } else { // Line
        double denom = (n > 1) ? (n - 1) : 1;
        double gap = static_cast<double>(plotW) / denom;
        QPolygon pts;
        for (int i = 0; i < n; ++i) {
            int x = marginLeft + static_cast<int>(i * gap);
            int y = marginTop + plotH - static_cast<int>(plotH * static_cast<double>(values_[i]) / maxV);
            pts << QPoint(x, y);
        }
        // 折线
        p.setPen(QPen(QColor(45, 110, 210), 2));
        p.setBrush(Qt::NoBrush);
        p.drawPolyline(pts);
        // 数据点
        p.setBrush(QColor(45, 110, 210));
        p.setPen(QPen(Qt::white, 1));
        for (int i = 0; i < pts.size(); ++i)
            p.drawEllipse(pts[i], 5, 5);
        // 数值
        p.setPen(Qt::black);
        for (int i = 0; i < n; ++i)
            p.drawText(QRect(pts[i].x() - 15, pts[i].y() - 22, 30, 16),
                       Qt::AlignCenter, QString::number(values_[i]));
        // x 标签
        for (int i = 0; i < n && i < labels_.size(); ++i) {
            int x = marginLeft + static_cast<int>(i * gap);
            p.drawText(QRect(x - 26, marginTop + plotH + 4, 52, marginBottom - 4),
                       Qt::AlignCenter | Qt::TextWordWrap, labels_[i]);
        }
    }
}
