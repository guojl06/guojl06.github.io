#include <iostream>
#include <vector>
#include <queue>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n + 1);
    vector<int> in(n + 1, 0);

    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        in[v]++;
    }

    queue<int> q;
    for (int i = 1; i <= n; i++)
        if (in[i] == 0) q.push(i);

    vector<int> ans;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        ans.push_back(u);
        for (int v : g[u]) {
            if (--in[v] == 0) q.push(v);
        }
    }

    if (ans.size() != n) {
        cout << -1;
    } else {
        for (int i = 0; i < n; i++) {
            if (i) cout << ' ';
            cout << ans[i];
        }
    }
}