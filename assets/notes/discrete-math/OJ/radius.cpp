#include <iostream>
#include <algorithm>
using namespace std;

int dist[505][505];

int main() {
    int n, m;
    cin >> n >> m;
    const int INF = 1e9;

    //初始化
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            dist[i][j] = (i == j ? 0 : INF);

    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        if (u == v) continue;
        dist[u][v] = min(dist[u][v], w);
        dist[v][u] = min(dist[v][u], w);
    }

    // Floyd
    for (int k = 1; k <= n; k++)
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++)
                if (dist[i][k] != INF && dist[k][j] != INF)
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);

    int ans = 0;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++) {
            if (dist[i][j] == INF) { cout << -1; return 0; }
            ans = max(ans, dist[i][j]);
        }
    cout << ans;
}