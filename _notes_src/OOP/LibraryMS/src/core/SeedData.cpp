#include "SeedData.h"
#include "Library.h"
#include "Date.h"

void seedSampleData(Library& lib) {
    lib.clearAll();

    // —— 图书 ——
    lib.addBook("C++ Primer", "Stanley Lippman", "人民邮电出版社", "计算机",
                "9787111554749", 2019, 5);
    lib.addBook("Effective C++", "Scott Meyers", "电子工业出版社", "计算机",
                "9787121262438", 2011, 3);
    lib.addBook("算法导论", "Thomas Cormen", "机械工业出版社", "计算机",
                "9787111407010", 2013, 4);
    lib.addBook("深入理解计算机系统", "Randal Bryant", "人民邮电出版社", "计算机",
                "9787111544938", 2016, 2);
    lib.addBook("红楼梦", "曹雪芹", "人民文学出版社", "文学",
                "9787020002207", 2008, 6);
    lib.addBook("活着", "余华", "作家出版社", "文学",
                "9787506365437", 2012, 4);
    lib.addBook("三体", "刘慈欣", "重庆出版社", "科幻",
                "9787229030933", 2008, 5);
    lib.addBook("人类简史", "尤瓦尔·赫拉利", "中信出版社", "历史",
                "9787508647357", 2014, 3);
    lib.addBook("明朝那些事儿", "当年明月", "北京联合出版社", "历史",
                "9787550219745", 2011, 3);
    lib.addBook("设计模式", "GoF", "机械工业出版社", "计算机",
                "9787111075752", 2000, 2);

    // —— 读者 ——
    lib.addUser(User::Type::Student, "张三", "男", "13800000001");
    lib.addUser(User::Type::Student, "李四", "女", "13800000002");
    lib.addUser(User::Type::Student, "王五", "男", "13800000003");
    lib.addUser(User::Type::Teacher, "赵教授", "男", "13900000001");
    lib.addUser(User::Type::Teacher, "钱老师", "女", "13900000002");

    // —— 借还记录 ——
    // 把"今天"暂时移到不同历史日期来借书，从而制造历史记录与逾期状态。
    Date realToday = lib.today();
    auto borrowAt = [&](int daysAgo, const std::string& uid,
                        const std::string& bid, int period) -> std::string {
        lib.setTodayForDemo(realToday.addDays(-daysAgo));
        return lib.borrowBook(uid, bid, period).id;
    };

    std::string r1 = borrowAt(120, "U0001", "B0001", 30);   // 后面会归还
    std::string r2 = borrowAt(100, "U0002", "B0003", 30);   // 后面会归还
    borrowAt(60,  "U0001", "B0005", 30);   // 到期 -30 天 -> 已逾期
    borrowAt(50,  "U0003", "B0007", 30);   // 已逾期
    borrowAt(40,  "U0004", "B0001", 30);   // 已逾期
    borrowAt(20,  "U0004", "B0002", 30);   // 借阅中（未到期）
    borrowAt(10,  "U0005", "B0005", 30);
    borrowAt(5,   "U0002", "B0009", 30);
    borrowAt(2,   "U0001", "B0007", 30);
    borrowAt(1,   "U0003", "B0003", 30);

    // 归还最早的两条（其中 r1 曾逾期）
    lib.setTodayForDemo(realToday.addDays(-55));
    lib.returnBook(r1);
    lib.setTodayForDemo(realToday.addDays(-45));
    lib.returnBook(r2);

    // 恢复为真实今天
    lib.setTodayForDemo(realToday);
}
