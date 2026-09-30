# Lab1 例题（二维子矩阵求和）调试报告

> 任务：对 `DSA/Lab1/code/solution_1.cpp`、`solution_2.cpp` 做**静态检查 → 黑盒测试 → 输出调试 → 调试器 → 对拍 → 归纳 → 修复 → 验证**的全流程留痕。
> 原始附件（题面、两份 solution、battle/rand/check）**全程未改动**，md5 见 §9。

---

## 0. 环境、材料与方法总览

| 项 | 值 |
|---|---|
| 机器 | macOS Darwin 25.6.0，arm64（Apple Silicon） |
| 编译器 | `/usr/bin/g++` → `Apple clang version 21.0.0 (clang-2100.3.34.2)` |
| 调试器 | lldb（本机无 gdb） |
| shell | zsh / bash（Bash 兼容脚本）；本机无 `timeout`，限时统一用 `cmd & PID=$!; …; kill` |
| 工作目录 | `/Volumes/PortableSSD/Documents/mynotebook` |
| 调试产物目录 | `DSA/Lab1/code/debug/`（原附件目录只读使用） |

测试点规模（实测首行）：

| 测试点 | n | m | q | 备注 |
|---|---|---|---|---|
| `1.in` | 4 | 4 | 4 | 手写小样例（4×4 仍落在题面 `1≤n,m≤2000` 之内） |
| `2.in` | 282 | 279 | 4680 | 元素含**负数** |
| `3.in` | 1950 | 1835 | 19488 | 23 MB；元素含负数；Σ(a·b)=4 276 008 453 |

> 环境备注：该卷为 exFAT，**不支持硬链接**，`write` 类工具创建新文件报 `ENOTSUP: operation not supported on socket`，因此本次所有新文件（调试副本、修复版、本报告）均用 shell 重定向写入。

---

## 1. 静态检查：通读代码后的怀疑清单

### solution_1.cpp（朴素实现，O(n·m + q·a·b)）

| 编号 | 行号 | 可疑点 | 预期后果 |
|---|---|---|---|
| S1-A | 3 | `int matrix[2000][2000]`，但第 8–10、20 行用 **1-based** 下标 `i∈[1,n]`、`j∈[1,m]`，而题面 `n,m ≤ 2000` | 访问 `matrix[2000][*]` / `matrix[*][2000]` 越界 → UB，可能 SIGBUS/SIGSEGV，也可能静默写坏相邻内存 |
| S1-B | 14 | `int sum = 0;` 写在询问 `for (i=1..q)` **之外** | 累加器跨询问累积，第 1 个询问之后答案全错 |
| S1-C | 14 / 20 / 23 | `sum` 是 `int`，输出用 `%d` | 单次询问最大和 `2000·2000·10^5 = 4×10^11` ≫ `2^31−1 = 2147483647` → 有符号溢出 |

### solution_2.cpp（行内前缀和，O(n·m + q·a)）

| 编号 | 行号 | 可疑点 | 预期后果 |
|---|---|---|---|
| S2-A | 3, 4, 15, 17 | `matrix`/`rowsum` 都是 `[2000][2000]`，同 S1-A 的 1-based 越界问题；且第 26 行会读 `rowsum[r][y+b]`，当查询贴着右边界（`y+b−1 = m`）时下标达到 `m+1`，`m=2000` 时为 2001 | 越界读 → 读到别的行/别的数组，答案错乱 |
| S2-B | 21 | `int sum = 0;` 在询问循环之外 | 同 S1-B |
| S2-C | 21 / 26 / 28 | `int sum` + `%d` | 同 S1-C |
| S2-D | 26 | `rowsum[x+j][y+b] - rowsum[x+j][y]`。列区间应是 `[y, y+b−1]`，正确写法为 `rowsum[..][y+b−1] - rowsum[..][y−1]`；现在两端都 +1，**窗口整体右移一列** | 除极特殊数据外几乎所有询问答案错误 |

> 说明：S1-A / S2-A、S1-B / S2-B、S1-C / S2-C 是**两份代码共有的同类缺陷**，S2-D 是 solution_2 独有的语义错误。下文按 4 个 BUG 分节（A/B/C 两份共有，D 仅 s2）。

### 附：题面数据范围容量核算（任务第 6 点）

