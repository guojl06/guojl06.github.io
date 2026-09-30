#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <set>

using namespace std;

void solve_BFS(int n, const vector<vector<int>>& adj, int startNode) {
    cout << "\n=== BFS 结果 (集合 Ai) ===" << endl;
    vector<int> level(n + 1, -1);
    vector<set<int>> A(n + 1);
    queue<int> q;
    level[startNode] = 0;
    q.push(startNode);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (level[v] == -1) {
                level[v] = level[u] + 1;
                A[level[v]].insert(v);
                q.push(v);
            }
        }
    }
    for (int i = 1; i <= n; i++) {
        if (A[i].empty()) continue;
        cout << "A" << i << " = { ";
        for (int node : A[i]) cout << "v" << node << " ";
        cout << "}" << endl;
    }
}

void solve_DFS(int n, const vector<vector<int>>& adj, int startNode) {
    cout << "\n=== DFS 访问顺序 ===" << endl;
    vector<bool> visited(n + 1, false);
    vector<int> order;
    auto dfs = [&](auto self, int u) -> void {
        visited[u] = true;
        order.push_back(u);
        for (int v : adj[u]) if (!visited[v]) self(self, v);
    };
    dfs(dfs, startNode);
    for (int i = 0; i < (int)order.size(); i++) {
        cout << "v" << order[i] << (i == (int)order.size() - 1 ? "" : " -> ");
    }
    cout << endl;
}

int main() {
    int n, m;
    // 必须读入两个数：顶点数n 边数m
    if (!(cin >> n >> m)) return 0;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (!(cin >> u >> v)) break;
        if (u <= n && v <= n && u >= 1 && v >= 1) {
            adj[u].push_back(v);
            adj[v].push_back(u);
        }
    }

    for (int i = 1; i <= n; i++) sort(adj[i].begin(), adj[i].end());

    solve_BFS(n, adj, 1);
    solve_DFS(n, adj, 1);
    return 0;
}