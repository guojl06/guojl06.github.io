#include "MainWindow.h"
#include "BookTab.h"
#include "UserTab.h"
#include "RecordTab.h"
#include "StatsTab.h"
#include "../core/SeedData.h"

#include <QTabWidget>
#include <QMenuBar>
#include <QMenu>
#include <QAction>
#include <QMessageBox>
#include <QCloseEvent>
#include <QStatusBar>
#include <QKeySequence>

MainWindow::MainWindow(Library* lib, DataManager* dm, QWidget* parent)
    : QMainWindow(parent), lib_(lib), dm_(dm) {
    // —— 各功能页 ——
    tabs_ = new QTabWidget;
    bookTab_   = new BookTab(lib_);
    userTab_   = new UserTab(lib_);
    recordTab_ = new RecordTab(lib_);
    statsTab_  = new StatsTab(lib_);
    tabs_->addTab(bookTab_,   "图书管理");
    tabs_->addTab(userTab_,   "用户管理");
    tabs_->addTab(recordTab_, "借还记录");
    tabs_->addTab(statsTab_,  "统计分析");
    setCentralWidget(tabs_);

    // 任一页数据变化 -> 刷新全部（保证各页数据一致）
    connect(bookTab_,   &BookTab::dataChanged,   this, [this] { refreshAll(); });
    connect(userTab_,   &UserTab::dataChanged,   this, [this] { refreshAll(); });
    connect(recordTab_, &RecordTab::dataChanged, this, [this] { refreshAll(); });

    // —— 菜单栏 ——
    QMenu* fileMenu = menuBar()->addMenu("文件(&F)");
    QAction* saveAct = fileMenu->addAction("保存(&S)");
    saveAct->setShortcut(QKeySequence::Save);
    connect(saveAct, &QAction::triggered, this, &MainWindow::onSave);
    QAction* quitAct = fileMenu->addAction("退出(&X)");
    connect(quitAct, &QAction::triggered, this, &QWidget::close);

    QMenu* dataMenu = menuBar()->addMenu("数据(&D)");
    QAction* reloadAct = dataMenu->addAction("重置为示例数据...");
    connect(reloadAct, &QAction::triggered, this, &MainWindow::onReloadDemo);

    QMenu* helpMenu = menuBar()->addMenu("帮助(&H)");
    QAction* aboutAct = helpMenu->addAction("关于(&A)...");
    connect(aboutAct, &QAction::triggered, this, &MainWindow::onAbout);

    statusBar()->showMessage("提示：数据在程序同目录的 data 文件夹下。修改后可按 Ctrl+S 保存。");
}

void MainWindow::refreshAll() {
    bookTab_->refresh();
    userTab_->refresh();
    recordTab_->refresh();
    statsTab_->refresh();
}

void MainWindow::onSave() {
    if (dm_->save(*lib_))
        statusBar()->showMessage("数据已保存。", 3000);
    else
        QMessageBox::warning(this, "保存失败", "无法写入数据文件，请检查 data 目录权限。");
}

void MainWindow::onReloadDemo() {
    auto btn = QMessageBox::question(
        this, "重置数据", "将清空当前所有数据并载入示例数据，确定吗？");
    if (btn != QMessageBox::Yes) return;
    seedSampleData(*lib_);
    dm_->save(*lib_);
    refreshAll();
    QMessageBox::information(this, "完成", "已载入示例数据。");
}

void MainWindow::onAbout() {
    QMessageBox::about(this, "关于 - 图书馆管理系统",
        "<h3>图书馆管理系统</h3>"
        "<p>面向对象程序设计 大作业</p>"
        "<p>功能：图书 / 用户 / 借还管理，模糊查询，统计分析（自绘图表），"
        "非法输入处理，文件持久化。</p>"
        "<p>技术：C++17 + Qt6，类的封装 / 继承 / 多态，头文件与实现分离。</p>");
}

void MainWindow::closeEvent(QCloseEvent* e) {
    if (dm_) dm_->save(*lib_);   // 退出时自动保存
    e->accept();
}
