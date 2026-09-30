#ifndef LIBRARYMS_CHARTWIDGET_H
#define LIBRARYMS_CHARTWIDGET_H

#include <QWidget>
#include <QString>
#include <QVector>
#include <QStringList>

// 用 QPainter 自绘的简易图表控件：支持柱状图与折线图。
// 继承 QWidget 并重写 paintEvent —— 体现「多态/重写」。
// 这样统计页无需依赖 Qt Charts 模块。
class ChartWidget : public QWidget {
    Q_OBJECT
public:
    enum class Type { Bar, Line };

    explicit ChartWidget(QWidget* parent = nullptr);

    void setBarData(const QStringList& labels, const QVector<int>& values,
                    const QString& title = QString());
    void setLineData(const QStringList& labels, const QVector<int>& values,
                     const QString& title = QString());
    void clear();

    QSize minimumSizeHint() const override { return QSize(340, 220); }
    QSize sizeHint() const override { return QSize(420, 260); }

protected:
    void paintEvent(QPaintEvent*) override;

private:
    Type type_ = Type::Bar;
    QStringList labels_;
    QVector<int> values_;
    QString title_;
};

#endif // LIBRARYMS_CHARTWIDGET_H
