// 调试副本：在 solution_1.cpp 基础上加入中间量打印（仅用于调试，不覆盖原文件）
#include <cstdio>
int matrix[2000][2000];
int main() {
    int n, m, q;
    scanf("%d%d", &n, &m);
    fprintf(stderr, "[dbg] n=%d m=%d\n", n, m);
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= m; ++j)
            scanf("%d", &matrix[i][j]);
    scanf("%d", &q);
    fprintf(stderr, "[dbg] q=%d\n", q);
    int sum = 0;                      // 注意：sum 在询问循环之外
    for (int i = 1; i <= q; ++i) {
        int x, y, a, b;
        scanf("%d %d %d %d", &x, &y, &a, &b);
        fprintf(stderr, "[dbg] --- query #%d: x=%d y=%d a=%d b=%d, sum(入口)=%d\n",
                i, x, y, a, b, sum);
        int local = 0;
        for (int j = 0; j < a; ++j) {
            for (int k = 0; k < b; ++k) {
                fprintf(stderr, "[dbg]   q%d += matrix[%d][%d] = %d  (sum: %d -> %d)\n",
                        i, x + j, y + k, matrix[x + j][y + k], sum, sum + matrix[x + j][y + k]);
                sum += matrix[x + j][y + k];
                local += matrix[x + j][y + k];
            }
        }
        fprintf(stderr, "[dbg] q%d 结束: 累加器 sum=%d  本次询问真实和 local=%d  差=%d\n",
                i, sum, local, sum - local);
        printf("%d\n", sum);
    }
    return 0;
}
