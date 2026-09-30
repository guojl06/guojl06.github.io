#include <QApplication>
#include <QCoreApplication>
#include <QDir>

#include "core/Library.h"
#include "core/DataManager.h"
#include "core/SeedData.h"
#include "gui/MainWindow.h"

int main(int argc, char* argv[]) {
    QApplication app(argc, argv);
    app.setApplicationName("图书馆管理系统");
    app.setOrganizationName("OOPCourse");

    // 数据存放在可执行文件同级的 data 目录，便于查看 books.txt 等。
    QString dataDir = QCoreApplication::applicationDirPath() + "/data";
    QDir().mkpath(dataDir);

    Library lib;
    DataManager dm(dataDir.toStdString());

    // 首次运行（无数据文件）则生成示例数据并保存。
    if (!dm.load(lib)) {
        seedSampleData(lib);
        dm.save(lib);
    }

    MainWindow w(&lib, &dm);
    w.setWindowTitle("图书馆管理系统");
    w.resize(1120, 740);
    w.show();
    return app.exec();
}
