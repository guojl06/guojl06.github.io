// Homework 1 — Formal Languages and Automata
#set page(
  paper: "us-letter",
  margin: (x: 1.0in, y: 0.9in),
  numbering: "1",
  number-align: center,
)
#set text(font: ("Times New Roman", "Songti SC"), size: 11pt, lang: "zh")
#set par(justify: true, leading: 0.78em)
#show heading.where(level: 1): it => block(above: 1.4em, below: 0.6em, text(
  font: ("Times New Roman", "PingFang SC"), size: 12.5pt, weight: "bold", it.body,
))
#show heading.where(level: 2): it => block(above: 1.0em, below: 0.4em, text(
  font: ("Times New Roman", "PingFang SC"), size: 11.5pt, weight: "bold", it.body,
))

#align(center)[
  #text(size: 15pt, weight: "bold")[Homework 1] \
  #v(0.2em)
  #text(size: 10.5pt)[郭嘉乐 #h(1.5em) 2025013332]
]
#v(0.6em)

// ============================================================
= Problem 1

对一切状态 $p$ 与一切 string $x, y$，要证明
$ hat(delta)(p, x y) = hat(delta)(hat(delta)(p, x), y). $

对 $|y|$ 作 Induction。

$|y| = 0$ 时 $y = epsilon$，此时 $x y = x$。由定义 $hat(delta)(q, epsilon) = q$，取 $q = hat(delta)(p, x)$ 得
$ hat(delta)(p, x y) = hat(delta)(p, x) = hat(delta)(hat(delta)(p, x), epsilon) = hat(delta)(hat(delta)(p, x), y). $

