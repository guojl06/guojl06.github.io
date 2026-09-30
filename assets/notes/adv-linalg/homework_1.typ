#import "../module/myutils.typ" : *

#show : conf

= 紫荆53 郭嘉乐 2025013332 高等线性代数选讲 作业

#outline()

// =====================================================================

== 第 1 次 #datetime(day:22,month:3,year:2026).display()

=== 1.1.6

==== (1) 证明 $cos(3theta) = 4cos^3 theta - 3cos theta$

$
cos(3theta) &= cos(2theta + theta) \
            &= cos 2theta cos theta - sin 2theta sin theta \
            &= (2cos^2 theta - 1)cos theta - 2sin theta cos theta dot sin theta \
            &= cos theta lr((2cos^2 theta - 1 - 2sin^2 theta)) \
            &= cos theta lr((2cos^2 theta - 1 - 2(1 - cos^2 theta))) \
            &= cos theta lr((4cos^2 theta - 3)) = 4cos^3 theta - 3cos theta. quad square
$

==== (2) 计算 $T_2(x),, T_3(x)$，并证明 $cos(n theta) = T_n(cos theta),, forall n >= 0$

由递推公式 $T_(n+1)(x) = 2x T_n(x) - T_(n-1)(x)$：
$
T_2(x) = 2x dot x - 1 = 2x^2 - 1, quad quad T_3(x) = 2x(2x^2 - 1) - x = 4x^3 - 3x.
$

*证明*

-  $T_0(cos theta) = 1 = cos 0$，$T_1(cos theta) = cos theta = cos theta$，成立。
- *归纳：* 设对某 $k >= 1$，$T_(k-1)(cos theta) = cos(k-1)theta$ 与 $T_k(cos theta) = cos(k theta)$ 均成立。则
$
T_(k+1)(cos theta) = 2cos theta dot T_k(cos theta) - T_(k-1)(cos theta)
                   = 2cos theta cos(k theta) - cos((k-1)theta).
$
由积化和差公式 $2cos theta cos(k theta) = cos((k+1)theta) + cos((k-1)theta)$，代入得
$
T_(k+1)(cos theta) = cos((k+1)theta) + cos((k-1)theta) - cos((k-1)theta) = cos((k+1)theta). quad square
$

==== (3) $T_n(x)$ 是 $n$ 次整系数多项式，求所有实根，并证明 $|T_n(x)| <= 1$（$|x| <= 1$）

*$n$ 次整系数多项式：* 对 $n$ 归纳。$T_0 = 1$，$T_1 = x$ 是整系数多项式，次数分别为 $0,1$。若 $T_(n-1)$ 是 $n-1$ 次、$T_n$ 是 $n$ 次整系数多项式，则 $T_(n+1) = 2x T_n - T_(n-1)$ 是 $n+1$ 次整系数多项式。$square$

*所有实根：* 令 $x = cos theta$，则
$
T_n(x) = 0 <==> cos(n theta) = 0 <==> n theta = frac(pi, 2) + k pi, quad k in ZZ.
$
对 $x in [-1, 1]$，取 $theta in [0, pi]$，满足条件的值为 $theta_k = frac((2k+1)pi, 2n)$，$k = 0, 1, ..., n-1$。故 $T_n(x)$ 的 $n$ 个实根为
$
x_k = cos frac((2k+1)pi, 2n), quad k = 0, 1, ..., n-1.
$

*$|T_n(x)| <= 1$（$|x| <= 1$）：* 若 $|x| <= 1$，取 $theta in [0, pi]$ 使 $cos theta = x$，则
$|T_n(x)| = |cos(n theta)| <= 1. quad square$

==== (4) 证明 $sin(3theta) = sin theta (4cos^2 theta - 1)$

*证明：*
$
sin(3theta) &= sin(2theta + theta) = sin 2theta cos theta + cos 2theta sin theta \
            &= 2sin theta cos^2 theta + (2cos^2 theta - 1)sin theta \
            &= sin theta lr((2cos^2 theta + 2cos^2 theta - 1)) = sin theta (4cos^2 theta - 1). quad square
$

==== (5) 计算 $U_2(x),, U_3(x)$，并证明 $sin((n+1)theta) = sin theta dot U_n(cos theta),, forall n >= 0$

由递推公式 $U_(n+1)(x) = 2x U_n(x) - U_(n-1)(x)$：
$
U_2(x) = 2x dot 2x - 1 = 4x^2 - 1, quad quad U_3(x) = 2x(4x^2 - 1) - 2x = 8x^3 - 4x.
$

*证明：*

