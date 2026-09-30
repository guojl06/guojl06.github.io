// 调试副本：在 solution_2.cpp 基础上打印 rowsum 下标与每行贡献
#include <cstdio>
int matrix[2000][2000];
int rowsum[2000][2000];
int main() {
    int n, m, q;
    scanf("%d%d", &n, &m);
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= m; ++j)
            scanf("%d", &matrix[i][j]);
    for (int i = 1; i <= n; ++i) {
        rowsum[i][0] = 0;
        for (int j = 1; j <= m; ++j)
            rowsum[i][j] = rowsum[i][j - 1] + matrix[i][j];
    }
    scanf("%d", &q);
    int sum = 0;
    for (int i = 1; i <= q; ++i) {
        int x, y, a, b;
        scanf("%d %d %d %d", &x, &y, &a, &b);
        fprintf(stderr, "[dbg] --- query #%d: x=%d y=%d a=%d b=%d (求和区间应为行 %d..%d, 列 %d..%d), sum(入口)=%d\n",
                i, x, y, a, b, x, x + a - 1, y, y + b - 1, sum);
        int local = 0;
        for (int j = 0; j < a; ++j) {
            int hi = rowsum[x + j][y + b], lo = rowsum[x + j][y];
            fprintf(stderr, "[dbg]   行%d: rowsum[%d][y+b=%d]=%d - rowsum[%d][y=%d]=%d => %d\n",
                    x + j, x + j, y + b, hi, x + j, y, lo, hi - lo);
            sum += hi - lo;
            local += hi - lo;
        }
        fprintf(stderr, "[dbg] q%d 结束: sum=%d (本询问贡献=%d)\n", i, sum, local);
        printf("%d\n", sum);
    }
    return 0;
}