```
n = m = 2000, |v| = 1e5
单次询问最大 2D 区域和        = 2000·2000·1e5 = 400 000 000 000 = 4e11
                             = 2^31 × 186.265     → int 只能装下 0.54% 的规模
q = 1e5 次询问若累加器不复位   = 4e11 × 1e5 = 4e16
                             = 2^63 × 0.00434     → long long 装得下（还差 200 倍余量）
int       上限 = 2 147 483 647      → 单次询问即可溢出（未取绝对值也算）
long long 上限 = 9 223 372 036 854 775 807 → 4e16 安全
单行前缀和 rowsum 最大 = m·|v| = 2000·1e5 = 2e8 < 2^31−1 ≈ 2.147e9 → rowsum 用 int 是**安全**的
```

结论：**`rowsum` 保持 `int` 正确**；**`sum` 必须是 `long long`**（`int` 在 n·m ≥ 21475、v=1e5 时就溢出，本例题面下必然溢出）。

---

## 2. BUG A —— 数组维度 2000 不足，满规模输入下 SIGBUS 崩溃（两份共有）

### 现象
- 官方 3 个测试点（n,m ≤ 1950）**不崩**，只是答案错 —— 越界刚好落在"还能写"的内存里，属于**运气**。
- 自造 2000×2000 满规模测试点后，`solution_1_orig` **直接崩溃**，退出码 138（SIGBUS）。

### 发现方法
1. **静态**：`int matrix[2000][2000]` + 1-based 下标 + `n,m ≤ 2000` ⇒ 最大下标 2000 越界（§1 S1-A/S2-A）。
2. **黑盒**（自造边界测试点）确认崩溃。
3. **ASan/UBSan** 确认越界类型与位置。
4. **lldb** 抓崩溃现场，崩溃地址与 `&matrix[2000][1792]` 精确吻合。

### 最小复现
`code/debug/big/max2000.in`：`n=m=2000`，全部元素 `100000`，`q=1`，询问 `1 1 2000 2000`（期望 `400000000000`）。

### 关键命令与输出

```console
$ g++ -O2 -std=c++17 -o s1_orig solution_1.cpp     # 无任何警告
$ ./s1_orig < big/max2000.in
Bus error: 10            # exit=138 (SIGBUS)
# stdout 为空，一行都没输出 —— 在【读入矩阵】阶段就崩了
```

```console
$ g++ -O0 -g -fsanitize=address,undefined -std=c++17 -o s1_asan solution_1.cpp
$ ./s1_asan < big/max2000.in
==13758==ERROR: AddressSanitizer: global-buffer-overflow on address 0x0001036ee780
WRITE of size 4 at 0x0001036ee780 thread T0
    #0 ... in scanf_common(...)
    #1 ... in scanf+0x68
    #2 0x0001027a4ca8 in main solution_1.cpp:10        <-- scanf("%d", &matrix[i][j])
    #3 ... in start+0x1b4c (dyld)
Abort trap: 6            # exit=134

# solution_2 同址同型：
==13764==ERROR: AddressSanitizer: global-buffer-overflow ...
    #2 0x0001022c0cb4 in main solution_2.cpp:11        <-- scanf("%d", &matrix[i][j])
```

```console
$ g++ -O0 -g -fsanitize=undefined -std=c++17 -o s2_ubsan2 solution_2.cpp
$ ./s2_ubsan2 < big/max2000.in
solution_2.cpp:11:26: runtime error: index 2000 out of bounds for type 'int[2000][2000]'
solution_2.cpp:17:47: runtime error: index 2000 out of bounds for type 'int[2000]'   <-- rowsum[i][j] 写
solution_2.cpp:17:13: runtime error: index 2000 out of bounds for type 'int[2000]'
solution_2.cpp:15:9:  runtime error: index 2000 out of bounds for type 'int[2000][2000]'
solution_2.cpp:...  : runtime error: index 2001 out of bounds for type 'int[2000]'  <-- 查询读 rowsum[r][m+1]
```

**lldb 崩溃现场**（对 `-g -O0` 版本，输入 `big/max2000.in`）：

```
(lldb) process launch -i .../big/max2000.in
Process 14083 stopped
* thread #1, stop reason = EXC_BAD_ACCESS (code=2, address=0x100f4c000)
    frame #0: 0x18c1bff48 libsystem_c.dylib`__svfscanf_l + 5428
->  0x18c1bff48 <+5428>: str    w26, [x27]          <-- 写内存时炸
(lldb) bt
  * frame #0: libsystem_c.dylib`__svfscanf_l + 5428
    frame #1: libsystem_c.dylib`scanf + 96
    frame #2: s1_lldb`main at solution_1.cpp:10:13   <-- scanf("%d", &matrix[i][j])
    frame #3: dyld`start + 6992