- $sin theta dot U_0(cos theta) = sin theta = sin(1 dot theta)$；$sin theta dot U_1(cos theta) = 2sin theta cos theta = sin(2theta)$，成立。
- *归纳步：* 设 $sin(k theta) = sin theta dot U_(k-1)(cos theta)$ 与 $sin((k+1)theta) = sin theta dot U_k(cos theta)$ 成立。则
$
sin theta dot U_(k+1)(cos theta) &= sin theta lr([2cos theta dot U_k(cos theta) - U_(k-1)(cos theta)]) \
                                   &= 2cos theta dot sin theta U_k(cos theta) - sin theta U_(k-1)(cos theta) \
                                   &= 2cos theta sin((k+1)theta) - sin(k theta).
$
由积化和差 $2cos theta sin((k+1)theta) = sin((k+2)theta) + sin(k theta)$，代入得
$
sin theta dot U_(k+1)(cos theta) = sin((k+2)theta). quad square
$

==== (6) $U_n(x)$ 是 $n$ 次整系数多项式，求所有实根

*$n$ 次整系数多项式：* 同 (3) 中对 $T_n$ 的证明，对 $U_n$ 的递推式 $U_(n+1) = 2x U_n - U_(n-1)$ 归纳即可。$square$

*所有实根：* 令 $x = cos theta$（$theta in (0, pi)$，即 $sin theta != 0$）。则
$
U_n(cos theta) = 0 <==> sin((n+1)theta) = 0 <==> (n+1)theta = k pi, quad k in ZZ.
$
结合 $theta in (0, pi)$，取 $k = 1, 2, ..., n$，得 $n$ 个实根
$
x_k = cos frac(k pi, n+1), quad k = 1, 2, ..., n.
$

==== (7) 利用 $cos(4pi\/5) = cos(6pi\/5)$ 证明 $cos(2pi\/5) = (sqrt(5)-1)\/4$

*证明：* 令 $x = cos(2pi\/5)$。由 (2) 题，$T_2(x) = cos(4pi\/5)$，$T_3(x) = cos(6pi\/5)$。

注意到 $cos(6pi\/5) = cos(2pi - 4pi\/5) = cos(4pi\/5)$，故 $T_2(x) = T_3(x)$：
$
2x^2 - 1 = 4x^3 - 3x ==> 4x^3 - 2x^2 - 3x + 1 = 0.
$
验证 $x = 1$ 是根，分解得
$
4x^3 - 2x^2 - 3x + 1 = (x - 1)(4x^2 + 2x - 1).
$
因 $cos(2pi\/5) != 1$，故 $4x^2 + 2x - 1 = 0$，解得
$
x = frac(-1 plus.minus sqrt(5), 4).
$
由于 $2pi\/5 < pi\/2$，$cos(2pi\/5) > 0$，取正根
$
cos frac(2pi, 5) = frac(sqrt(5) - 1, 4). quad square
$

==== (8) $K_n$ 的特征多项式、特征值与特征向量

*特征多项式：* 令 $p_n(lambda) = det(lambda I - K_n)$。矩阵 $lambda I - K_n$ 是对角元为 $lambda - 2$、次对角元为 $1$ 的三对角矩阵。按最后一行展开：
$
p_n(lambda) = (lambda - 2) p_(n-1)(lambda) - p_(n-2)(lambda),
$
初始值 $p_0 = 1$，$p_1(lambda) = lambda - 2$。

令 $mu = (lambda-2)\/2$，递推化为 $p_n = 2mu dot p_(n-1) - p_(n-2)$，与 $U_n$ 的递推完全一致。初始值 $U_0(mu) = 1 = p_0$，$U_1(mu) = 2mu = lambda - 2 = p_1$。由归纳得
$
p_n(lambda) = U_n frac(lambda - 2, 2). quad square
$

*特征值：* $U_n((lambda-2)\/2) = 0$ 且 $sin theta != 0$（令 $cos theta = (lambda-2)\/2$），得 $theta = k pi\/(n+1)$，$k = 1, ..., n$，对应
$
lambda_k = 2 + 2cos frac(k pi, n+1), quad k = 1, 2, ..., n.
$

*特征向量：* 对 $lambda_k$，取 $alpha_k = k pi\/(n+1)$，令
$
bold(v)_k = lr((sin alpha_k,, sin 2alpha_k,, ...,, sin n alpha_k))^T.
$
验证第 $j$ 分量（$1 <= j <= n$）：
$
(K_n bold(v)_k)_j &= 2sin(j alpha_k) - sin((j-1)alpha_k) - sin((j+1)alpha_k).
$
由和差化积 $sin((j-1)alpha_k) + sin((j+1)alpha_k) = 2sin(j alpha_k) cos alpha_k$，故
$
(K_n bold(v)_k)_j = 2sin(j alpha_k)(1 - cos alpha_k) = (2 - 2cos alpha_k) sin(j alpha_k) = lambda_k (bold(v)_k)_j.
$
边界项 $(j=0 text("或") j=n+1)$：$sin(0) = sin((n+1)alpha_k) = sin(k pi) = 0$，自动满足。

