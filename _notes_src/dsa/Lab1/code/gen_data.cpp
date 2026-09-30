#include <cstdio>
#include <cstdlib>
// 用法: ./gen_data A > A.in     ./gen_data B > B.in
// 两类数据规模相同: n = m = 2000, q = 100000, |v(i,j)| <= 1e5
int main(int argc, char** argv){
    const int n = 2000, m = 2000, q = 100000, V = 100000;
    const char mode = (argc > 1) ? argv[1][0] : 'A';
    srand(20261227);            // 固定种子，保证实验可复现
    printf("%d %d\n", n, m);
    for (int i = 1; i <= n; ++i){
        for (int j = 1; j <= m; ++j)
            printf("%d ", rand() % (2 * V + 1) - V);
        printf("\n");
    }
    printf("%d\n", q);
    for (int k = 1; k <= q; ++k){
        if (mode == 'A'){
            // 类 A：瘦高型大面积询问——高度恒为 2000（x=1, a=n），宽度平均约 20
            int x = 1, a = n - x + 1;
            int y = rand() % m + 1;
            int b = (m - y + 1 < 20) ? (m - y + 1) : 20;
            printf("%d %d %d %d\n", x, y, a, b);
        } else {
            // 类 B：单点询问
            int x = rand() % n + 1, y = rand() % m + 1;
            printf("%d %d %d %d\n", x, y, 1, 1);
        }
    }
    return 0;
}