(lldb) frame select 2
(lldb) frame variable i j
(int) i = 2000
(int) j = 1792                       <-- 正在写第 2000 行的第 1792 列
(lldb) expr (void*)matrix
(void *) $0 = 0x0000000100008000
(lldb) expr (void*)&matrix[2000][0]
(void *) $1 = 0x0000000100f4a400
(lldb) expr (void*)&matrix[0][2000]
(void *) $2 = 0x0000000100009f40
```

**地址核对**：实机崩溃地址 `0x100f4c000`，
`&matrix[2000][0] + 1792·4 = 0x100f4a400 + 0x1C00 = 0x100f4c000` —— 与 lldb 报告的故障地址**逐位吻合**，
即崩溃点就是 `matrix[2000][1792]`（该地址已越过 16 MB 全局数组末尾 `0x100f4a400`，落在未映射页）。

### 根因分析
代码采用 1-based 下标（`i∈[1,n]`，`j∈[1,m]`），因此第一维、第二维都需要能放下下标 `n`、`m`；
题面给的上界是 `n,m ≤ 2000`，故声明至少要 `int matrix[2001][2001]`。
实际声明 `[2000][2000]` 合法下标只到 1999，于是：
- `matrix[i][2000]`（i ≤ 1998）：越出本行、落到 `matrix[i+1][0]` —— 恰好是 1-based 下标下**从未使用**的第 0 列，
  仍在数组内，**静默无害**（所以官方 3 个测试点没崩）；
- `matrix[1999][2000]`：落到 `matrix[2000][0]`，**已在 16 MB 数组之外**；
- `matrix[2000][j]`（整个第 2000 行）：整行越出 16 MB 数组，写进 .bss 之后的未映射页 → **SIGBUS**。
- solution_2 里布局是 `matrix` 紧跟 `rowsum`，`matrix[2000][j]` 会写进 `rowsum[0][j]`（未被使用，侥幸无害）；
  但其查询又读 `rowsum[r][y+b]`，当 `y+b−1=m` 时读到 `rowsum[r][m+1]`，`m=2000` 时即 `rowsum[2000][2001]`，
  **整体越出 rowsum 数组**，属于真实越界读。

### 修复方式
两份代码的数组维度 `[2000][2000]` → `[2001][2001]`（`FIX-1`）。行内前缀和改为 `rowsum[r][y+b−1] − rowsum[r][y−1]` 之后，最大下标回到 `m`，同样只需 2001。

---

## 3. BUG B —— 累加器 `sum` 未在每次询问前复位（两份共有）

### 现象
1.in 只有 4 个询问，两份程序都从**第 2 行开始**出错，数值呈"累加"特征：

| 询问 | 期望 (1.ans) | solution_1 输出 | solution_2 输出 |
|---|---|---|---|
| 1 | 1 | **1** ✅ | 2 ❌（另有 BUG D） |
| 2 | 38 | **39** (=1+38) ❌ | −55 ❌ |
| 3 | 48 | **87** (=1+38+48) ❌ | −90 ❌ |
| 4 | 76 | **163** (=1+38+48+76) ❌ | −109 ❌ |

`39 = 1+38`、`87 = 1+38+48`、`163 = 1+38+48+76` —— 明显的**前缀累加**。

### 发现方法
**静态**（第 14/21 行 `int sum = 0;` 在询问循环外）→ **黑盒**（1.in 黑盒 diff 立刻暴露）→ **输出调试**（打印每次询问的入口 sum）→ **lldb 断点**（q1 与 q2 处 sum 取值）→ **对拍**（第一个反例即复现）。

### 最小复现
`code/debug/repro/min_s1.in`（1×1 矩阵、同一个询问问两次）：

```
1 1
5
2
1 1 1 1
1 1 1 1
```
期望 `5 / 5`，`solution_1_orig` 实际输出：

```console
$ ./s1_orig < repro/min_s1.in
5
10        <-- 应为 5（5 被累加了两次）
```

### 输出调试（副本 `code/debug/dbg_s1.cpp`，未改动原文件）
在副本中加入"每次累加前后"与"询问入口/出口"打印后跑 1.in：

```
[dbg] --- query #1: x=1 y=1 a=1 b=1, sum(入口)=0
[dbg]   q1 += matrix[1][1] = 1  (sum: 0 -> 1)
[dbg] q1 结束: 累加器 sum=1  本次询问真实和 local=1  差=0
[dbg] --- query #2: x=1 y=3 a=4 b=2, sum(入口)=1        <-- 入口不是 0！
[dbg]   q2 += matrix[1][3] = 3  (sum: 1 -> 4)           <-- 从 1 开始累加
...
[dbg] q2 结束: 累加器 sum=39  本次询问真实和 local=38  差=1
[dbg] --- query #3: x=2 y=2 a=3 b=3, sum(入口)=39       <-- 入口是上一次的 39
[dbg] q3 结束: 累加器 sum=87  本次询问真实和 local=48  差=39
[dbg] q4 结束: 累加器 sum=163 本次询问真实和 local=76  差=87
```

现象非常直白：`sum(入口)` 在 q1 之后永远等于上一次的输出；
调试副本里同时打印的 `local`（每次询问从 0 开始累加的对照量）分别等于 `1, 38, 48, 76`，正是 1.ans。

### 调试器（lldb 断点观察 `sum`）
```
$ cat /tmp/lldb_s1.cmds
breakpoint set --file solution_1.cpp --line 14     # int sum = 0;
breakpoint set --file solution_1.cpp --line 23     # printf("%d\n", sum);
process launch -i .../repro/min_s1.in
...
(lldb) breakpoint set --file solution_1.cpp --line 14
Breakpoint 1: where = s1_lldb`main + 228 at solution_1.cpp:14:9
(lldb) breakpoint set --file solution_1.cpp --line 23
Breakpoint 2: where = s1_lldb`main + 464 at solution_1.cpp:23:24
(lldb) frame variable sum
(int) sum = -1                        # 第 14 行尚未执行，栈上是垃圾值
(lldb) continue
* thread #1, stop reason = breakpoint 2.1      # 第 1 个询问的 printf
->  23  	        printf("%d\n", sum);
(lldb) frame variable sum
(int) sum = 5                         # 输出 5 ✅
(lldb) continue
5
(lldb) frame variable sum
(int) sum = 10                        # 第 2 个询问的 printf：sum 没被复位！
(lldb) continue
10
```
关键点：**两次命中第 23 行断点时，`sum` 变量是同一个栈槽（同一次循环体外的声明）**，
第 2 次进入时值为 10 而不是 5，直接证明"变量声明位置错了"。

### 对拍
`battle.cpp` 第一次生成随机数据即报分歧（见 §6），`1.out`（s1）与 `2.out`（s2）首行之后就全错。

### 根因分析
`sum` 的语义是"本次询问的子矩阵和"，必须在每次询问前归零。
原代码把声明放在询问循环外（`int sum = 0;` 只执行一次），
内层 `sum += ...` 于是变成了**跨询问的全局累加器**，第 k 个询问的输出 = 前 k 个询问真值之和。
`solution_1` 与 `solution_2` 犯的是同一个错。

### 修复方式
把 `long long sum = 0;` 移到询问循环体内（`FIX-2` / `FIX-3`）。

---

## 4. BUG C —— `sum` 使用 `int` 导致溢出（两份共有）

### 现象
无越界可归咎时仍出错：自造 1999×1999（规避 BUG A）全 1e5 矩阵、询问整矩阵：

```console
$ ./s1_orig < big/ovf1999.in      # 期望 1999*1999*100000 = 399600100000
168141472
$ ./s1_fixed < big/ovf1999.in
399600100000
```
`168141472 = 399600100000 mod 2^32`（399600100000 − 93×4294967296 = 168141472），
即典型的 32 位回绕。

### 发现方法
**静态 + 量级核算**（§1 附：4e11 ≫ 2^31−1）→ **UBSan 实测**确认溢出点 → **隔离测试点**给出具体错值。

### 最小复现
`code/debug/big/ovf1999.in`：`n=m=1999`，全元素 `100000`，`q=1`，询问 `1 1 1999 1999`。

### 关键命令与输出
```console
$ g++ -O0 -g -fsanitize=undefined -std=c++17 -o s1_ubsan3 solution_1.cpp
$ ./s1_ubsan3 < big/ovf1999.in
solution_1.cpp:20:21: runtime error: signed integer overflow: 2147400000 + 100000 cannot be represented in type 'int'
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior solution_1.cpp:20:21
```
`2147400000 + 100000` 正是跨过 `INT_MAX`（2147483647）的那一步。

对 `solution_2`，同一输入的输出是 `-199900000`（BUG D 的越界读 + BUG C 的溢出叠加）。

### 根因分析
题面 `|v| ≤ 10^5`、`n,m ≤ 2000` ⇒ 单次询问最大 `4×10^11`，需要 39 bit；
`int` 只有 31 bit（有符号），必然溢出。溢出在有符号数上是 UB，实测表现为二补数回绕（静默给错值，不崩溃）。
注意 `rowsum[i][j]`（行内前缀，最大 2e8）用 `int` 是安全的，**不需要**改。

### 修复方式
`sum` 声明为 `long long`，输出格式由 `%d` 改为 `%lld`（`FIX-3` / `FIX-4`）。

---

## 5. BUG D —— solution_2 前缀和窗口整体右移一列（仅 s2）

### 现象
solution_2 在 **1.in 的**第 1 个询问就错：期望 `1`，输出 `2`；
在 2.in / 3.in 上 **4680/4680、19488/19488 全错**（比 solution_1 还差，因为它连"第一个询问"都错）。

### 发现方法
**静态**（第 26 行下标推导：`rowsum[r][y+b] − rowsum[r][y]` 得到的是列 `[y+1, y+b]` 而不是 `[y, y+b−1]`）
→ **黑盒**（1.in 第 1 行即错）→ **输出调试**（打印 rowsum 下标与取值）→ **lldb**（断在第 26 行核对下标）→ **对拍**（2.out 全错）。

### 最小复现
`code/debug/repro/min_s2.in`：

```
2 2
1 2
3 4
1
1 1 1 1
```
期望 `1`，`solution_2_orig` 实际输出：

```console
$ ./s2_orig < repro/min_s2.in
2         <-- rowsum[1][2] - rowsum[1][1] = 3 - 1 = 2，即第 2 列的和
```

### 输出调试（副本 `code/debug/dbg_s2.cpp`，未改动原文件）
```
[dbg] --- query #1: x=1 y=1 a=1 b=1 (求和区间应为行 1..1, 列 1..1), sum(入口)=0
[dbg]   行1: rowsum[1][y+b=2]=3 - rowsum[1][y=1]=1 => 2        <-- 用了 [y+b] 和 [y]
[dbg] q1 结束: sum=2 (本询问贡献=2)
[dbg] --- query #2: x=1 y=3 a=4 b=2 (求和区间应为行 1..4, 列 3..4), sum(入口)=2
[dbg]   行1: rowsum[1][y+b=5]=0 - rowsum[1][y=3]=6 => -6        <-- y+b=5 > m=4，读到未初始化的 0
[dbg]   行2: rowsum[2][y+b=5]=0 - rowsum[2][y=3]=18 => -18
[dbg]   行3: rowsum[3][y+b=5]=0 - rowsum[3][y=3]=9 => -9
[dbg]   行4: rowsum[4][y+b=5]=0 - rowsum[4][y=3]=24 => -24
[dbg] q2 结束: sum=-55 (本询问贡献=-57)                          <-- 真值 38
```
可见两个后果：
1. 窗口右移：用 `[y+b] − [y]` 得到的是列 `y+1..y+b`（多算了右边一列、漏算了第 y 列）；
2. 当 `y+b > m` 时读到**尚未初始化/越界**的 `rowsum[r][y+b]`（本例读到 0，正好是 .bss 里的初值），
   在 `m=2000` 且 `y=m` 时越出整个 `rowsum` 数组（见 §2 UBSan `index 2001 out of bounds for type 'int[2000]'`）。

### 调试器（lldb 断点 + 表达式求值）
```
(lldb) breakpoint set --file solution_2.cpp --line 26
Breakpoint 1: where = s2_lldb`main + ... at solution_2.cpp:26:27
(lldb) process launch -i .../repro/min_s2.in
* thread #1, stop reason = breakpoint 1.1
->  26  	            sum += rowsum[x + j][y + b] - rowsum[x + j][y];
(lldb) frame variable i x y a b j n m
(int) i = 1
(int) x = 1
(int) y = 1
(int) a = 1
(int) b = 1
(int) j = 0
(int) n = 2
(int) m = 2
(lldb) expr (int)(y+b)
(int) $0 = 2                       <-- 下标用的是 y+b = 2
(lldb) expr (int)rowsum[x+j][y+b]
(int) $1 = 3                       <-- = 1+2，列 1..2 的前缀和
(lldb) expr (int)rowsum[x+j][y]
(int) $2 = 1                       <-- = 1，列 1..1 的前缀和
(lldb) expr (int)matrix[x+j][y]
(int) $3 = 1                       <-- 目标元素其实是 1
(lldb) continue
2                                  <-- 3-1=2，答案错
```
即：**要的是 `rowsum[1][1] − rowsum[1][0] = 1`，代码算的是 `rowsum[1][2] − rowsum[1][1] = 2`。**

