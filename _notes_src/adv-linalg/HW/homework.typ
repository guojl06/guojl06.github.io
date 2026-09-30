#import "../../module/myutils.typ":*

#show:conf

= 高等线性代数选讲作业 郭嘉乐 2025013332

#outline()

== HW 2 #datetime(day:5,month:4,year:2026).display()

=== 1.
充分性：
*已知* $A^H A=||A||^2$。
$
||A vct(x)|| = ||A^H vct(x)|| \ 
=> ||A vct(x)||^2 = ||A^H vct(x)||^2 \
=> (A vct(x))^H A vct(x) = (A^H vct(x))^H A^H vct(x) \
=> vct(x)^H A^H A vct(x) = vct(x)^H A A^H vct(x) \
=> A A^H = A^H A
$

必要性：
$
  A A^H = A^H A \
  => vct(x)^H A^H A vct(x) = vct(x)^H A A^H vct(x) \
  => (A vct(x))^H A vct(x) = (A^H vct(x))^H A^H vct(x)
$

*已知* $A^H A=||A||^2$，则 $||A vct(x)||^2=||A^H vct(x)||^2 => ||A vct(x)|| = ||A^H vct(x)||$

Q.E.D.

=== 2.

由于 $A$ 是正规矩阵，满足 $A A^H = A^H A$。对于任意向量 $vct(x)$，
$||A vct(x)|| = ||A^H vct(x)||$

取 $V$ 的一组标准正交基 $vct(u_1), dots, vct(u_k)$，并将其扩充为 $CC^n$ 的标准正交基 $vct(u_1), dots, vct(u_n)$。在此基下，$A$ 具有分块形式：
$A = mat(A_11, A_12; 0, A_22)$
其中 $A_11$ 是 $k times k$ 矩阵。由于 $V$ 是 $A$ 的不变子空间，左下角块为 $0$。

考虑前 $k$ 个基向量作用后的模长平方和：
$sum_(i=1)^k ||A vct(u_i)||^2 = sum_(i=1)^k ||A^H vct(u_i)||^2$

左侧：$A vct(u_i)$ 的结果仅由 $A$ 的前 $k$ 列决定，其平方和等于左侧两块的元素模长平方和之和，即 $||A_11||^2 + 0 = ||A_11||^2$。

右侧：$A^H$ 的矩阵表示为 $mat(A_11^H, 0; A_12^H, A_22^H)$。前 $k$ 个基向量 $vct(u_i)$ 对应 $A^H$ 的前 $k$ 列，其模长平方和等于 $||A_11^H||^2 + ||A_12^H||^2$。

利用 $||A_11|| = ||A_11^H||$，代入等式可得：
$||A_11||^2 = ||A_11||^2 + ||A_12||^2$
由此推出 $||A_12||^2 = 0$，即 $A_12 = 0$。

因此 $A = mat(A_11, 0; 0, A_22)$ 是分块对角矩阵，其伴随矩阵 $A^H = mat(A_11^H, 0; 0, A_22^H)$ 也是分块对角矩阵。
这说明 $A^H$ 作用在 $V$ 中的向量上时，结果仍在 $V$ 中。证毕。
=== 3. \*\*


=== 4.

==== $A = mat(1, 2; -2, 1)$
特征值为 $lambda = 1 plus.minus 2i$。
- *特征向量：* 对应 $lambda_1 = 1+2i$，解 $(A - (1+2i)I) vct(u_1) = 0$ 得 $vct(u_1) = 1/sqrt(2) mat(1; i)$。
- $U = 1/sqrt(2) mat(1, i; i, 1)$。
-  $R = U^H A U = mat(1+2i, 4i; 0, 1-2i)$。
- $A = (1/sqrt(2) mat(1, i; i, 1)) mat(1+2i, 4i; 0, 1-2i) (1/sqrt(2) mat(1, -i; -i, 1))$。

==== $A = mat(2, 1, 1; -1, 1, 2; 1, -1, -2)$
特征值为 $lambda = 2, 0, -1$。
- $U = mat(1/sqrt(3), 1/sqrt(2), 1/sqrt(6); 1/sqrt(3), -1/sqrt(2), 1/sqrt(6); -1/sqrt(3), 0, 2/sqrt(6))$。
-  $R = mat(2, 0, 0; 0, 0, 0; 0, 0, -1)$。
-  $A = U mat(2, 0, 0; 0, 0, 0; 0, 0, -1) U^H$。

 $A = mat(1, i, 0; 0, 1, 1; i, 0, 1)$
特征值为 $lambda_1 = 0, lambda_2 = 1.5 - i sqrt(3)/2, lambda_3 = 1.5 + i sqrt(3)/2$。
- $U = mat(1/sqrt(3), i/sqrt(2), 1/sqrt(6); i/sqrt(3), 1/sqrt(2), -i/sqrt(6); -i/sqrt(3), 0, 2/sqrt(6))$。
- $R = mat(0, i sqrt(2), 1/sqrt(2); 0, 1.5 - i sqrt(3)/2, -0.5 - i sqrt(3)/2; 0, 0, 1.5 + i sqrt(3)/2)$。
$A = U R U^H$
=== 5.

$M_1 = mat(1, 1, 0, 0; 0, 1, 1, 0; 0, 0, 1, 1; 0, 0, 0, 1)$
- *特征多项式：* $f(lambda) = (lambda - 1)^4$。
- *最小多项式：* 这是一个完整的 $4$ 阶 Jordan 块 $J_4(1)$， $m(lambda) = (lambda - 1)^4$。

$M_2 = mat(1, 1, 0, 0; 0, 1, 1, 0; 0, 0, 1, 0; 0, 0, 0, 1)$
- 包含一个 $J_3(1)$ 和一个 $J_1(1)$。
- *特征多项式：* $f(lambda) = (lambda - 1)^4$。
- *最小多项式：* 取各块阶数的最大值，即 $3$ 阶，故 $m(lambda) = (lambda - 1)^3$。

$M_3 = mat(1, 1, 0, 0; 0, 1, 0, 0; 0, 0, 1, 0; 0, 0, 1, 1)$
-  左上角 $2 times 2$ 块 $B_1 = mat(1, 1; 0, 1)$ 是标准 $J_2(1)$；右下角 $2 times 2$ 块 $B_2 = mat(1, 0; 1, 1)$，虽然不是直接的 Jordan 块，但是可以通过行列变换在 $P$ 中操作实现转换。

 $f(lambda) = (lambda - 1)^4$。
- *最小多项式：* $m(lambda) = "lcm"((lambda - 1)^2, (lambda - 1)^2) = (lambda - 1)^2$。

== 第七周作业 #datetime(day:19,month:4,year:2026).display()

=== 1.
