#include <iostream>
#include <vector>
#include <queue>
#include <string>
#include <algorithm>

using namespace std;

const int INF = 1e9;

// 边的结构体
struct Edge {
    int from, to;
    int cap;    // 容量 c(a)
    int flow;   // 流量 f(a)
    int id;     // 边的编号
};

// 严格按照 PPT 定义的标号结构体
struct Label {
    bool is_labeled = false;
    int pre_node = -1;       // v_i
    string sign = "";        // "^+" 或 "^-"
    int delta = 0;           // delta_{v_j}
};

int n, m;         // 点数和边数
int source, sink; // 源点 s 和汇点 t
vector<Edge> edges;
vector<vector<int>> adj; // 邻接表，存储边在 edges 数组中的索引

// Edmonds-Karp 标号算法
void edmonds_karp() {
    // 初始化所有边流量为 0
    for (auto& e : edges) e.flow = 0;
    
    int iteration = 1;
    
    while (true) {
        // 初始化标号数组，去掉除源点外的所有标号
        vector<Label> labels(n + 1);
        labels[source] = {true, -1, "", INF}; 
        
        queue<int> q;
        q.push(source);
        
        bool found_t = false;

        // Step 1. 标号过程
        while (!q.empty()) {
            int vi = q.front();
            q.pop();
            
            string vi_label_str = (vi == source) ? "(-, infinity)" : "(v_" + to_string(labels[vi].pre_node) + labels[vi].sign + ", " + to_string(labels[vi].delta) + ")";
            cout << "-> Step 1. 检查标号点 $v_" << vi << "$，其自身标号为: $" << vi_label_str << "$" << endl;

            // 检查 v_i 的所有邻点
            for (int edge_idx : adj[vi]) {
                Edge& e = edges[edge_idx];
                
                // a. 若存在 (v_i, v_j) = a 且 f(a) < c(a)
                if (e.from == vi) {
                    int vj = e.to;
                    if (!labels[vj].is_labeled && e.flow < e.cap) {
                        labels[vj].is_labeled = true;
                        labels[vj].pre_node = vi;
                        labels[vj].sign = "^+";
                        labels[vj].delta = (labels[vi].delta == INF) ? (e.cap - e.flow) : min(labels[vi].delta, e.cap - e.flow);
                        
                        string delta_vi_str = (labels[vi].delta == INF) ? "infinity" : to_string(labels[vi].delta);
                        cout << "   [正向标号] $delta_{v_" << vj << "} = min{" << delta_vi_str << ", " << e.cap << " - " << e.flow << "} = " << labels[vj].delta << "$" << endl;
                        cout << "              给 $v_" << vj << "$ 标号为: $(v_" << vi << "^+, " << labels[vj].delta << ")$" << endl;
                        
                        q.push(vj);
                    }
                } 
                // b. 若存在边 (v_j, v_i) = a 且 f(a) > 0
                else if (e.to == vi) {
                    int vj = e.from;
                    if (!labels[vj].is_labeled && e.flow > 0) {
                        labels[vj].is_labeled = true;
                        labels[vj].pre_node = vi;
                        labels[vj].sign = "^-";
                        labels[vj].delta = (labels[vi].delta == INF) ? e.flow : min(e.flow, labels[vi].delta);
                        
                        string delta_vi_str = (labels[vi].delta == INF) ? "infinity" : to_string(labels[vi].delta);
                        cout << "   [反向标号] $delta_{v_" << vj << "} = min{" << e.flow << ", " << delta_vi_str << "} = " << labels[vj].delta << "$" << endl;
                        cout << "              给 $v_" << vj << "$ 标号为: $(v_" << vi << "^-, " << labels[vj].delta << ")$" << endl;
                        
                        q.push(vj);
                    }
                }

                // Step 2. 若 t 已被标号，转 Step 3
                if (labels[sink].is_labeled) {
                    found_t = true;
                    cout << "Step 2. 汇点 $v_" << sink << "$ 已被标号，成功找到增流路径，转 Step 3。" << endl;
                    break;
                }
            }
            if (found_t) break;
        }

        // 队列为空且未标号到汇点，说明无增流路径，算法结束
        if (!found_t) {
            cout << "Step 1. 无法继续给汇点 $v_" << sink << "$ 标号。算法结束。" << endl;
            break;
        }

        // Step 3. 构造增流路并修改流量
        int delta_t = labels[sink].delta;
        cout << "Step 3. 调整量 $delta_t = " << delta_t << "$" << endl;
        
        int curr = sink;
        while (curr != source) {
            int prev = labels[curr].pre_node;
            if (labels[curr].sign == "^+") {
                for (auto& e : edges) {
                    if (e.from == prev && e.to == curr) {
                        cout << "        [前向边修改] 边 ($v_" << prev << " -> v_" << curr << "$): 流量 $f = " << e.flow << " -> " << e.flow + delta_t << "$" << endl;
                        e.flow += delta_t;
                        break;
                    }
                }
            } else if (labels[curr].sign == "^-") {
                for (auto& e : edges) {
                    if (e.from == curr && e.to == prev) {
                        cout << "        [后向边修改] 边 ($v_" << curr << " -> v_" << prev << "$): 流量 $f = " << e.flow << " -> " << e.flow - delta_t << "$" << endl;
                        e.flow -= delta_t;
                        break;
                    }
                }
            }
            curr = prev;
        }
        cout << "Step 3. 流量修改完成，去掉除 $v_" << source << "$ 外所有点的标号，返回 Step 1。\n" << endl;
        iteration++;
    }

    // 最终最大流分布整合与算式输出
    cout << "\n==================================================" << endl;
    cout << "【最终最大流分布结果】" << endl;
    cout << "--------------------------------------------------" << endl;
    
    // 输出所有边的流量分布
    for (auto& e : edges) {
        cout << "边 ($v_" << e.from << " -> v_" << e.to 
             << "$): $f = " << e.flow << " / c = " << e.cap << "$";
        if (e.flow == e.cap && e.cap > 0) cout << "  [满流]";
        cout << endl;
    }
    
    cout << "--------------------------------------------------" << endl;

    // 计算最大流（从源点流出的总量）
    int max_flow = 0;
    string formula_str = "";
    bool first = true;
    for (int edge_idx : adj[source]) {
        if (edges[edge_idx].from == source && edges[edge_idx].flow > 0) {
            int current_edge_flow = edges[edge_idx].flow;
            max_flow += current_edge_flow;
            if (!first) formula_str += " + ";
            formula_str += to_string(current_edge_flow);
            first = false;
        }
    }

    cout << "最大流总和算式: $" << formula_str << " = " << max_flow << "$" << endl;
    cout << "该网络的最大流量为: $" << max_flow << "$" << endl;
    cout << "==================================================" << endl;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int u_count, e_count;
    if (!(cin >> u_count >> e_count)) return 0;
    n = u_count; m = e_count;

    cin >> source >> sink;

    adj.resize(n + 1);

    for (int i = 0; i < m; ++i) {
        int u, v, w;
        cin >> u >> v >> w;
        edges.push_back({u, v, w, 0, i});
        adj[u].push_back(i);
        adj[v].push_back(i); 
    }

    edmonds_karp();
    return 0;
}