### 根因分析
设 `rowsum[i][j] = Σ_{k=1..j} matrix[i][k]`。
列区间 `[y, y+b−1]` 的和 = `rowsum[i][y+b−1] − rowsum[i][y−1]`。
原代码写成 `rowsum[i][y+b] − rowsum[i][y]`，两端各 +1 ⇒ 等价于求区间 `[y+1, y+b]`：
- 只要 `b < m`（窗口右边还有元素），结果必然错误；
- `y+b = m+1` 时还会越界读 `rowsum[i][m+1]`。

### 修复方式
改为 `sum += rowsum[x + j][y + b - 1] - rowsum[x + j][y - 1];`（`FIX-2`）。
`rowsum[i][0]` 在第 15 行已显式置 0，所以 `y−1 = 0` 的情况安全。

---

## 6. 对拍（battle 流水线）

### 原版对拍：3 秒即抓到第一个反例
```console
$ cd code/debug/battle_run && g++ -O2 -std=c++17 -o battle battle.cpp && ./battle
1,18c1,18
< 9244      <-- 1.out = solution_1
< 11865
...
---
> 9534      <-- 2.out = solution_2
> 12474
...
different output!          <-- battle.cpp 第 17 行触发，退出
```
（battle 自身在 3 秒内退出，未触发 120 s 上限。）

