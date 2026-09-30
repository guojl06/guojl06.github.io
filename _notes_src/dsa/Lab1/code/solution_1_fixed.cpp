// solution_1_fixed.cpp
// 由原始附件 solution_1.cpp 复制修改而来，只修正确性/运行时错误，不做性能优化。
// 改动（共 3 处，已在行内标注 FIX）：
//   FIX-1  数组维度 2000 -> 2001：本题采用 1-based 下标，最大下标为 n/m = 2000，
//          原 [2000][2000] 会越界读写（n=2000 时实测 SIGBUS 崩溃）。
//   FIX-2  sum 由“询问循环外声明”改为“循环内声明”：原代码累加器跨询问累积。
//   FIX-3  sum 类型 int -> long long，输出 %d -> %lld：
//          单次询问最大子矩阵和 2000*2000*1e5 = 4e11，远超 int 上限 2147483647。
#include <cstdio>

int matrix[2001][2001];   // FIX-1: 2000 -> 2001

int main() {
    int n, m, q;
    scanf("%d%d", &n, &m);
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            scanf("%d", &matrix[i][j]);
        }
    }
    scanf("%d", &q);
    for (int i = 1; i <= q; ++i) {          // FIX-2: sum 的声明移入循环体
        int x, y, a, b;
        scanf("%d %d %d %d", &x, &y, &a, &b);
        long long sum = 0;                  // FIX-2 + FIX-3
        for (int j = 0; j < a; ++j) {
            for (int k = 0; k < b; ++k) {
                sum += matrix[x + j][y + k];
            }
        }
        printf("%lld\n", sum);              // FIX-3
    }
    return 0;
}
