#ifndef LIBRARYMS_SEEDDATA_H
#define LIBRARYMS_SEEDDATA_H

class Library;

// 生成一组示例数据（图书 / 读者 / 借还记录），用于首次运行或一键演示。
// 示例里有意制造"已归还 / 借阅中 / 已逾期"三种状态，方便展示统计图表。
void seedSampleData(Library& lib);

#endif // LIBRARYMS_SEEDDATA_H