反例输入 `rand.in`（已归档为 `code/debug/repro/battle_counterexample.in`）：
`n=18, m=91, q=18`；首个询问 `16 31 1 24`，第二个 `12 84 2 2`。

用独立参考实现（二维前缀和 + `long long`，`code/debug/battle_run/ref.cpp`）定真值后归属分歧：

```
真值=9244   s1=9244    s2=9534     s1对=Y  s2对=N
真值=2621   s1=11865   s2=12474    s1对=N  s2对=N
真值=63559  s1=75424   s2=75409    s1对=N  s2对=N
真值=98130  s1=173554  s2=174417   s1对=N  s2对=N
真值=36112  s1=209666  s2=209928   s1对=N  s2对=N
s1 错: 17/18      s2 错: 18/18
```
- s1 第 1 个询问对、其后全错 ⇒ **BUG B**（累加不复位）。
- s2 从第 1 个询问就错 ⇒ **BUG D**（窗口右移）；第 1 个询问 `x=16 y=31 a=1 b=24`：
  正确是列 31..54，代码算的是列 32..55，多 9534−9244=290。

### 用修复版重跑：60 秒无分歧
```console
$ cd code/debug/battle_fixed_run       # 目录内 solution_1.cpp/solution_2.cpp = 修复版
$ ./battle                              # 限时 60s
60s 内未发现分歧（已 kill）
```

