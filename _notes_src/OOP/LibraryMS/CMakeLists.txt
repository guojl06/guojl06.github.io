cmake_minimum_required(VERSION 3.16)
project(LibraryMS LANGUAGES CXX)

# —— C++ 标准 ——
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# —— Qt 元对象/资源自动处理 ——
set(CMAKE_AUTOMOC ON)

# —— 可执行文件输出到 build 根目录（data 目录随之在 build/data）——
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

# —— 查找 Qt6 Widgets ——
find_package(Qt6 REQUIRED COMPONENTS Widgets)

add_executable(LibraryMS
    src/main.cpp

    src/core/Date.cpp
    src/core/Validator.cpp
    src/core/Book.cpp
    src/core/User.cpp
    src/core/Record.cpp
    src/core/Library.cpp
    src/core/DataManager.cpp
    src/core/SeedData.cpp

    src/gui/ChartWidget.cpp
    src/gui/BookTab.cpp
    src/gui/UserTab.cpp
    src/gui/RecordTab.cpp
    src/gui/StatsTab.cpp
    src/gui/MainWindow.cpp
)

target_include_directories(LibraryMS PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)
target_link_libraries(LibraryMS PRIVATE Qt6::Widgets)
target_compile_options(LibraryMS PRIVATE
    $<$<CXX_COMPILER_ID:GNU,Clang,AppleClang>:-Wall -Wextra>
    # MSVC 默认不按 UTF-8 解释源码，会导致中文字面量乱码 / C4819 警告，必须显式开启。
    $<$<CXX_COMPILER_ID:MSVC>:/utf-8>
)

# Windows：隐藏控制台黑窗口
if(WIN32)
    set_target_properties(LibraryMS PROPERTIES WIN32_EXECUTABLE TRUE)
endif()
