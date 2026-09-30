# 图书馆管理系统（C++ / Qt6）

面向对象程序设计大作业。一个带图形界面的图书馆管理系统，包含图书管理、用户管理、
借还书记录、统计分析四大模块，支持模糊查询、非法输入校验和文件持久化。

## 功能一览

| 模块 | 功能 |
|------|------|
| 图书管理 | 增删改查、按 书名/作者/分类/ISBN **模糊查询**、馆藏与可借副本统计 |
| 用户管理 | 读者增删改查、学生/教师两种类型（**可借数量不同，体现多态**）、按姓名/手机号查询 |
| 借还记录 | 借书（含借期设定）、还书、**逾期自动识别并标红**、按状态着色 |
| 统计分析 | 最受欢迎图书、借阅最多读者（**自绘柱状图**）、近 N 月借阅量趋势（**自绘折线图**）、总览数据 |
| 其它 | 非法输入统一校验（手机号/ISBN/性别/数量等）、启动自动加载、退出自动保存、一键载入示例数据 |

## 目录结构

```
LibraryMS/
├── CMakeLists.txt
├── README.md
├── src/
│   ├── main.cpp                 程序入口
│   ├── core/                    领域层（无 Qt 依赖）
│   │   ├── Date.{h,cpp}         日期类：比较 / 加减天数 / 与字符串互转
│   │   ├── Validator.{h,cpp}    输入校验工具（静态方法）
│   │   ├── Book.{h,cpp}         图书类（封装）
│   │   ├── User.{h,cpp}         用户抽象基类 + Student/Teacher（继承+多态）
│   │   ├── Record.{h,cpp}       借还记录类（动态状态）
│   │   ├── Library.{h,cpp}      系统核心：增删改查/模糊查询/借还/统计
│   │   ├── DataManager.{h,cpp}  文件持久化（读/写文本文件）
│   │   └── SeedData.{h,cpp}     示例数据生成
│   └── gui/                     界面层（基于 Qt Widgets）
│       ├── ChartWidget.{h,cpp}  自绘柱状图/折线图控件
│       ├── BookTab.{h,cpp}      图书管理页（含添加/编辑对话框）
│       ├── UserTab.{h,cpp}      用户管理页（含添加/编辑对话框）
│       ├── RecordTab.{h,cpp}    借还记录页
│       ├── StatsTab.{h,cpp}     统计分析页
│       └── MainWindow.{h,cpp}   主窗口（菜单栏 + 多标签页）
└── data/                        运行时生成：books.txt / users.txt / records.txt
```

每个类的**声明在头文件、实现在 cpp**，职责单一，分层清晰（领域层 `core` 不依赖 Qt）。

## 面向对象特性

- **封装**：`Book` / `User` / `Record` / `Date` 全部私有字段 + 公有接口；
  `Book` 的副本借还通过 `borrowOut()` / `returnBack()` 保证库存始终合法。
- **继承与多态**：`User` 为抽象基类，`Student`、`Teacher` 重写 `maxBorrowLimit()` 等
  纯虚函数；系统按用户类型决定可借数量。
- **重写（override）**：`ChartWidget` 重写 `paintEvent` 自绘图表；各用户子类 `override`。
- **STL 运用**：`std::map` 管理图书/用户，`std::vector` 管理记录，`std::unique_ptr` 管理多态用户。
- **友元**：`DataManager` 作为 `Book`/`User` 的友元，持久化时直接恢复内部状态。

## 编译与运行（macOS / Linux / Windows）

依赖：CMake ≥ 3.16、C++17 编译器、Qt6（含 Widgets 模块）。

### 安装 Qt6（macOS，使用 Homebrew）

```bash
brew install cmake qt
```

### macOS / Linux

```bash
cd LibraryMS
cmake -S . -B build
cmake --build build -j
./build/LibraryMS          # 首次运行会自动生成示例数据
```

> 若 CMake 提示找不到 Qt6，显式指定路径：
> `cmake -S . -B build -DCMAKE_PREFIX_PATH=$(brew --prefix qt)`

### Windows（MSVC）

需要 Visual Studio（含 CMake 组件）+ Qt6 的 MSVC 版，例如 `C:/Qt/6.x.x/msvc2022_64`。

```powershell
cd LibraryMS
cmake -S . -B build -DCMAKE_PREFIX_PATH=C:/Qt/6.x.x/msvc2022_64
cmake --build build --config Release
# 部署 Qt 运行依赖 dll（否则双击 exe 会报找不到 Qt6Widgets.dll）
C:/Qt/6.x.x/msvc2022_64/bin/windeployqt.exe build/Release/LibraryMS.exe
build/Release/LibraryMS.exe
```

> - `CMakeLists.txt` 已为 MSVC 自动开启 `/utf-8`，中文界面与数据不会乱码。
> - 若用 MinGW 版 Qt，请让编译器与 Qt 版本一致（都用 MinGW），构建命令同理。
> - 首次运行同样会自动生成示例数据，数据文件位于 `build/Release/data/`。

## 数据说明

程序在**可执行文件同级**的 `data/` 目录下读写三个文本文件（字段以 `|` 分隔）：

- `books.txt`：`编号|书名|作者|出版社|分类|ISBN|年份|馆藏|可借`
- `users.txt`：`编号|类型(S/T)|姓名|性别|手机号|注册日期`
- `records.txt`：`编号|读者|图书|借出日|到期日|归还日|是否归还(0/1)`

菜单「数据 → 重置为示例数据」可随时恢复演示数据。
