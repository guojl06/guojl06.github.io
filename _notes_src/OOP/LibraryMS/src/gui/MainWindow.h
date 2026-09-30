#ifndef LIBRARYMS_MAINWINDOW_H
#define LIBRARYMS_MAINWINDOW_H

#include <QMainWindow>
#include "../core/Library.h"
#include "../core/DataManager.h"

class QTabWidget;
class QCloseEvent;
class BookTab;
class UserTab;
class RecordTab;
class StatsTab;

// 主窗口：用 QTabWidget 组织四大功能页，提供菜单栏与全局刷新。
class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    explicit MainWindow(Library* lib, DataManager* dm, QWidget* parent = nullptr);

protected:
    void closeEvent(QCloseEvent* e) override;

private slots:
    void onSave();
    void onReloadDemo();
    void onAbout();

private:
    void refreshAll();   // 任一页修改数据后，刷新全部页

    Library* lib_;
    DataManager* dm_;
    QTabWidget* tabs_;
    BookTab* bookTab_;
    UserTab* userTab_;
    RecordTab* recordTab_;
    StatsTab* statsTab_;
};

#endif // LIBRARYMS_MAINWINDOW_H