$bold(v)_1, ..., bold(v)_n$ 对应 $n$ 个互不相同的特征值，线性无关，构成 $K_n$ 的全部特征向量。$square$

// =====================================================================
=== 1.2.7

**(1)** 1 阶酉阵与模为 1 的复数一一对应。

*证明：* 设 $Q = [q] in M_1(CC)$ 满足 $overline(Q)^T Q = [|q|^2] = I_1 = [1]$，故 $|q| = 1$。反之，$|q| = 1$ 时 $overline(q) dot q = 1$，故 $[q]$ 为 1 阶酉阵。映射 $q arrow.r.bar [q]$ 是双射。$square$

**(2)** $D = op("diag")(e^(i theta_1), ..., e^(i theta_n))$ 是酉阵；反之，对角酉阵均具有此形式。

*证明：*
$
overline(D)^T D = op("diag")(e^(-i theta_1), ..., e^(-i theta_n)) dot op("diag")(e^(i theta_1), ..., e^(i theta_n)) = op("diag")(1, ..., 1) = I_n,
$
故 $D$ 是酉阵。

反之，设 $Q = op("diag")(q_1, ..., q_n)$ 为对角酉阵，则 $overline(Q)^T Q = op("diag")(|q_1|^2, ..., |q_n|^2) = I_n$，故 $|q_k| = 1$，每个 $q_k = e^(i theta_k)$ 对某 $theta_k in RR$ 成立。$square$

**(3)** 1.2.6中的标准正交基 $epsilon_1, epsilon_2, epsilon_3$ 给出 3 阶酉阵。

*证明：* 例 1.2.6 通过 Gram-Schmidt 正交化构造了 $CC^3$ 的标准正交基 $epsilon_1, epsilon_2, epsilon_3$，满足 $angle.l epsilon_i, epsilon_j angle.r = overline(epsilon)_i^T epsilon_j = delta_(i j)$。令 $Q = [epsilon_1 wide epsilon_2 wide epsilon_3] in M_3(CC)$，由引理 1.2.5，$Q$ 的列为单位正交向量组等价于 $overline(Q)^T Q = I_3$，故 $Q$ 是 3 阶酉阵。$square$

// =====================================================================
=== 1.2.3

以下 $S, S_1, S_2$ 为 $n$ 阶厄米特阵，$A$ 为 $n$ 阶复方阵。

==== (1) 若 $overline(bold(z))^T S bold(z) = 0$ 对所有 $bold(z) in CC^n$，则 $S = 0$

*证明：* 对任意 $alpha, beta in CC^n$，分别令 $bold(z) = alpha + beta$ 与 $bold(z) = alpha + i beta$，并利用假设（$overline(alpha)^T S alpha = overline(beta)^T S beta = 0$）：

令 $bold(z) = alpha + beta$，展开得
$
overline(alpha)^T S beta + overline(beta)^T S alpha = 0. quad (ast)
$
令 $bold(z) = alpha + i beta$（此时 $overline(bold(z))^T = overline(alpha)^T - i overline(beta)^T$），展开得
$
i overline(alpha)^T S beta - i overline(beta)^T S alpha = 0 ==> overline(alpha)^T S beta = overline(beta)^T S alpha. quad (ast ast)
$
$(ast) + (ast ast)$ 得 $2 overline(alpha)^T S beta = 0$，即对所有 $alpha, beta in CC^n$ 有 $overline(alpha)^T S beta = 0$。

特别地，取 $alpha = e_i$，$beta = e_j$（标准基，均为实向量）：$e_i^T S e_j = s_(i j) = 0$。由 $i, j$ 的任意性，$S = 0$。$square$

==== (2) 若 $overline(bold(z))^T S_1 bold(z) = overline(bold(z))^T S_2 bold(z)$ 对所有 $bold(z) in CC^n$，则 $S_1 = S_2$

*证明：* 令 $T = S_1 - S_2$，则 $T$ 是厄米特阵，且 $overline(bold(z))^T T bold(z) = 0$ 对所有 $bold(z) in CC^n$。由 (1) 得 $T = 0$，即 $S_1 = S_2$。$square$

==== (3) $overline(A)^T A$ 是厄米特阵

