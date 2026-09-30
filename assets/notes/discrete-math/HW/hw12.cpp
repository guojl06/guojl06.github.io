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

// 打印当前网络中所有边的流量状态
void print_current_flow() {
    cout << "\n[当前网络流量状态 $f$]:" << endl;
    cout << "-----------------------------------" << endl;
    for (const auto& e : edges) {
        cout << "边 ($v_" << e.from << " -> v_" << e.to << "$) | 容量 $c = " 
             << e.cap << "$ | 当前流量 $f = " << e.flow << "$" << endl;
    }
    cout << "-----------------------------------\n" << endl;
}

// Edmonds-Karp 标号算法
void edmonds_karp() {
    // Step 0. 令 f 是任意一个流 (例如 f = 0)
    for (auto& e : edges) e.flow = 0;
    
    int iteration = 1;
    
    while (true) {
        cout << "=================== 【第 " << iteration++ << " 轮迭代】 ===================" << endl;
        print_current_flow();

        // Step 0. 给 s 一个永久标号 (-, infinity)
        vector<Label> labels(n + 1);
        labels[source] = {true, -1, "", INF}; 
        
        // 队列用于维护“按先标号先检查的顺序”
        queue<int> q;
        q.push(source);
        
        cout << "Step 0. 初始化源点 $v_" << source << "$ 的永久标号为: $(-, infinity)$" << endl;
        
        bool found_t = false;

        // Step 1. 标号过程
        while (!q.empty()) {
            // 选择标号最早但尚未检查的点 v_i
            int vi = q.front();
            q.pop();
            
            // 格式化输出 v_i 自身的标号
            string vi_label_str;
            if (vi == source) {
                vi_label_str = "(-, infinity)";
            } else {
                vi_label_str = "(v_" + to_string(labels[vi].pre_node) + labels[vi].sign + ", " + to_string(labels[vi].delta) + ")";
            }
            
            cout << "\n-> Step 1. 检查标号点 $v_" << vi << "$，其自身标号为: $" << vi_label_str << "$" << endl;

            // 检查 v_i 的所有邻点
            for (int edge_idx : adj[vi]) {
                Edge& e = edges[edge_idx];
                
                // a. 若存在 (v_i, v_j) = a 且 f(a) < c(a)
                if (e.from == vi) {
                    int vj = e.to;
                    if (!labels[vj].is_labeled && e.flow < e.cap) {
                        // v_j 标号 (v_i^+, delta_{v_j})
                        labels[vj].is_labeled = true;
                        labels[vj].pre_node = vi;
                        labels[vj].sign = "^+";
                        
                        // 计算 delta
                        if (labels[vi].delta == INF) {
                            labels[vj].delta = e.cap - e.flow;
                        } else {
                            labels[vj].delta = min(labels[vi].delta, e.cap - e.flow);
                        }
                        
                        string delta_vi_str = (labels[vi].delta == INF) ? "infinity" : to_string(labels[vi].delta);
                        
                        cout << "   [正向标号] 发现未标号邻点 $v_" << vj << "$ (存在正向边，且 $f < c$)" << endl;
                        cout << "              $delta_{v_" << vj << "} = min lr(lbrace delta_{v_" << vi << "}, c(a) - f(a) rbrace) = min lr(lbrace " << delta_vi_str << ", " << e.cap << " - " << e.flow << " rbrace) = " << labels[vj].delta << "$" << endl;
                        cout << "              给 $v_" << vj << "$ 标号为: $(v_" << vi << "^+, " << labels[vj].delta << ")$" << endl;
                        
                        q.push(vj);
                    }
                } 
                // b. 若存在边 (v_j, v_i) = a 且 f(a) > 0
                else if (e.to == vi) {
                    int vj = e.from;
                    if (!labels[vj].is_labeled && e.flow > 0) {
                        // v_j 标号 (v_i^-, delta_{v_j})
                        labels[vj].is_labeled = true;
                        labels[vj].pre_node = vi;
                        labels[vj].sign = "^-";
                        
                        // 计算 delta
                        if (labels[vi].delta == INF) {
                            labels[vj].delta = e.flow;
                        } else {
                            labels[vj].delta = min(e.flow, labels[vi].delta);
                        }
                        
                        string delta_vi_str = (labels[vi].delta == INF) ? "infinity" : to_string(labels[vi].delta);
                        
                        cout << "   [反向标号] 发现未标号邻点 $v_" << vj << "$ (存在反向边，且 $f > 0$)" << endl;
                        cout << "              $delta_{v_" << vj << "} = min lr(lbrace f(a), delta_{v_" << vi << "} rbrace) = min lr(lbrace " << e.flow << ", " << delta_vi_str << " rbrace) = " << labels[vj].delta << "$" << endl;
                        cout << "              给 $v_" << vj << "$ 标号为: $(v_" << vi << "^-, " << labels[vj].delta << ")$" << endl;
                        
                        q.push(vj);
                    }
                }

                // Step 2. 若 t 已被标号，转 Step 3
                if (labels[sink].is_labeled) {
                    found_t = true;
                    cout << "\nStep 2. 汇点 $v_" << sink << "$ 已被标号！成功找到一条增流路径。立刻中断标号过程，转 Step 3。" << endl;
                    break;
                }
            }
            if (found_t) break;
        }

        // Step 1 结束条件：若所有的点都已检查，说明找不到增流路径，结束
        if (!found_t) {
            cout << "\nStep 1. 队列为空，所有已标号点已检查完毕，无法给汇点 $v_" << sink << "$ 标号。" << endl;
            cout << "====== 算法结束：未找到新的增流路径。已达到最大流！ ======" << endl;
            break;
        }

        // Step 3. 构造增流路并修改流量
        int delta_t = labels[sink].delta;
        cout << "\nStep 3. 由点 $v_" << sink << "$ 开始，使用标号的第一个元素反向构造增流路 $p$" << endl;
        cout << "        当前增流路调整量 $delta_t = " << delta_t << "$" << endl;
        
        int curr = sink;
        while (curr != source) {
            int prev = labels[curr].pre_node;
            if (labels[curr].sign == "^+") {
                // 若是前向边：f'(a) = f(a) + delta_t
                for (auto& e : edges) {
                    if (e.from == prev && e.to == curr) {
                        cout << "        [前向边修改] 边 ($v_" << prev << " -> v_" << curr << "$): 流量 $f = " << e.flow << " -> " << e.flow + delta_t << "$" << endl;
                        e.flow += delta_t;
                        break;
                    }
                }
            } else if (labels[curr].sign == "^-") {
                // 若是后向边：f'(a) = f(a) - delta_t
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
        cout << "Step 3. 已用 $f'$ 代替 $f$，去掉除 $v_" << source << "$ 外的所有点的 $f$ 标号。返回 Step 1。" << endl << endl;
    }

    // 计算最终最大流
    int max_flow = 0;
    for (int edge_idx : adj[source]) {
        if (edges[edge_idx].from == source) {
            max_flow += edges[edge_idx].flow;
        }
    }
    cout << "\n==================================================" << endl;
    cout << " 最终计算完成！该网络的最大流量为: $" << max_flow << "$" << endl;
    cout << "==================================================" << endl;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cout << "请输入点的数量 (N) 和边的数量 (M): ";
    if (!(cin >> n >> m)) return 0;

    cout << "请输入源点 (s) 和汇点 (t) 的编号: ";
    cin >> source >> sink;

    adj.resize(n + 1);

    cout << "请输入每条边的信息 (起点 终点 容量):" << endl;
    for (int i = 0; i < m; ++i) {
        int u, v, w;
        cin >> u >> v >> w;
        edges.push_back({u, v, w, 0, i});
        adj[u].push_back(i);
        adj[v].push_back(i); 
    }

    // 运行算法
    edmonds_karp();

    return 0;
}