### ⚠️ 对拍工具的覆盖局限（必须指出）
`rand_input.cpp` 限定 `n,m ∈ [10,100]`、`v ∈ [0,1000]`、`q ∈ [10,20]`（`check_input.cpp` 第 7–16 行用 `assert` 强制），于是：
- 最大下标 100 ≪ 2000 ⇒ **永远碰不到 BUG A**（数组越界）；
- 单次最大和 `100·100·1000 = 1e7` ≪ `2^31` ⇒ **永远碰不到 BUG C**（int 溢出）；
- `v ≥ 0` ⇒ 也测不到负数场景。

即：**对拍只能稳定暴露 BUG B、BUG D；BUG A、BUG C 必须靠静态分析 + 自造边界测试点 + 消毒器**。
这也是"随机对拍通过 ≠ 程序正确"的一个实例。

---

## 7. 修复版

新增两个文件（**未改动** `solution_1.cpp` / `solution_2.cpp` / 题面 / battle 等原始附件）：

- `DSA/Lab1/code/solution_1_fixed.cpp`：`FIX-1` 数组 `[2001][2001]`；`FIX-2` `sum` 移入询问循环；`FIX-3` `long long` + `%lld`。
- `DSA/Lab1/code/solution_2_fixed.cpp`：`FIX-1` 数组 `[2001][2001]`；`FIX-2` 窗口下标 `[y+b-1] − [y-1]`；`FIX-3` `sum` 移入循环；`FIX-4` `long long` + `%lld`。