设 $|y'| = n$ 时等式对一切状态 $p$ 与一切 string $x$ 都成立。把 $y$ 写成 $y = y' a$，其中 $a$ 是 $y$ 的最后一个符号，则
$ hat(delta)(p, x y) &= hat(delta)(p, x y' a) \
  &= delta(hat(delta)(p, x y'), a) \
  &= delta(hat(delta)(hat(delta)(p, x), y'), a) \
  &= hat(delta)(hat(delta)(p, x), y' a) \
  &= hat(delta)(hat(delta)(p, x), y). $

证毕。

// ============================================================
= Problem 2

四个 DFA 都写成 $A = (Q, Sigma, delta, q_0, F)$，其中字母表 $Sigma = \{0, 1\}$。

== (a) 含三个连续 $0$ 的 string

$Q = \{q_0, q_1, q_2, q_3\}$，起始状态 $q_0$，接受状态 $F = \{q_3\}$。状态 $q_i$ 表示已经读入的 string 末尾有 $i$ 个连续的 $0$，超过 $3$ 的按 $3$ 记，也就是到了 $q_3$ 之后一直留在 $q_3$。转移关系：

- $delta(q_i, 0) = q_(min(i + 1, 3))$
- $delta(q_i, 1) = q_0$

对 $|w|$ 作 Induction 可知 $hat(delta)(q_0, w) = q_i$ 里的 $i$ 恰好是 $w$ 末尾连续 $0$ 的个数：读入 $1$ 时末尾连续 $0$ 的个数变成 $0$，读入 $0$ 时个数加 $1$ 但不超过 $3$，两种情况都与上面的转移关系一致。因此
$ w in L(A) <=> w "末尾有三个连续的" 0 <=> w "含有子串" 000 . $

== (b) 含子串 $011$ 的 string

$Q = \{s_0, s_1, s_2, s_3\}$，起始状态 $s_0$，接受状态 $F = \{s_3\}$。状态 $s_j$ 表示已读入的 string 末尾与 $011$ 的前 $j$ 个符号相同，并且这样的 $j$ 取最大。转移关系：

- $s_0$ 读 $0$ 到 $s_1$，读 $1$ 留在 $s_0$；
- $s_1$ 读 $1$ 到 $s_2$，读 $0$ 留在 $s_1$；
- $s_2$ 读 $1$ 到 $s_3$，读 $0$ 回到 $s_1$；
- $s_3$ 读 $0$ 或 $1$ 都到 $s_3$。

$s_3$ 读什么都回到自己，因为 $011$ 一旦出现就不会再消失。对 $|w|$ 作 Induction 可以验证：读入新符号后，要么多凑出一个前缀符号，要么退到最长的、仍然是末尾的前缀，例如在 $s_2$ 读到 $0$ 时末尾是 $010$，最长的是 $0$，所以回到 $s_1$。因此 $w$ 被接受当且仅当 $011$ 是 $w$ 的子串。

== (c) 从右边数第 $10$ 个符号是 $1$ 的 string

取 $Q$ 为所有长度不超过 $10$ 的、由 $0$ 和 $1$ 组成的 string，起始状态 $q_0 = epsilon$，接受状态是所有长度正好是 $10$ 且以 $1$ 开头的 string。读入符号 $a$ 时

- 若 $|q| < 10$，则 $delta(q, a) = q a$；
- 若 $|q| = 10$，则 $delta(q, a)$ 是去掉 $q$ 的第一个符号以后再接上 $a$。

所以 $|Q| = 2^11 - 1 = 2047$，$|F| = 2^9 = 512$。

对 $|w|$ 作 Induction 可知读完 $w$ 之后状态恰好是 $w$ 最近的 $min(10, |w|)$ 个符号：长度不到 $10$ 时每读一个符号就接在后面，长度到了 $10$ 之后每读一个符号就丢掉最旧的那一个。所以这个状态被接受当且仅当 $|w| >= 10$ 且其中最旧的符号是 $1$，也就是右边数第 $10$ 个符号是 $1$。

== (d) $0$ 的个数被 $5$ 整除，且 $1$ 的个数被 $3$ 整除

记 $N_0 (w)$、$N_1 (w)$ 为 string $w$ 中 $0$、$1$ 的个数。取状态 $(i, j)$，其中 $i$ 是 $N_0$ 除以 $5$ 的余数、$j$ 是 $N_1$ 除以 $3$ 的余数：
$ Q = \{0, 1, 2, 3, 4\} times \{0, 1, 2\}, quad q_0 = (0, 0), quad F = \{(0, 0)\}, $
转移关系：

- $delta((i, j), 0) = ((i + 1) mod 5, j)$
- $delta((i, j), 1) = (i, (j + 1) mod 3)$

一共 $5 times 3 = 15$ 个状态。对 $|w|$ 作 Induction：读入 $0$ 时第一个分量加 $1$、第二个分量不变，读入 $1$ 时反过来，与转移关系一致，所以
$ hat(delta)((0, 0), w) = (N_0 (w) mod 5, N_1 (w) mod 3). $
于是 $w in L(A)$ 当且仅当 $N_0 (w) equiv 0 (mod 5)$ 且 $N_1 (w) equiv 0 (mod 3)$。

// ============================================================
= Problem 3

设 $A = (Q, Sigma, delta, q_0, \{q_f\})$，且对每个 $a in Sigma$ 都有 $delta(q_0, a) = delta(q_f, a)$。

*(a)* 对 $|w|$ 作 Induction，其中 $|w| >= 1$。

$|w| = 1$ 时 $w = a in Sigma$，由假设
$ hat(delta)(q_0, a) = delta(q_0, a) = delta(q_f, a) = hat(delta)(q_f, a). $

设 $|v| = n >= 1$ 时 $hat(delta)(q_0, v) = hat(delta)(q_f, v)$ 成立，取 $w = v a$，则
$ hat(delta)(q_0, v a) = delta(hat(delta)(q_0, v), a) = delta(hat(delta)(q_f, v), a) = hat(delta)(q_f, v a), $
归纳假设。因此对一切 $w != epsilon$ 都有 $hat(delta)(q_0, w) = hat(delta)(q_f, w)$。

*(b)* 设 $x != epsilon$ 且 $x in L(A)$，即 $hat(delta)(q_0, x) = q_f$。对 $k$ 作 Induction，证明 $hat(delta)(q_0, x^k) = q_f$。

$k = 1$ 时就是 $hat(delta)(q_0, x) = q_f$，由 $x in L(A)$ 得到。

设 $hat(delta)(q_0, x^(k - 1)) = q_f$ 成立，由 Problem 1 的结论把 string 拆开：
$ hat(delta)(q_0, x^k) &= hat(delta)(q_0, x^(k - 1) x) \
  &= hat(delta)(hat(delta)(q_0, x^(k - 1)), x) \
  &= hat(delta)(q_f, x) \
  &= hat(delta)(q_0, x) \
  &= q_f . $

所以对一切 $k > 0$ 都有 $x^k in L(A)$。

// ============================================================
= Problem 4

原 NFA 的起始状态是 $p$，接受状态是 $q$ 和 $s$，转移关系是

- $delta(p, 0) = \{q, s\}$，$delta(p, 1) = \{q\}$；
- $delta(q, 0) = \{r\}$，$delta(q, 1) = \{q, r\}$；
- $delta(r, 0) = \{s\}$，$delta(r, 1) = \{p\}$；
- $delta(s, 0) = emptyset$，$delta(s, 1) = \{p\}$。

用子集构造法：把每个状态集合看成新 DFA 的一个状态，转移关系是
$ delta_D (P, a) = union.big_(r in P) delta(r, a), $
起始状态是 $\{p\}$，接受状态是所有含 $q$ 或含 $s$ 的子集。从 $\{p\}$ 出发逐个算出新出现的子集，一共得到 $10$ 个可达子集，下表列出它们：

#block(breakable: false, align(center, table(
    columns: 3,
    align: center + horizon,
    stroke: 0.5pt,
    table.header([状态], [读 $0$], [读 $1$]),
    [$\{p\}$], [$\{q, s\}$], [$\{q\}$],
    [$\{q\}$], [$\{r\}$], [$\{q, r\}$],
    [$\{q, s\}$], [$\{r\}$], [$\{p, q, r\}$],
    [$\{q, r\}$], [$\{r, s\}$], [$\{p, q, r\}$],
    [$\{p, q, r\}$], [$\{q, r, s\}$], [$\{p, q, r\}$],
    [$\{q, r, s\}$], [$\{r, s\}$], [$\{p, q, r\}$],
    [$r$], [$\{s\}$], [$\{p\}$],
    [$\{r, s\}$], [$\{s\}$], [$\{p\}$],
    [$\{s\}$], [$emptyset$], [$\{p\}$],
    [$emptyset$], [$emptyset$], [$emptyset$],
  )))


