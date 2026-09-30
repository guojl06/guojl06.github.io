// solution_2_fixed.cpp
// 由原始附件 solution_2.cpp 复制修改而来，只修正确性/运行时错误，不做性能优化。
// 改动（共 4 处，已在行内标注 FIX）：
//   FIX-1  matrix / rowsum 维度 2000 -> 2001：1-based 下标最大为 n/m = 2000，
//          原数组越界（rowsum 还会被查询读到 m+1 列）。
//   FIX-2  行内前缀和窗口下标修正：
//          正确应为 rowsum[r][y+b-1] - rowsum[r][y-1]（列区间 [y, y+b-1]），
//          原代码写成 rowsum[r][y+b] - rowsum[r][y]，整个窗口右移了一列。
//   FIX-3  sum 由“询问循环外声明”改为“循环内声明”：原代码累加器跨询问累积。
//   FIX-4  sum 类型 int -> long long，输出 %d -> %lld：单次询问最大和 4e11。
#include <cstdio>

int matrix[2001][2001];   // FIX-1: 2000 -> 2001
int rowsum[2001][2001];   // FIX-1: 2000 -> 2001

int main() {
    int n, m, q;
    scanf("%d%d", &n, &m);
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            scanf("%d", &matrix[i][j]);
        }
    }
    for (int i = 1; i <= n; ++i) {
        rowsum[i][0] = 0;
        for (int j = 1; j <= m; ++j) {
            rowsum[i][j] = rowsum[i][j - 1] + matrix[i][j];
        }
    }
    scanf("%d", &q);
    for (int i = 1; i <= q; ++i) {          // FIX-3: sum 的声明移入循环体
        int x, y, a, b;
        scanf("%d %d %d %d", &x, &y, &a, &b);
        long long sum = 0;                  // FIX-3 + FIX-4
        for (int j = 0; j < a; ++j) {
            sum += rowsum[x + j][y + b - 1] - rowsum[x + j][y - 1];   // FIX-2
        }
        printf("%lld\n", sum);              // FIX-4
    }
    return 0;
}