按要求**只修正确性/运行时错误，未做任何性能优化**：solution_1 保持 O(n·m + q·a·b) 朴素双重循环，solution_2 保持 O(n·m + q·a) 行内前缀和。

### ⚠️ 性能提示（非本次修复范围，但需如实记录）
solution_1 的算法本身在 3.in 上要做 `Σ a·b = 4 276 008 453` 次内层迭代（用独立计数器程序核实）：

| 编译 | 3.in 实测耗时 |
|---|---|
| `g++ -O2` | **0.49 s**（clang 自动向量化了连续内存的整数归约，本机未超时） |
| `g++ -O0` | 5 s |

本机 1s 内能过，但该复杂度在较慢的评测机上**有 TLE 风险**（题面时限 1 s）。这属于复杂度问题而非 bug，
按"不做性能优化"的要求保持原样；若需要稳过，应改用二维前缀和（参考实现见 `code/debug/battle_run/ref.cpp`）。

---

## 8. 修复版验证

### 8.1 原始命令与结果

```console
$ g++ -O2 -std=c++17 -Wall -Wextra -o s1_fixed ../solution_1_fixed.cpp    # 无警告
$ g++ -O2 -std=c++17 -Wall -Wextra -o s2_fixed ../solution_2_fixed.cpp    # 无警告

$ for t in 1 2; do for p in 1 2; do
    ./s${p}_fixed < ../../$t.in > F$t.s$p.out
    if diff -q F$t.s$p.out ../../$t.ans >/dev/null; then
      echo "[通过] 测试点 $t.in / solution_${p}_fixed"
    else echo "[失败] ..."; fi
  done; done
[通过] 测试点 1.in / solution_1_fixed
[通过] 测试点 1.in / solution_2_fixed
[通过] 测试点 2.in / solution_1_fixed
[通过] 测试点 2.in / solution_2_fixed

$ /usr/bin/time -p ./s1_fixed < ../../3.in > F3.s1.out   # real 0.49
$ diff F3.s1.out ../../3.ans                             # 无输出
[通过] 3.in / solution_1_fixed  (real 0.49s)
$ /usr/bin/time -p ./s2_fixed < ../../3.in > F3.s2.out   # real 0.16
[通过] 3.in / solution_2_fixed  (real 0.16s)
```
> 3.in 上两份修复版都**没有超时**（0.49 s / 0.16 s），因此不需要 kill。

### 8.2 额外边界与压力验证

```console
# 满规模 2000×2000，v=1e5，询问整矩阵（原版 s1 此处 SIGBUS 崩溃）
$ ./s1_fixed < big/max2000.in     # 400000000000   ✅
$ ./s2_fixed < big/max2000.in     # 400000000000   ✅
$ ./s1_fixed_asan < big/max2000.in   # 400000000000  exit=0（ASan+UBSan 全程无报错）
$ ./s2_fixed_asan < big/max2000.in   # 400000000000  exit=0（ASan+UBSan 全程无报错）

# 隔离 int 溢出点 1999×1999
$ ./s1_fixed < big/ovf1999.in     # 399600100000   ✅（原版 168141472）
$ ./s2_fixed < big/ovf1999.in     # 399600100000   ✅（原版 -199900000）
```

随机 + 边界压力测试（生成器 `code/debug/stress/gen.py`，参考实现 `ref64.cpp`＝二维前缀和 + long long，
元素范围 `[-1e5, 1e5]`，每例强制包含 4 个角、全矩阵、1×1 及贴边查询）：

```
[通过] mode=max     seed=1/2/3   (2000 2000 q=60)
[通过] mode=rowvec  seed=1/2/3   (2000 1    q=20)
[通过] mode=colvec  seed=1/2/3   (1   2000 q=20)
[通过] mode=tiny    seed=1/2/3   (1   1    q=5)
[通过] mode=rand    seed=1/2/3 各跑 3 轮，共 9 例  (随机 n,m≤2000, q≤40)
随机/边界压力测试：通过 21 组，失败 0 组
```

### 8.3 验证结果表（测试点 × 程序）

