#ifndef LIBRARYMS_DATAMANAGER_H
#define LIBRARYMS_DATAMANAGER_H

#include <string>
#include "Library.h"

// 文件持久化：把 Library 的数据保存到 dataDir 下的文本文件，
// 并在启动时读回。采用 "字段以 | 分隔" 的简单可读格式。
// 体现「单一职责」：Library 只管业务，DataManager 只管读写。
class DataManager {
public:
    explicit DataManager(const std::string& dataDir);

    bool save(const Library& lib) const;     // 返回是否全部写入成功
    bool load(Library& lib) const;           // 无数据文件时返回 false
    bool hasData() const;

private:
    std::string dataDir_;
};

#endif // LIBRARYMS_DATAMANAGER_H