*证明：* 需验证 $overline(overline(A)^T A)^T = overline(A)^T A$。由引理 1.2.1，
$
overline(overline(A)^T A) = overline(overline(A)^T) dot overline(A) = A^T overline(A).
$
再取转置：$(A^T overline(A))^T = overline(A)^T (A^T)^T = overline(A)^T A$。故 $overline(overline(A)^T A)^T = overline(A)^T A$，即 $overline(A)^T A$ 是厄米特阵。$square$

==== (4) 若 $||A bold(z)|| = ||bold(z)||$ 对所有 $bold(z) in CC^n$，则 $A$ 是酉阵

*证明：* 由题设，对任意 $bold(z) in CC^n$，
$
overline(bold(z))^T (overline(A)^T A) bold(z) = ||A bold(z)||^2 = ||bold(z)||^2 = overline(bold(z))^T I_n bold(z),
$
故 $overline(bold(z))^T (overline(A)^T A - I_n) bold(z) = 0$ 对所有 $bold(z) in CC^n$ 成立。

由 (3)，$overline(A)^T A$ 是厄米特阵；$I_n$ 也是厄米特阵；故 $overline(A)^T A - I_n$ 是厄米特阵。由 (1) 得 $overline(A)^T A - I_n = 0$，即 $overline(A)^T A = I_n$，故 $A$ 是酉阵。$square$

// =====================================================================
==== 2 阶（特殊）酉矩阵的结构

 $2$ 阶行列式为 $1$ 的酉矩阵均形如 $mat(delim: "[", c, s; -overline(s), overline(c))$，其中 $c, s in CC$，$|c|^2 + |s|^2 = 1$；反之，所有此形式的矩阵均为行列式为 1 的 2 阶酉阵。

*证明（充分性）：* 设 $Q = mat(delim: "[", c, s; -overline(s), overline(c))$，$|c|^2 + |s|^2 = 1$，直接验证：
$
overline(Q)^T Q = mat(delim: "[", overline(c), -s; overline(s), c) mat(delim: "[", c, s; -overline(s), overline(c)) = mat(delim: "[", |c|^2 + |s|^2, 0; 0, |s|^2 + |c|^2) = I_2,
$
故 $Q$ 是酉阵。行列式 $det Q = c overline(c) + s overline(s) = |c|^2 + |s|^2 = 1$。$square$

*证明（必要性）：* 设 $Q = mat(delim: "[", z_1, z_2; z_3, z_4)$ 是行列式为 $1$ 的 2 阶酉阵（即 $overline(Q)^T Q = I_2$，$det Q = 1$）。

$overline(Q)^T Q = I_2$ 等价于 $Q$ 的两列为单位正交向量：
$
|z_1|^2 + |z_3|^2 = 1, quad |z_2|^2 + |z_4|^2 = 1, quad overline(z_1) z_2 + overline(z_3) z_4 = 0.
$

由正交条件 $overline(z_1) z_2 = -overline(z_3) z_4$。

- 若 $z_2 != 0$（若 $z_3 != 0$）：由 $overline(z_3) = -overline(z_1) z_2 \/ z_4$，整理得 $mat(delim:"[", z_3; z_4) = -(z_3 \/ overline(z_2)) mat(delim:"[", -overline(z_2); overline(z_1))$。
- 若 $z_1 != 0$（若 $z_4 != 0$）：由 $overline(z_1) = -overline(z_3) z_4 \/ z_2$，整理得 $mat(delim:"[", z_3; z_4) = (z_4 \/ overline(z_1)) mat(delim:"[", -overline(z_2); overline(z_1))$。

无论哪种情况，均存在 $c' in CC$ 使
$
mat(delim: "[", z_3; z_4) = c' mat(delim: "[", -overline(z_2); overline(z_1)), quad "即" quad Q = mat(delim: "[", z_1, z_2; -c' overline(z_2), c' overline(z_1)).
$

由单位列条件 $|z_3|^2 + |z_4|^2 = |c'|^2(|z_2|^2 + |z_1|^2) = |c'|^2 = 1$，故 $|c'| = 1$。

计算行列式：$det Q = c' z_1 overline(z_1) + c' z_2 overline(z_2) = c'(|z_1|^2 + |z_2|^2) = c' dot 1 = c'$。

由题设 $det Q = 1$，故 $c' = 1$，于是
$
Q = mat(delim: "[", z_1, z_2; -overline(z_2), overline(z_1)).
$
令 $c = z_1$，$s = z_2$，满足 $|c|^2 + |s|^2 = |z_1|^2 + |z_2|^2 = 1$，即得结论。$square$