| 测试点 | solution_1（原版） | solution_2（原版） | solution_1_fixed | solution_2_fixed |
|---|---|---|---|---|
| `1.in` (4×4, q=4) | ❌ 错误 3/4 行（首行对） | ❌ 错误 4/4 行 | ✅ 通过 | ✅ 通过 |
| `2.in` (282×279, q=4680) | ❌ 错误 4679/4680 行 | ❌ 错误 4680/4680 行 | ✅ 通过 (0.01 s) | ✅ 通过 (0.00 s) |
| `3.in` (1950×1835, q=19488) | ❌ 错误 19487/19488 行，**未超时** (0.51 s) | ❌ 错误 19488/19488 行，未超时 (0.19 s) | ✅ 通过 (0.49 s) | ✅ 通过 (0.16 s) |
| `big/max2000.in` (2000×2000, v=1e5) | ❌ **运行时错误：SIGBUS，exit 138**（无输出） | ❌ 错误（输出 −100000，期望 4e11） | ✅ 通过 | ✅ 通过 |
| `big/ovf1999.in` (1999×1999) | ❌ 错误（168141472 vs 399600100000） | ❌ 错误（−199900000） | ✅ 通过 | ✅ 通过 |
| ASan+UBSan 复检 2000×2000 | ❌ global-buffer-overflow（solution_1.cpp:10） | ❌ global-buffer-overflow（solution_2.cpp:11）+ index 2000/2001 越界 | ✅ 无任何报错 | ✅ 无任何报错 |
| 随机/边界压力 21 组 | — | — | ✅ 21/21 | ✅ 21/21 |
| battle 对拍（60 s） | ❌ 3 s 内抓到分歧 | ❌ | ✅ 60 s 无分歧 | ✅ 60 s 无分歧 |

> 所有测试点两份修复版**全部通过**；没有任何一项需要标记"超时"。

---

## 9. 原始附件完整性

```
$ md5 DSA/Lab1/code/{solution_1.cpp,solution_2.cpp,battle.cpp,check_input.cpp,rand_input.cpp}
MD5 (solution_1.cpp) = c1bb94b194d8994d3726c6fd4a87c23b
MD5 (solution_2.cpp) = 54d6f126291a8c3cff76762cdc30e8f3
MD5 (battle.cpp)     = 04c76c7258424f24282a964345b39fb1
MD5 (check_input.cpp)= d44512433db37cf344d8f4e43e5a06e6
MD5 (rand_input.cpp) = 661cec66fcc117b92f9e0d885898b885
```
题面（`1.in/1.ans/2.in/2.ans/3.in/3.ans`、`Tsinghua Online Judge.html`）与上述源码均**只读使用，未做任何改动**；
新增文件全部位于 `DSA/Lab1/code/solution_1_fixed.cpp`、`DSA/Lab1/code/solution_2_fixed.cpp`、
`DSA/Lab1/code/debug/`（调试副本、测试点、日志）、`DSA/Lab1/report/task3_debugging.md`。

---

## 10. 结论汇总：bug 与发现方法对照

| # | Bug | 位置 | 类型 | 主要由哪种方法发现 |
|---|---|---|---|---|
| A | 数组维度 `[2000][2000]` 不足（1-based 下标需 2001；查询还会读 `rowsum[r][m+1]`） | s1:3 / s2:3,4 | **运行时错误**（满规模 SIGBUS）；小规模下为静默越界 | 静态（下标推导）→ 黑盒自造 2000×2000 测试点实测 SIGBUS → ASan/UBSan → lldb 崩溃现场地址核对 |
| B | `sum` 声明在询问循环外，累加器跨询问累积 | s1:14 / s2:21 | 结果错误 | 静态 → 黑盒（1.in 第 2 行起全错）→ 输出调试（入口 sum 打印）→ lldb 断点（q1 sum=5 / q2 sum=10）→ 对拍 |
| C | `sum` 用 `int`（应为 `long long`），最大和 4e11 溢出 | s1:14,20,23 / s2:21,26,28 | 结果错误（静默回绕/UB） | 静态 + 容量核算 → UBSan（`signed integer overflow: 2147400000 + 100000`）→ 隔离测试点 ovf1999 |
| D | solution_2 前缀和窗口整体右移一列：`[y+b]−[y]` 应为 `[y+b−1]−[y−1]`（并连带 `y+b>m` 的越界读） | s2:26 | 结果错误（**几乎全部询问都错**） | 静态 → 黑盒（1.in 首行即错）→ 输出调试（rowsum 下标/取值打印）→ lldb 下标核对 → 对拍（2.out 全错） |

修复后：`1.in`、`2.in`、`3.in` 三个官方测试点 + 满规模/边界/溢出 2 个自造测试点 + 21 组随机边界压力 + 60 s 对拍，
**两份修复版全部通过**（详见 §8.3）。
