#include <iostream>
#include <vector>
#include <queue>
using namespace std;

const int N = 1005, INF = 1e9;
int n, m;
vector<pair<int,int>> g[N];
vector<int> eu, ev, ew;  // 存所有边

void dij(int s, int d[]) {
    fill(d + 1, d + n + 1, INF);
    d[s] = 0;
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [dis, u] = pq.top(); pq.pop();
        if (dis != d[u]) continue;
        for (auto [v, w] : g[u]) {
            if (d[v] > d[u] + w) {
                d[v] = d[u] + w;
                pq.push({d[v], v});
            }
        }
    }
}

int main() {
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v, w; cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
        eu.push_back(u); ev.push_back(v); ew.push_back(w);
    }

    int d1[N], dn[N];
    dij(1, d1);
    dij(n, dn);

    if (d1[n] == INF) { cout << -1; return 0; }

    int ans = d1[n];
    for (int i = 0; i < m; i++) {
        int u = eu[i], v = ev[i];
        if (d1[u] != INF && dn[v] != INF) ans = min(ans, d1[u] + dn[v]);
        if (d1[v] != INF && dn[u] != INF) ans = min(ans, d1[v] + dn[u]);
    }

    cout << ans;
}