下面证明新 DFA 与原 NFA 等价。对 NFA 记 $hat(delta)(p, w)$ 为从 $p$ 出发读完 $w$ 之后所有可能到达的状态组成的集合，要证明
$ hat(delta)_D (\{p\}, w) = hat(delta)(p, w) $
对一切 string $w$ 成立。对 $|w|$ 作 Induction，归纳的对象是子集 $hat(delta)_D (\{p\}, w)$。

$|w| = 0$ 时两边都是 $\{p\}$。设 $|w'| = n$ 时等式成立，$w = w' a$，则
$ hat(delta)_D (\{p\}, w' a) &= delta_D (hat(delta)_D (\{p\}, w'), a) \
  &= delta_D (hat(delta)(p, w'), a) \
  &= union.big_(r in hat(delta)(p, w')) delta(r, a) \
  &= hat(delta)(p, w' a). $

于是 $w$ 被这个 DFA 接受当且仅当 $hat(delta)(p, w)$ 含 $q$ 或含 $s$，当且仅当 $w$ 被原 NFA 接受。

// ============================================================
= Problem 5

== (a) 最后一位 digit 之前没有出现过

字母表 $Sigma = \{0, 1, dots, 9\}$，目标语言是
$ union.big_(d in Sigma) (Sigma without \{d\})^* \{d\}, $
也就是最后一位是 $d$，而 $d$ 在前面没有出现过。

取 NFA：状态 $s$ 是起始状态，每个 digit $d$ 配两个状态 $q_d$ 和 $f_d$，所有 $f_d$ 都是接受状态，一共 $1 + 2 times 10 = 21$ 个状态。转移关系：

- $s$ 读 $epsilon$ 到每个 $q_d$，也就是在开头非确定地猜出最后一位是哪个 digit；
- $q_d$ 读 $c != d$ 留在 $q_d$，读 $d$ 到 $f_d$；
- $f_d$ 没有出边。

Induction。设 $R(w) = hat(delta)(s, w)$，同时证明：

- $q_d in R(w)$ 当且仅当 $w$ 中不含 $d$；
- $f_d in R(w)$ 当且仅当 $w = u d$ 且 $u$ 中不含 $d$。

$|w| = 0$ 时 $R(epsilon) = \{s\} union \{q_d : d in Sigma\}$，两条都成立，空 string 不含任何 digit，也没有最后一位。设两条对 $w'$ 成立、$w = w' a$。读入 $a$ 之后，$q_d$ 只可能从 $q_d$ 自己过来，而且要求 $a != d$，所以 $q_d in R(w)$ 当且仅当 $a != d$ 且 $q_d in R(w')$，由归纳假设就是 $w$ 中不含 $d$；$f_d$ 只可能从 $q_d$ 读 $d$ 过来，所以 $f_d in R(w)$ 当且仅当 $a = d$ 且 $q_d in R(w')$，由归纳假设就是 $w = w' d$ 且 $w'$ 中不含 $d$。两条都由 Induction 成立，于是 $w$ 被接受当且仅当存在 digit $d$ 使 $f_d in R(w)$，也就是最后一位 digit 在它之前没有出现过。

== (b) 两个 $0$ 之间相隔的位置数是 $4$ 的倍数

若两个 $0$ 的位置是 $i < j$，条件就是它们之间符号的个数 $j - i - 1$ 能被 $4$ 整除。$0$ 也是 $4$ 的倍数，所以相邻的两个 $0$ 也可以。

取 NFA：状态 $A$ 是起始状态，另有 $B_0, B_1, B_2, B_3$ 和接受状态 $C$。转移关系：

- $A$ 读 $0$ 到 $A$，同时也可以读到 $B_0$，也就是非确定地决定这一位是不是所选那一对 $0$ 中的第一个，读 $1$ 留在 $A$；
- $B_k$ 读 $0$ 或读 $1$ 都到 $B_((k + 1) mod 4)$，用来数中间隔了几个符号；
- $B_0$ 读 $0$ 还可以到 $C$，也就是中间隔了 $4$ 的倍数个符号之后又见到 $0$；
- $C$ 读 $0$ 或读 $1$ 都回到 $C$。

设 $R(w) = hat(delta)(A, w)$，对 $|w|$ 作 Induction，同时证明：

- $A in R(w)$；
- $B_k in R(w)$ 当且仅当存在分解 $w = u 0 v$ 且 $|v| equiv k (mod 4)$；
- $C in R(w)$ 当且仅当 $w$ 中有两个 $0$，它们之间相隔的符号个数能被 $4$ 整除。

$|w| = 0$ 时 $R(epsilon) = \{A\}$，三条都成立。设三条对 $w'$ 成立、$w = w' a$，则由
$ R(w) = union.big_(r in R(w')) delta(r, a) $
和转移关系可以逐条验证。

$B_k in R(w)$ 当且仅当 $a = 0$ 且 $k = 0$，也就是 $A$ 读 $0$ 直接到 $B_0$，或者 $B_((k - 1) mod 4) in R(w')$。前一种情形取 $u = w'$、$v = epsilon$，就有 $w = u 0 v$ 且 $|v| = 0 equiv k (mod 4)$；后一种情形由归纳假设有 $w' = u 0 v$ 且 $|v| equiv k - 1 (mod 4)$，于是 $w = u 0 (v a)$ 且 $|v a| equiv k (mod 4)$。反过来，若 $w = u 0 v$ 且 $|v| equiv k (mod 4)$，当 $v = epsilon$ 时属于前一种情形，当 $v != epsilon$ 时写 $v = v' a$，由归纳假设 $B_((k - 1) mod 4) in R(w')$，属于后一种情形。

$C in R(w)$ 当且仅当 $C in R(w')$，或者 $a = 0$ 且 $B_0 in R(w')$。前一种情形 $w'$ 里已经有一对符合条件的 $0$，$w$ 当然也有；后一种情形由归纳假设 $w' = u 0 v$ 且 $|v| equiv 0 (mod 4)$，于是 $w = u 0 v 0$，中间正好隔了 $|v|$ 个符号。反过来，若 $w$ 中符合条件的那一对 $0$ 都在 $w'$ 里，属于前一种情形；否则第二个 $0$ 就是最后读入的符号，此时 $a = 0$，$w' = u 0 v$ 且 $|v| equiv 0 (mod 4)$，属于后一种情形。

三条都由 Induction 成立，所以 $w$ 被接受当且仅当 $C in R(w)$，当且仅当 $w$ 中有两个 $0$ 且它们之间相隔的符号个数能被 $4$ 整除。
