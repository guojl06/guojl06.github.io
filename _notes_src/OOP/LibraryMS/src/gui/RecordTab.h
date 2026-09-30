#ifndef LIBRARYMS_RECORDTAB_H
#define LIBRARYMS_RECORDTAB_H

#include <QWidget>
#include <vector>
#include "../core/Library.h"

class QComboBox;
class QSpinBox;
class QTableWidget;
class QLabel;
class Record;

// 借还书记录页：借书、还书、记录列表（含逾期状态着色）。
class RecordTab : public QWidget {
    Q_OBJECT
public:
    explicit RecordTab(Library* lib, QWidget* parent = nullptr);

public slots:
    void refresh();

signals:
    void dataChanged();

private slots:
    void onBorrow();
    void onReturn();

private:
    void fillTable(const std::vector<const Record*>& rows);
    void reloadCombos();

    Library* lib_;
    QComboBox* userCombo_;
    QComboBox* bookCombo_;
    QSpinBox* daysSpin_;
    QTableWidget* table_;
    QLabel* countLabel_;
};

#endif // LIBRARYMS_RECORDTAB_H
