#import "../module/myutils.typ":*
#show:conf

#outline()

= 〇 机械运动
== 一、运动学的基础概念 #datetime(day:4,month:3,year:2026).display()
=== (1) Displacement, speed, acceleration, velocity
average speed: $ overline(s)= frac("total distance",Delta t)$

average velocity: $ overline(v)= frac(Delta x,Delta t)$

velocity: $v=lim_(Delta t -> 0) frac(Delta x,Delta t)= frac(\dx , \dt)$

acceleration: $a=lim_(Delta t ->0) frac(Delta v,Delta t)= frac(\dv , \dt)=frac(d^2x,\dt^2)$

$integral_(v_0)^v \dv=integral_(t_0)^t a(t)\dt => v=v_0 +integral_(t_0)^t a(t)\dt$

$integral_(x_0)^x \dx=integral_(t_0)^t v(t)\dt => a(x-x_0)=integral_(v_0)^v v(t)\dv =>v^2-v_0^2=2a(x-x_0)$

In 3D World,we can also say that-- 三个分量决定一切！导数也是三个导分量组成的！举个例子：$arrow(a)=frac(d^2 x,d t^2)arrow(i)+frac(d^2 y,d t^2)arrow(j)$

Something interesting: $|arrow(v)|=frac(\ds,\dt)$

==== 1. Free Fall & Throwing
$
  v_y=v_(0y) - \gt \
  Delta t=v_(0y)/g \
  y=1/2 \gt^2=v_(0y)^2 / (2g)\
  "For throwing: "T=2 sqrt((2h)/g)
$

==== 2. Circular

$
  theta = omega t \
  omega = (d theta) / (d t) \
  "("arrow(omega)": angular velocity)" \
  arrow(v)=R cos(omega t) arrow(i)+R sin(omega t) arrow(j) \
  arrow(v)=(d r)/(d t)=-omega R sin(omega t) arrow(i)+omega R cos(omega t) arrow(j) \
  |arrow(v)|=omega R \
  "Centripetal acceleration: "arrow(a)=-omega^2 R cos(omega t) arrow(i)-omega^2 R sin(omega t) arrow(j) \
  |arrow(a)|=omega ^2 R
$

==== 3. Polar coordinate
$
  arrow(e_r)=cos theta arrow(i)+ sin theta arrow(j) \ 
  arrow(e_theta)=-sin theta arrow(i) + cos theta arrow(j) \ 
  frac(d arrow(e_r),d theta)=arrow(e_theta) \
  frac(d arrow(e_theta),d theta)=-arrow(e_r) \
  arrow(r)=r arrow(e_r) \
  frac(d r,d t) = frac(d r,d t)arrow(e_r)+r frac(d r,d arrow(e_r))=frac(d r,d t)arrow(e_r)+arrow(w)r arrow(e_theta) \
  arrow(a)=frac(d arrow(v),d t)=d/(d t)(frac(d r,d t)arrow(e_r)+r frac(d r,d arrow(e_r)))="(after a long process) " ((d^2 r)/(d t^2)-omega^2 r)arrow(e_r)+(r (d w)/(d t)+2 omega (d r)/(d t))arrow(e_theta)
$

Review #datetime(day:9,month:3,year:2026).display()

$Delta vct(r) != Delta |vct(r)| = Delta r \ |dif vct(r)|=dif s$

划船速度分解问题的真实严谨解法：

$x^2+y^2=r^2$，求导，
$2x dif x + 2y dif  y = 2 r dif r$，由于竖直方向没有速度，所以 $dif y=0$，所以 $dif r = (x/r) dif x$，所以划船的速度是 $vct(r)= (x/r) vct(x)$，即三角函数：$dfrac(x,t)=v_0 / (sin theta)$

还有奇怪的合成分解向量的求导：

$vct(r_(P O))=vct(r_(P O^'))+vct(r_(O O^'))$，求导后 $dfrac(vct(r_(P O)),t)=dfrac(( vct(r_(P O^'))),t)+dfrac((vct(r_(O O^'))),t)$，目前在 Translatimal 平动体系讨论。

纯滚动：
当最底部的点与地面接触时，$- omega R + v_0 = v_P= 0$，所以 $v_0 = omega R$。在并非顶点的时候，则是分量运算，比如说把最低点半径、当前位置半径的夹角叫做 $theta$，则 $v_P = 2 v_0 sin (theta/2)$。\*需要补图片。

=== (2) Newton's Laws
==== 1. Newton's First Law & Second Law
$vct(F)=0 => vct(v)="const" or vct(v)=0$

*Only useful in inertial (reference) frames 惯性参考系*

那么 non-inertial frame 怎么办？

举例：线性阻力的下落过程。对于一个物体自由落体，一个物体向上抛出，分别如下：

- for free fall:

$m g- alpha m v_1=m dfrac(v_1,t)$

Then $integral_0^t dif t= integral_0^(v_1) frac(dif v_1,g - alpha v_1)$, and $- alpha t= ln(g - alpha v_1) - ln(g) => v_1(t)=g/ alpha (1- e^(- alpha t))$,我的天哪神秘的积分！

- for throwing:

$m g - alpha m v_2 = m dfrac( v_2,  t) \ => integral_0^t dif t=integral_(-v_0)^(v_2) frac(dif v_2,g - alpha v_2) \ => 
v_2(t)=g / alpha - (g / alpha + v_0) e^(- alpha t)
$

把这两个再混合到一起：
$integral_0^(t_0) v_1(t) dif t=h+ integral_0^t v_2(t_0) dif t \
 => integral_0^(t_0) (v_1(t)-v_2(t)) dif t=h \
 => integral_0^(t_0) (g/alpha (1-e^(-alpha t))- (g/alpha - (g/alpha + v_0) e^(-alpha t))) dif t=h \
 => integral_0^(t_0) v_0 e^(-alpha t) dif t=h$

 ==== 2. Non-inertial frame
$vct(a_(O^'))+vct(a^')=vct(a)$

So $vct(a^')=vct(a)-vct(a_(O^'))$，其中 $vct(a_(O^'))$ 是非惯性参考系的加速度。同理，$vct(F)-m vct(a_(O^'))=m vct(a^')$

本质是为了减小运算难度。

比如在上面的例子，加入惯性力竖直向上的 $m g$， 则 $m g + alpha m vct(v_2^') #text(fill:blue,$- m g$) = m dfrac(v_2^', t) \
=> v_2^'=-v_0 e^(-alpha t) \
=> h = integral_0^(t_0) v_0 e^(-alpha t) dif t$

答案居然一样！因为我们在非惯性参考系中引入了一个等效的力来抵消非惯性参考系的加速度，所以最终的结果与在惯性参考系中计算得到的结果是相同的。这提醒我们，在非惯性参考系中引入惯性力是为了简化计算，但最终的物理结果应该与在惯性参考系中得到的结果一致。

举例：潮汐力

- 近日侧：$F_A=(G M_s m)/(R - r)^2-(G M_s m)/R^2 approx 2(G M_s m)/(R^3) r$，方向朝向太阳，向外拉伸。
- 远日侧：$F_B=(G M_s m)/(R + r)^2-(G M_s m)/R^2 approx - 2(G M_s m)/(R^3) r$，方向背向太阳，同样向外拉伸。
- 侧面，距离太太阳 $sqrt(R^2+r^2)$：引力在 x 方向分量和惯性力在 x 方向分量几乎相等，所以没有拉伸。在 y 方向上，$F_(-y)=-(G M_s m)/R^3 r$，向内压缩，系数恰好是近日远日点的一半。

我们又来讨论 Rotation 了。Rotation 也有“非惯性系”。考虑一个盘子，有固有角速度 $omega$，圆心处有一个物体径向射出，速度为 $v_0$。

我们先假设一个物体在最简单的情况：只是站在圆盘上，以 $v$ 的速度往前走

则 $T=m v^2/r = m (v^'+omega r)^2 /r = m v^'^2 / r +2m v ^' omega + m omega^2 r$，这些东西分别叫做：非惯性系内向心力、科里奥利力、离心力。

科里奥利力是一个用来解释为什么你在参考系里像“后偏/前压”的力。当你从中心向边缘走的时候，你感受到的力是向后的，当你从边缘向中心走的时候，你感受到的力是向前的。这个力的大小取决于你的速度、角速度和距离。*方向始终由* $omega  times v$ *决定！*

一个典型的运用：傅科摆。

=== (3) Momentum
==== 1. Center of Mass
$vct(r_c)=(sum_i m_i vct(r_i)) / (sum _i m_i)$ or for uniform: $vct(r_c)=(integral rho vct(r) dif V) / (integral rho dif V)$

For each particle, 
$ m_i vct(a)_i = vct(F)_i + sum_(j != i) vct(f)_(i j) $

$ sum_i m_i vct(a)_i = sum_i vct(F)_i + sum_i sum_(j != i) vct(f)_(i j) $

*内力抵消！！！*

$ sum_i m_i vct(a)_i = sum_i vct(F)_i $

$ M vct(a)_C = sum_i vct(F)_i $

*(Euler's 1st Law)*

==== 2. Momentum
$vct(p)=m vct(v)$

$vct(F)=m dfrac(vct(v),t)=dfrac(m vct(v),t)=dfrac(vct(p),t) \
=> vct(F) dif t= dif vct(p),Delta vct(p)=integral vct(F) dif t,(sum vct(F_i))dif t= dif vct(p)$

$vct(P)=sum_i vct(p)_i = sum_i m_i vct(v)_i = (sum_i m_i) dfrac(vct(r_c),t)=M vct(v_c)$

推导出来：动量守恒定律！

$sum_i vct(F)_i = 0 => sum_i vct(p)_i = "const" $

朝花夕拾：火箭起飞问题

原始的完整式子：$M v=(M-dif m)(v + dif v) + dif m(-u+v)$，其中 $dif m$ 是火箭发射出去的燃料质量，$u$ 是燃料的喷射速度，$v$ 是火箭的速度，$M$ 是火箭的总质量。为什么两个都有 $ dif v$ 呢？这是因为火箭发射燃料时，燃料和火箭一起运动，所以火箭的速度和燃料的速度是相同的。

$M dif v=-u dif M$

$integral_0^v dif v = -u integral_(M_0)^(M_f) (dif M) / M \
=> v = -u ln(M_f/M_0)=u ln (M_0/M_f) \
$

==== 3. Angular Momentum

旋转不满足交换律。*角速度可以被定义为向量，方向沿轴（右手定则）*。

$vct(omega)=dfrac(theta,t)vct(e)$

举例：开普勒第二定律，即面积定律。面积定律指出，行星绕太阳运动的轨道面积与时间成正比。这可以通过角动量守恒定律来解释。

$
S= ((vct(r) times vct(v)) Delta t) / 2 = L/(2m) Delta t ;vct(L)=vct(r) times m vct(v)=vct(r) times vct(p) \
=> |vct(L)|=r m omega r=m omega r^2 "(only in circular motion)" \
$

另一个例子：圆锥摆

$
|vct(v)|= omega l sin theta \
|vct(L_O)|= l sin theta m omega l sin theta = m omega l^2 sin^2 theta "以底盘原点为中，此时角动量唯一且始终竖直向上，守恒"\

|vct(L_(O^'))|= l m omega l sin theta = m omega l^2 sin theta \ "以悬挂点为中心，角动量垂直于线，分解后竖直分量守恒，水平分量大小不变、方向始终背离圆心"\

"因此我们可以讨论（微元法/神秘分析）：" (|Delta vct(L_(O^'))|) /( Delta t ) = |Delta vct(L_(O^'))| cos theta omega = |vct(togrog)| = l m g sin theta = ... "反正最后发现本质相等"  \

"至于是怎么发现的：有一个很神秘的点请你注意到，那就是他妈的力矩的计算式子，叉乘的魅力这一块"\

dfrac(vct(L),t) = dfrac((vct(r) times vct(p)),t)= vct(r) times dfrac(vct(p),t)+vct(p) times dfrac(vct(r),t) = vct(r) times vct(F)  = vct(togrog) "力矩"
\

$

这个时候对于这个神秘的圆锥摆，我们很容易发现：（受力分析得到两力关系什么的）

$
cos theta = g/(omega^2 l) => theta = arccos(g/(omega^2 l)) \
$

*现在告诉你什么是角动量守恒：合力矩为零，角动量守恒。*

==== 4. System of Particles

有一堆神秘且漫长的消除、计算等等等等各种神秘的过程，最后得到一个结论：*内力矩相互抵消，只看外力矩。*

即：$sum_i vct(r_i) times vct(F_i) = dfrac((sum_i vct(L_i)),t)$

另一个例子：一个小球在正中间撞上了一根轻杆。

===== 定轴转动碰撞实验：角动量守恒与线动量丢失

在有固定转轴 $O$ 的系统中，当质量为 $m_2$ 的质点以 $v_0$ 撞击质量为 $m_1$ 的单摆中点时：

*角动量守恒 (Conservation of Angular Momentum)*

由于支点 $O$ 的瞬时冲力通过轴心，对 $O$ 点的力矩 $tau_O = 0$，故系统角动量守恒。
设碰撞后系统的共同角速度为 $omega$，则有：
$ m_2 v_0 l/2 = (m_2 (l/2)^2 + m_1 l^2) omega $

解得碰撞后的角速度：
$ omega = (2 m_2 v_0) / ((m_2 + 4 m_1) l) $

*线动量分析 (Linear Momentum Analysis)*

我们对比碰撞前后的系统总线动量 $P$：
- *碰撞前*：$P_"before" = m_2 v_0$
- *碰撞后*：
$ P_"after" &= m_2 v_(m_2) + m_1 v_(m_1) \
            &= m_2 (omega l/2) + m_1 (omega l) \
            &= (m_2/2 + m_1) l omega $

将 $omega$ 的表达式代入上式：
$ P_"after" &= (m_2/2 + m_1) l dot (2 m_2 v_0) / ((m_2 + 4 m_1) l) \
            &= (m_2 + 2 m_1) / (m_2 + 4 m_1) m_2 v_0 $

*结论*：

由于系数满足：
$ (m_2 + 2 m_1) / (m_2 + 4 m_1) < 1 $

故得出结论：
$ P_"after" < P_"before" $

*结论分析*：虽然系统的合外力矩为零导致角动量守恒，但由于支点 $O$ 在碰撞瞬间产生了向后的瞬时冲量 $vct(I)_O$，该外力导致了系统线动量的丢失。

===== 另一个例子：太典，跷跷板

$togrog=m_1 g l cos theta - m_2 g l cos theta = dif / (dif t) (-m_1 omega l^2-m_2 omega l^2) \
=> -(m_1+m_2) omega l^2 dfrac(omega,t) dif theta= (m_1-m_2) g l cos theta dif theta \
=> integral_(omega_0)^0 (m_1+m_2) l^2 omega dif omega = integral_(theta_0)^(- theta_0) (m_1-m_2) g l dif (sin theta)  \
=> omega_0 = 2/l sqrt(((m_1-m_2)g h) / (m_1+m_2))
$

哥们，神了。在质心系里面有奇妙的现象：

$
vct(r_c)=(sum_i m_i vct(r_i)) / (sum _i m_i) \ 
=> vct(r_i^')=vct(r_i)-vct(r_c) \
sum_i m_i vct(r_i^')=sum_i m_i vct(r_i) - sum_i m_i vct(r_c)  =0 \

"导数也为" 0, "所以质心系里面动量守恒" \
sum_i vct(F_i) =dfrac(vct(P_c),t)
$

以及神秘的质心系里的分配。假设两个质量快一上一下中间有根绳子。假设它们都向水平方向飞过去，那么获取质心：
$
v_c=(m_1 v_1+m_2 v_2) / (m_1+m_2) \
l_1=(m_2 l_2) / (m_1+m_2) \
l_2=(m_1 l_1) / (m_1+m_2) \
$

假设它们不同方向飞行：
#let vct(x) = $bold(arrow(#x))$

这部分内容推导了双质心系统在质心参考系（COM-frame）下的动力学描述及张力 $T$ 的求解。

首先定义质心速度 $v_c$：
$ v_c = (m_1 v_1 + m_2 v_2) / (m_1 + m_2) $

在质心系中，各质点的相对速度 $v_i'$ 为：
$ v_1' = v_1 - v_c = v_1 - (m_1 v_1 + m_2 v_2) / (m_1 + m_2) = - m_2 / (m_1 + m_2) (v_2 - v_1) $
$ v_2' = v_2 - v_c = v_2 - (m_1 v_1 + m_2 v_2) / (m_1 + m_2) = m_1 / (m_1 + m_2) (v_2 - v_1) $

由此可以定义系统的转动角速度 $omega$。由于 $m_1$ 和 $m_2$ 绕质心转动的半径分别为 $r_1 = m_2 / (m_1 + m_2) l$ 和 $r_2 = m_1 / (m_1 + m_2) l$，则有：
$ omega = (|v_1'|) / r_1 = (|v_2'|) / r_2 = (v_2 - v_1) / l $

最后，利用向心力公式求解绳子或杆的张力 $T$：
$ T = m_1 omega^2 r_1 = m_1 omega^2 (m_2 / (m_1 + m_2) l) $
$ T = m_2 omega^2 r_2 = m_2 omega^2 (m_1 / (m_1 + m_2) l) $

整理可得：
$ T = (m_1 m_2) / (m_1 + m_2) omega^2 l $

其中 $(m_1 m_2) / (m_1 + m_2)$ 即为该系统的折合质量 (Reduced Mass)。

不是哥们，真神了！为什么到底为什么这么强？！

同样的道理，你再看看角动量呢？！

$
vct(L_i)=vct(r_i) times m_i vct(v_i) \
sum_i vct(L_i) = vct(L_c) +sum_i vct(L_i^') "COM 的神秘力量！！！" \
= vct(r_c) times sum_i m_i vct(v_i) + sum_i vct(r_i^') times m_i vct(v_i^') \
"然后！！！"
\

vct(r_i)=vct(r_i^')+vct(r_c) \
sum_i vct(L_i) = sum_i vct(r_i) times m_i dfrac(vct(r_i),t) \
= sum_i (vct(r_c)+vct(r_i^')) times m_i (dfrac(vct(r_i^'),t)+dfrac(vct(r_c),t))  \

=  "消元之后" vct(r_c) times sum_i m_i vct(v_c)+ sum_i vct(r_i^') times m_i dfrac(vct(r_i^'),t) \
$

还有一个神秘的式子，听见你说：
$
dfrac(sum_i vct(L_i),t)=sum_i vct(togrog_i) \
dfrac(sum_i vct(L_i^'),t)=sum_i vct(r_i^') times vct(F_i) \
= "消元消元大消元" sum_i (vct(r_i)-vct(r_c)) times vct(F_i) \
$

== 二、 Energy 

- $1/2 m v^2$ *Kenetic Energy*
  - How to get it?
  $m (dif^2 x)/(dif t^2)=F(x) 
  \ m (dif^2 x)/(dif t^2) dif x = F(x) dif x \
  \ m dfrac(v,t) dif x = F(x) dif x
  \ => integral_0^t m v dif v = integral_0^t F(x) dif x \ 
  => 1/2 m v^2 - 1/2 m v_0^2 = integral_(x_0)^(x_t) F(x) dif x \ $
- $integral_(x_0)^(x_t) F(x) dif x= W_(x(t) x_0)=W_0^t$ *Work* on the object by the force

同理，对弹簧进行积分，得到：$1/2 k x^2$ *Potential Energy*

在*三维世界*里面，
$
  m dfrac(vct(v),t) = vct(F)(vct(r)) \ 
  m dfrac(vct(v),t) dif vct(r) = vct(F)(vct(r)) dif vct(r) \
  integral m vct(v) dif vct(v) = integral vct(F)(vct(r)) dif vct(r) \
  = integral dif(1/2 m v^2) = integral vct(F)(vct(r)) dif vct(r) = 1/2 m v^2 - 1/2 m v_0^2 = Delta K
$



=== 动能定理 (Work-Energy Theorem)
合外力做的功等于物体动能的增量：
$ W = integral vct(F) dot d vct(r) = Delta K = 1/2 m v^2 - 1/2 m v_0^2 $
*物理意义 (Significance)*：建立了力场空间分布与物体运动状态的联系。

==== 1. 基础保守力实例 (Basic Conservative Forces)

- *重力 (Gravity)*：$F(y) = -m g$。
  $ W_G = integral_(h_0)^h (-m g) thin dif y = -m g h + m g h_0 $
- *弹性力 (Elastic Force)*：$F(x) = -k x$。
  $ W_s = integral_(x_0)^x (-k x) thin dif x = -1/2 k x^2 + 1/2 k x_0^2 $

==== 2. 有心力的路径无关性证明 (Central Force Path Independence)

设*有心力* (Central Force) 为 $vct(F)(vct(r)) = f(r) vct(e)_r$。在极坐标中，元位移分解为径向和切向：
$ dif vct(r) = (dif r) vct(e)_r + r d theta vct(e)_theta $


计算元功 (Infinitesimal Work)：
$ dif W = vct(F) dot dif vct(r) = f(r) dif r $
*推论 (Conclusion)*：切向分量 $r d theta$ 对功无贡献，因此功的大小只取决于始末径向距离 $r$，即*有心力必为保守力*。

==== 3. 引力势能模型 (Gravitational Potential Energy Model)

针对*平方反比力*(Inverse-Square Force)，令 $f(r) = -A/r^2$（如引力，$A=G M m$）：
$ W = integral_(r_0)^r (-A / r^2) d r = [A / r]_(r_0)^r = A / r - A / r_0 $

=== 势能函数 (Potential Energy Function)
物理学定义势能变化量为功的负值 $Delta U = -W$。若取无穷远处为零势能参考点 ($r_0 arrow.r oo$)：
$ U(r) = - A / r $


*图像特性 (Graph Characteristics)*：
  1. *负值 (Negative Value)*：代表引力束缚态 (Bound State)。
  2. *渐近线 (Asymptote)*：当 $r arrow.r 0$ 时，$U(r) arrow.r -oo$；当 $r arrow.r oo$ 时，$U(r) arrow.r 0$。
  3. *斜率 (Slope)*：曲线的斜率 $d U / d r$ 即对应于力的大小（负梯度）。

// 定义向量和梯度算符
#let vct(x) = $arrow(bold(#x))$
#let grad = $nabla$

#text(fill: rgb("#1a4a7c"), weight: "bold")[核心概念：势能变化与梯度力场 (Potential Energy & Gradient Force Field)]

---

==== 1. 势能的基本定义 (Definition of Potential Energy)

势能的变化量 $Delta U$ 定义为保守力做功的负值：
$ Delta U = -W = - integral_(vct(r)_0)^(vct(r)) vct(F) dot dif vct(r) $

- *重力情况*：$Delta U = m g h - m g h_0$
- *弹力情况*：$Delta U = 1/2 k x^2 - 1/2 k x_0^2$

==== 2. 力与势能的微分关系 (Differential Relationship)

在微小位移 $Delta x$ 下，功可以近似为 $W approx F(x) Delta x$，因此：
$ Delta U approx -F(x) Delta x $

取极限 $Delta x arrow.r 0$，得到一维下的基本关系：
$ (dif U) / (dif x) = -F(x) quad arrow.r.double quad F(x) = - (dif U) / (dif x) $
*物理直观*：力总是指向势能降低最快的方向。

==== 3. 梯度算符与高维推广 (The Gradient Operator $nabla$)

在三维空间中，力是一个矢量，而势能是一个标量场。板书上的“倒三角”符号 $nabla$（读作 Nabla 或 Del）代表*梯度算符*：

$ vct(F) = -nabla U $


其展开形式为：
$ vct(F) = -( (partial U) / (partial x) vct(i) + (partial U) / (partial y) vct(j) + (partial U) / (partial z) vct(k) ) $

==== 4. 图像分析：等势面与力线 (Equipotential Lines & Force Lines)

观察老师在黑板右下角画的示意图：
- *曲线（等势线）*：代表势能相等的轨迹（类似地图上的等高线）。
- *带箭头的直线（力线）*：代表力 $vct(F)$ 的方向。
- *关键特性*：
  1. *正交性*：力线（梯度方向）始终与等势面（$U$ 为常数的面）*垂直*。
  2. *方向性*：由于公式中有负号，力的方向指向势能*减小*的方向（从高处指向低处）。

---

#text(fill: rgb("#d32f2f"), weight: "bold")[物理专题：非保守力做功与广义能量守恒定律]

---
=== 机械能守恒与能量守恒
==== 1. 非保守力：摩擦力的路径相关性 (Non-conservative Force)

与重力或引力不同，*非保守力*（如摩擦力）做功的大小取决于物体运动的具体路径 (*path dependent*)。

* 物理特性 (Characteristics)：
  摩擦力 $vct(f)$ 的方向始终与瞬时位移 $d vct(r)$ 相反，即 $vct(f) dot d vct(r) = -f d s$。
* 数学对比 (Comparison)：
  如图所示，从起点到终点有两条路径：$s_1$（直线）和 $s_2$（曲线）。
  - 直线功：$W_(f 1) = -f s_1$
  - 曲线功：$W_(f 2) = -f s_2$
  由于 $s_2 > s_1$，故 $|W_(f 2)| > |W_(f 1)|$。这说明非保守力无法定义唯一的势能函数。


==== 2. 机械能的损耗与转化 (Energy Dissipation)

当系统中存在非保守力时，机械能（动能 $K$ + 势能 $U$）不再守恒。非保守力所做的功 $W_(n c)$ 等于系统机械能的变化量：
$ W_(n c) = Delta (K + U) $

*物理直观* (Intuition)：
  摩擦力通常做负功，导致系统的机械能“流失”。这种流失并不是能量消失了，而是转化为了微观层面的分子动能，即*热能* (Thermal Energy)。

==== 3. 广义能量守恒定律 (Law of Energy Conservation)

板书最后一节给出了能量守恒的终极形式。通过引入热能项 $E_(t h)$，我们可以描述一个封闭系统的总能量守恒：

$ K + U + E_(t h) = "const." $


*符号说明* (Nomenclature)：
  - $K$: *Kinetic Energy* (动能)
  - $U$: *Potential Energy* (势能)
  - $E_(t h)$: *Thermal Energy* (热能/内能)

*物理意义* (Physical Significance)：
  这是比机械能守恒更普适的规律。它表明在孤立系统中，能量既不会凭空产生，也不会凭空消失，只能从一种形式转化为另一种形式（例如通过摩擦将机械能转化为热能）。

---

#text(fill: rgb("#1a4a7c"), size: 1.2em, weight: "bold")[专题：典型动力学系统的能量与动量分析]

---
=== 常见模型
==== 1. 变摆长单摆模型 (Variable Length Pendulum)
*场景*：摆球在运动过程中摆长由 $L$ 突变为 $l$（如线被钉子挡住）。

* *核心特征*：在摆长缩短的瞬间，系统满足*角动量守恒*。
  $ m v_0 L = m v l quad arrow.r.double quad v = v_0 L / l $
* *能量转化*：碰撞后（或缩短后）满足机械能守恒。设最高点高度为 $h = L(1-cos theta)$。
  - 长摆：$1/2 m v_0^2 = m g L (1 - cos theta)$
  - 短摆：$1/2 m v^2 = m g l (1 - cos theta')$
*比例结论*：
  $ (1 - cos theta') / (1 - cos theta) = L^3 / l^3 $
  由于 $L > l$，推得 $theta' > theta$。即*摆长越短，摆起角度越大*。



==== 2. 滑块-滑梯碰撞爬升模型 (Block-Slide Interaction)
*场景*：小物块 $m$ 以 $v_0$ 撞击并爬上水平面上静止的滑梯 $M$。

* *水平动量守恒*：在最高点时，二者具有共同水平速度 $v_c$。
  $ m v_0 = (m + M) v_c quad arrow.r.double quad v_c = m / (m + M) v_0 $
* *机械能守恒*：系统初动能转化为系统余下的动能与重力势能。
  $ 1/2 m v_0^2 = 1/2 (m + M) v_c^2 + m g h $
* *最大高度表达式*：
  $ h = M / (m + M) dot v_0^2 / (2g) $
* *结论*：上升高度受质量分配系数 $M / (m + M)$ 调制。



==== 3. 最低点完全非弹性碰撞模型 (Inelastic Collision at Bottom)
*场景*：单摆 $m$ 在最低点与静止物块 $M$ 碰撞并*结合为整体*后继续摆动。

* *动量守恒 (碰撞瞬间)*：
  $ m v_0 = (m + M) v' quad arrow.r.double quad v' = m / (m + M) v_0 $
* *机械能变化 (爬升阶段)*：
  结合体以速度 $v'$ 开始爬升，满足 $(m + M) g h' = 1/2 (m + M) v'^2$。
* *高度对比*：
  设不碰撞时的爬升高度为 $h_0 = v_0^2 / (2g)$，则碰撞后的高度为：
  $ h' = v'^2 / (2g) = ( m / (m + M) )^2 h_0 $
* *结论*：由于速度在碰撞中因动量分配而大幅减小，且机械能有耗散，*碰撞结合后爬升的高度明显更低* ($h' < h_0$)。



---

==== 总结与对比分析 (Comparative Summary)

#table(
  columns: (1fr, 1.2fr, 1.2fr, 1.6fr),
  inset: 10pt,
  align: horizon,
  [*模型 (Model)*], [*第一守恒准则*], [*第二守恒准则*], [*核心物理结果*],
  [变摆长单摆], [角动量守恒 \ $m v_0 L = m v l$], [机械能守恒 \ $Delta (K + U) = 0$], [$L arrow.b arrow.r.double v arrow.t$ \ $theta' > theta$ (摆角增大)],
  [滑块-滑梯], [水平动量守恒 \ $m v_0 = (m+M)v_c$], [机械能守恒 \ $Delta (K + U) = 0$], [$h = M / (m + M) dot v_0^2 / (2g)$ \ (能量重新分配)],
  [碰撞结合], [动量守恒 \ $m v_0 = (m+M)v'$], [机械能守恒 \ (仅限碰撞后爬升)], [$h' = (m / (m+M))^2 h_0$ \ (速度阶跃减小，高度降低)]
)

*重点提醒*：
1. 在“变摆长”中，速度增大是因为半径减小；在“碰撞结合”中，速度减小是因为总质量增大。
2. 注意区分“内力做功”：滑块模型中 $m$ 与 $M$ 间的法向力对系统整体不做功，但完全非弹性碰撞中内部有能量耗散。

==== 再看变摆长模型分析 #datetime(day:30,month:3,year:2026).display()

===== 核心守恒量
在忽略空气阻力且拉力过轴心的条件下，系统满足 *角动量守恒*：
$ m v_2 l = m v_1 L $

由于 $l < L$，推导出 $v_2 > v_1$。

===== 动力学补充
在该过程中，向心力（拉力）的径向分量对质点做功，满足动能定理：
$ W = integral_(L)^(l) vct(F) dot d vct(r) = 1/2 m v_2^2 - 1/2 m v_1^2 $

=== 中心力场动力学分析

==== 1. 场与能量定义
- 矢量力：$ vct(F)(vct(r)) = - (G m M) / r^2 vct(e)_r $
- 势能：$ U(r) = - (G m M) / r $
- 能量守恒：$ 1/2 m vct(v)^2 - (G m M) / r = E_0 $

==== 2. 径向方程推导
利用 $vct(L_0) = vct(r) times m vct(v)$，将速度分解为：
$ vct(v) = (dif r) / (dif t) vct(e)_r + (L_0) / (m r) vct(e)_theta $

代入能量方程，得到黄框标注的核心公式：
$ E_0 = 1/2 m v_r^2 + [ L_0^2 / (m^2 r^2) - (G m M) / r ] $
其中方括号内项标注为 *effective*（有效势能）。

一部分叫做有效势能，一部分叫做有效机械能。

==== 3. 有效势能曲线分析
根据 $E(r)$ 图像：
- $L_0^2 / (m^2 r^2)$ 项：随 $r$ 减小快速上升，起到排斥作用。
- $- (G m M) / r$ 项：吸引作用。
- 综合曲线（黄线）呈现势阱特征。



#image("../Assets/img/202611323213.jpg", width: 350pt)

#image("../Assets/img/2026222.jpeg")
=== 轨道形状的几何判定

==== 1. 能量与轨迹对应关系
根据总能量 $E_0$ 的取值，系统的运动轨迹呈现不同的圆锥曲线特征：
- $E_0 > 0$: *hyperbola* (双曲线)，表现为逃逸轨道。
- $E_0 = 0$: *Parabola* (抛物线)，为临界逃逸轨道。
- $E_0 < 0$: *Ellipse* (椭圆)，为束缚闭合轨道。

==== 2. 图像解析
在 $E(r)$ 图像中：
- 当 $E_0 > 0$ 时（图中蓝色虚线以上），能量线与 $U_"eff"$ 曲线仅有一个交点，即质点只能到达 *最近距离*。
- 当 $E_0 < 0$ 时（图中蓝色虚线以下），能量线与曲线有两个交点，对应椭圆轨道的近日点与远日点。
- 当 $E_0$ 恰好处于势阱最低点时，轨道退化为 *Circle* (圆)。

=== 轨道转折点的定量计算

==== 1. 物理条件
在轨道半径的极值处（近日点或远日点），径向速度满足：
$ (dif r) / (dif t) = 0 $

==== 2. 径向位置方程
将条件代入有效势能公式，整理得到关于 $r$ 的一元二次方程：
$ r^2 + (G m M) / E_0 r - L_0^2 / (2 m E_0) = 0 $

==== 3. 半径解的表达式
利用求根公式，得到转折点半径 $r_0$：
$ r_0 = 1 / 2 [ - (G m M) / E_0 plus.minus sqrt( (G^2 m^2 M^2) / E_0^2 + (2 L_0^2) / (m E_0) ) ] $

- 若 $E_0 < 0$，方程有两个正根，对应椭圆轨道的近日点与远日点。
- 若 $E_0 >= 0$，仅有一个物理意义上的正根，对应抛物线或双曲线的最近点。

=== 轨道转折点与圆轨道的定量计算

==== 1. 长半轴与能量的关系
在 $E_0 < 0$ 的椭圆轨道束缚态下，近日点 $r_"min"$ 与远日点 $r_"max"$ 之和（对应椭圆长轴 $2a$）代数整理结果为（标注 $r_0$）：
$ 2a = r_"max" + r_"min" = - (G m M) / E_0 $
这证实了开普勒第一定律的动力学根源，长半轴 $a$ 仅取决于总能量。

==== 2. 圆轨道的最低能量
在有效势阱的最低点处，系统只能以固定的半径 $r_c$ 做匀速圆周运动，其总能量满足板书原样公式：
$ E_0 = - (G^2 m^3 M^2) / (2 L_0^2) $
此即该角动量状态下的最低可能能量。

==== 3. 物理术语补充
对于非逃逸态轨道，最靠近中心天体的点称为：
- *perigee*：近日点。
- *peri-helion*：近日点（专门指绕太阳轨道）。

=== 轨道方程的积分求解

==== 1. 运动学分量解构
由角动量与能量守恒导出：
$ (dif theta) / (dif t) = L_0 / (m r^2) $
$ (dif r) / (dif t) = sqrt( 2 / m (E_0 - L_0^2 / (2 m r^2) + (G m M) / r) ) $

==== 2. 空间轨迹积分
利用 $ (dif r) / (dif theta) = ((dif r) / (dif t)) / ((dif theta) / (dif t)) $ 消去时间变量，建立 $r$ 与 $theta$ 的积分关系：
$ integral (g(r)) / (f(r)) dif r = integral dif theta $

==== 3. 极坐标轨道解 (圆锥曲线)
轨道方程最终表示为：
$ r = p / (1 + epsilon cos theta) $

其中关键几何参量为：
- *半正焦弦* $p = L_0^2 / (G M m^2)$
- *离心率 (eccentricity)* $epsilon = sqrt( 1 + (2 E_0 L_0^2) / (G^2 M^2 m^3) )$

==== 4. 能量与轨道几何的统一
通过 $epsilon$ 的表达式可知，总能量 $E_0$ 彻底决定了轨道的拓扑形状（椭圆、抛物线或双曲线）。

=== 轨道积分详细步骤

1. *链式法则消元*:
$ (dif r) / (dif theta) = (dif r / dif t) / (dif theta / dif t) $

2. *分离变量形式*:
$ integral dif theta = integral (L_0 / (m r^2)) / (sqrt( 2/m (E_0 - U_"eff"(r)) )) dif r $

3. *换元 $u = 1/r$*:
$ theta = integral - (L_0 / m) / (sqrt( 2/m (E_0 - (L_0^2 u^2) / (2 m^2) + G m M u) )) dif u $

=== 质点系动力学完整总结

==== 1. 质心系基本属性
- 质心运动定理：$ (dif vct(P)_c) / (dif t) = sum vct(F)_i $
- 质心系动量特性：$ sum m_i vct(r)'_i = 0 arrow.r sum vct(p)'_i = 0 $

==== 2. 动能分解 (Koenig 定理)
系统的总动能 $K$ 可分解为质心动能与相对动能：
$ sum K_i = 1/2 M v_c^2 + sum 1/2 m_i v_i prime^2 = K_c + sum K'_i $

==== 3. 功能原理 (Work-Energy Theorem)
系统总动能的增量等于外力功与内力功之和：
$ integral dif (sum_i K_i) = underbrace(integral sum vct(F)_i dot dif vct(r)_i, W_E) + underbrace(integral sum vct(f)_(i j) dot dif vct(r)_i, W_I) $

==== 4. 质心参考系下的功
在 COM frame 中，动能增量同样满足分解关系：
$ sum Delta K_i = sum Delta K'_i + Delta K_c $
其中外力功对应的质心部分：
$ W_E = integral (dif vct(P)_c) / (dif t) dot dif vct(r)_c $

此时还有  $sum_i Delta K_i=sum_i K_i^' +K_c \ sum_i Delta K_i^' = W_E^' +W_I^'$

=== 质点系角动量 (Angular Momentum)

==== 1. 角动量分解公式
系统的总角动量等于质心动量矩与相对质心动量矩之和：
$ sum vct(L)_i = vct(L)_c + sum vct(L)'_i $
其中：
- 质心角动量：$ vct(L)_c = vct(r)_c times M vct(v)_c $
- 相对角动量：$ sum vct(L)'_i = sum (vct(r)'_i times m_i vct(v)'_i) $

==== 2. 质心系角动量定理
相对于质心的总角动量变化率仅由外力矩决定：
$ (dif) / (dif t) (sum vct(L)'_i) = sum vct(tau)'_i $
该式说明，即使质心本身在加速（非惯性系），只要参考点选在质心上，角动量定理的形式依然保持简洁，不需要引入惯性力矩。

=== 两体系统的动能分解 (Koenig 定理特例)

==== 1. 动能构成
两质点系统的总动能可表示为质心动能与相对动能之和：
$ K = K_c + 1/2 mu v_r^2 $

==== 2. 参数定义
- *质心动能*: $K_c = 1/2 (m_1 + m_2) v_c^2$，其中 $v_c$ 为质心速度。
- *折合质量 (Reduced Mass)*:
  $ mu = (m_1 m_2) / (m_1 + m_2) $
- *相对速度*: $vct(v)_r = vct(v)_1 - vct(v)_2$。

==== 3. 物理意义
这一推导允许我们将相互作用的两个天体（如地月系统）简化为一个质量为 $mu$ 的“单体”绕质心旋转的问题，这也是之后解轨道方程的前提。

=== 实例：电荷散射最近距离求解 (修正版)

==== 1. 初始状态设定
- 电荷 1 ($m$): $v_1 = 2 v_0$
- 电荷 2 ($m$): $v_2 = - v_0$
- 相对速度: $v_"rel" = 3 v_0$

==== 2. 相对动能计算
利用折合质量 $mu = m / 2$，初始总相对动能为：
$ sum K'_i = 1/2 mu v_"rel"^2 = 1/2 (m/2) (3 v_0)^2 = 9/4 m v_0^2 $

==== 3. 功能定理求解 $r_"min"$
内力（库仑力）做功的矢量微分形式：
$ W'_I = integral [ (k e^2) / (vct(r_1) - vct(r_2))^2 dif vct(r_1) - (k e^2) / (vct(r_1) - vct(r_2))^2 dif vct(r_2) ] $
积分结果对应电势能变化：
$ W'_I = - (k e^2) / r_"min" $

根据能量守恒：
$ 0 - 9/4 m v_0^2 = - (k e^2) / r_"min" $

最终得到：
$ r_"min" = (4 k e^2) / (9 m v_0^2) $

=== 引力助推 (Gravity Assist) 动力学分析

==== 1. 物理背景
- 探测器质量: $m_s$
- 行星质量: $M_p$ (满足 $M_p >> m_s$)
- 行星公转速度: $vct(v)_p$

==== 2. 质心系下的简化
由于 $M_p$ 巨大，系统的质心几乎与行星中心重合：
$ vct(v)_c approx vct(v)_p $
此时，折合质量 $mu$ 简化为探测器质量 $m_s$：
$ mu = (m_s M_p) / (m_s + M_p) approx m_s $

==== 3. 速度增益推导
设探测器以相对速度 $vct(u)$ 进入行星引力范围，在行星参考系中：
- 进入速度大小: $u + v$
- 甩出速度大小: $u + v$ (动能守恒)

回到太阳参考系（实验室系）：
$ vct(v)_"final" = vct(v)_p + vct(v)_"relative" $
对于 180 度调头的理想情况：
$ v_"final" = v + (u + v) = u + 2v $

==== 4. 能量损失 (Energy Transfer)
探测器获得的动能 $Delta K$ 全部来自于行星动能的减小：
$ Delta K_s = - Delta K_p $
由于行星质量极大，其速度变化 $Delta v_p$ 极其微小，但在能量守恒上体现为行星 "Lose Energy"。


== 三、刚体角动量的

=== 1. 角动量的基本定义
对于由多个质点组成的系统，其对原点 $O$ 的总角动量 $vct(L)$ 定义为各质点动量矩的矢量和：
$ vct(L) = sum_i vct(r)_i times m_i vct(v)_i $

=== 2. $z$ 轴分量的行列式表达
利用矢量叉乘的行列式形式，提取角动量在 $z$ 轴方向的分量 $L_z$：
$ L_z = sum_i |mat(delim: "|", 
  vct(i), vct(j), vct(k); 
  x_i, y_i, z_i; 
  m_i v_(i x), m_i v_(i y), m_i v_(i z))|_z $

展开行列式的 $z$ 轴分量（即 $vct(k)$ 对应项）：
$ L_z = sum_i (m_i v_(i y) x_i - m_i v_(i x) y_i) $

=== 3. 绕定轴转动的运动学约束
设刚体绕 $z$ 轴以角速度 $omega$ 旋转。根据板书左侧的几何关系，质点在 $x-y$ 平面内的速度分量为：
$ v_(i x) = -omega r_(i, perp) sin(theta) = -omega y_i $
$ v_(i y) = omega r_(i, perp) cos(theta) = omega x_i $

其中 $r_(i, perp) = sqrt(x_i^2 + y_i^2)$ 是质点到旋转轴（$z$ 轴）的垂直距离。

=== 4. 转动惯量与最终简化
将上述速度分量代入 $L_z$ 表达式：
$ L_z = sum_i (m_i (omega x_i) x_i - m_i (-omega y_i) y_i) $
$ L_z = (sum_i m_i (x_i^2 + y_i^2)) omega $

对于一个系统，其总转动惯量 $I$ 定义为所有质点对旋转轴的垂直距离平方与质量乘积之和：（积分形式）$integral rho (vct(r)) dif V  r_perp^2$

定义 *转动惯量* 为 $I = sum_i m_i r_(i, perp)^2$，则最终简化为：
$ L_z = I omega $
#image("../Assets/img/20260401_194105.png")


=== 1. 转动定律的推导过程
根据质点系的角动量定理，系统总角动量对时间的变化率等于其所受的合外力矩 $vct(tau)$ (total torque)：
$ (dif sum_i vct(L)_i) / (dif t) = vct(tau) $

=== 2. 定轴转动的投影形式
对于绕固定轴（通常设为 $z$ 轴）旋转的刚体，板书通过向下箭头展示了从矢量方程到标量投影方程的简化：
$ (dif L_z) / (dif t) = tau_z $

=== 3. 结合转动惯量的代换
利用此前推导的 $L_z = I_z omega$ 关系，由于刚体绕定轴转动时 $I_z$ 为常数，可以将其提至微分号外：
$ (dif (I_z omega)) / (dif t) = tau_z $
$ I_z (dif omega) / (dif t) = tau_z $

=== 4. 动力学基本方程
最终得到定轴转动的动力学基本方程（转动定律）：
$ I_z alpha = tau_z $
其中 $alpha = (dif omega) / (dif t)$ 为角加速度。

*物理意义*：该方程建立了外力矩 $tau$ 与角加速度 $alpha$ 之间的线性关系，转动惯量 $I$ 在此扮演了“转动惯性”的角色，类似于平动中的质量 $m$。

=== 7. 定轴转动定律的应用实例：滑轮下落系统
模型描述：质量为 $m$ 的重物通过绳子绕在转动惯量为 $I$、半径为 $R$ 的滑轮上。

==== (1) 动力学方程组的建立
分别对重物（平动）和滑轮（转动）列式：
- *重物方程*：$m g - T = m a$
- *滑轮方程*：$T R = I alpha$
- *约束关系*：$a = R alpha$

==== (2) 加速度 $a$ 的解析解
联立消去张力 $T$ 与角加速度 $alpha$：
$ m g - (I a) / R^2 = m a $
解得系统下落加速度：
$ a = m / (m + I / R^2) g $

==== (3) 运动学规律
重物由静止释放，下落高度 $h$ 与时间 $Delta t$ 的关系为：
$ 1/2 a (Delta t)^2 = h $

*物理结论*：由于滑轮转动惯量 $I$ 的存在，加速度 $a$ 总是小于 $g$。项 $I / R^2$ 可视为滑轮对系统的 *等效平动质量*。


=== 8. 实验测量与连续体模型补充

==== (1) 转动惯量的实验反推
通过测量重物下落的高度 $h$ 与时间 $Delta t$，可以间接测定滑轮的转动惯量 $I$。
由 $a = (2 h) / (Delta t)^2$ 及前述加速度公式联立可得：
$ I = ( (g Delta t^2) / (2 h) - 1 ) m R^2 $

==== (2) 连续体转动惯量计算：均匀细杆
对于质量分布连续的物体，需要引入密度概念将求和转化为积分。
- *线性密度*：对于长度为 $L$、质量为 $m$ 的均匀细杆，定义线性密度为：
$ lambda = m / L $
- *微元分析*：取长度微元 $dif r$，其对应的质量微元为 $dif m = lambda dif r$。

*后续预告*：通过积分 $I = integral r^2 dif m$，我们可以推导出细杆绕不同转轴（如中心轴或端点轴）的具体转动惯量表达式。

#image("../Assets/img/20260401_200626.png",width:400pt)

#image("../Assets/img/20260401_200643.png",width:400pt)


=== 10. 连续体转动惯量的详细推导

==== (1) 均匀细杆 (1D)：绕中心轴
- *密度*：$lambda = m / L$
- *质量微元*：取距离中心 $r$ 处的微段 $dif r$，其质量 $dif m = (m / L) dif r$
- *积分过程*：
$ I = integral_(-L/2)^(L/2) r^2 (m / L) dif r = 2 (m / L) [r^3 / 3]_0^(L/2) = 1 / 12 m L^2 $

==== (2) 均匀圆盘 (2D)：绕中心垂直轴
- *密度*：$sigma = m / (pi R^2)$
- *质量微元*：取半径为 $r$、宽度为 $dif r$ 的薄圆环。该环面积 $dif A = 2 pi r dif r$，质量为：
$ dif m = sigma dot 2 pi r dif r = (2 m r dif r) / R^2 $
- *积分过程*：
$ I = integral_0^R r^2 dif m = integral_0^R r^2 ( (2 m r) / R^2 ) dif r $
$ I = (2 m) / R^2 [r^4 / 4]_0^R = 1 / 2 m R^2 $

*核心逻辑*：计算的关键在于寻找与转轴等距的 *几何微元*（细杆对应点，圆盘对应环），从而将复杂的多元积分简化为关于半径 $r$ 的一元积分。
=== 11. 三维 (3D) 连续体转动惯量：均匀球体

==== (1) 模型建立与密度
- *体密度*：$rho = m / (4 / 3 pi R^3)$
- *切片思路*：将球体沿 $z$ 轴垂直方向切成无数层厚度为 $dif z$ 的薄圆盘。

==== (2) 微元分析
对于高度为 $z$ 处的圆盘切片：
- *切片半径*：$r = sqrt(R^2 - z^2)$
- *质量微元*：$dif m = rho dot pi r^2 dif z = rho pi (R^2 - z^2) dif z$
- *惯量微元*（借用圆盘结论）：
  $ dif I = 1 / 2 (dif m) r^2 = 1 / 2 rho pi (R^2 - z^2)^2 dif z $

==== (3) 积分求解
利用参数替换（如板书所示 $z = R cos theta$）或直接对 $z$ 积分：
$ I = integral_(-R)^R 1 / 2 rho pi (R^2 - z^2)^2 dif z $
代入密度公式 $rho$ 最终化简得：
$ I = 2 / 5 m R^2 $

*维度总结*：
- 一维细杆：$1 / 12 m L^2$（或 $1 / 3$）
- 二维圆盘：$1 / 2 m R^2$
- 三维实心球：$2 / 5 m R^2$
- 三维薄球壳：$2 / 3 m R^2$（质量更分布在边缘，故系数更大）

=== 16. 平行轴定理 (Parallel-Axis Theorem) 的引入与矢量证明

==== (1) 定理引入背景与意义
转动惯量的积分计算 $I = integral r^2 dif m$ 高度依赖于转轴位置。为了高效求解非对称轴的惯量，引入平行轴定理。
- *核心逻辑*：若已知物体绕过质心轴的惯量 $I_C$，可通过代数公式求得绕任何与其平行的轴的惯量 $I$。
- *移轴增量*：新轴惯量总是大于质心轴惯量，其增加值为 $M d^2$（总质量 $times$ 轴间距平方）。

==== (2) 矢量几何关系建立
如板书图示，建立两个平行轴系（转轴原点 $O$ 与质心 $C$）。取刚体内任意质点 $i$，建立如下矢量三角形：
$ vct(r)_i = vct(d) + vct(r)_(i C) $
其中：
- $vct(d)$：从原点轴 $O$ 指向质心 $C$ 的距离矢量。
- $vct(r)_(i C)$：质点相对于质心的相对矢量。

==== (3) 动力学公式推导过程
依据定义展开新轴惯量 $I_z$：
$ I_z = sum m_i |vct(r)_i|^2 = sum m_i (vct(d) + vct(r)_(i C)) dot (vct(d) + vct(r)_(i C)) $
展开点积项：
$ I_z = sum m_i (d^2 + r_(i C)^2 + 2 vct(d) dot vct(r)_(i C)) $
对各项分别求和并物理化简（板书关键标注）：
- *公转项*：$sum m_i d^2 = (sum m_i) d^2 = M d^2$。
- *消去项（质心性质）*：$2 vct(d) dot (sum m_i vct(r)_(i C)) = 2 vct(d) dot vct(0) = 0$。
- *自转项*：$sum m_i r_(i C)^2 = I_C$。

==== (4) 最终定理与应用示例
联立上述项，得通用平行轴定理公式：
$ I = I_C + M d^2 $

- *应用举例：均匀细杆绕端点*
  - 已知：绕中心质心轴 $I_C = 1 / 12 m L^2$。
  - 偏离距离：新轴在端点，故 $d = L / 2$。
  - 代入定理：$I = (1 / 12 m L^2) + m (L / 2)^2 = (1 / 12 + 1 / 4) m L^2 = 1 / 3 m L^2$。

*物理总结*：平行轴定理将旋转运动拆解为 *绕质心的自转* 与 *质心绕轴心的公转* 两部分惯性的叠加。
*这期神了？！*

=== 19. 复杂连续体转动惯量与转动动能定理

==== (1) 均匀圆柱体绕横向中心轴的转动惯量
设均匀实心圆柱体质量为 $m$，半径为 $R$，长度为 $L$，体密度为 $rho = m / (pi R^2 L)$。求解其绕垂直于几何中心线的横向轴的转动惯量。

取距离中心轴为 $l$ 处，厚度为 $dif l$ 的薄圆盘为微元：
- *微元质量*：$dif m = rho pi R^2 dif l$
- *惯量组合（平行轴定理）*：
  微元对总转轴的惯量贡献由其绕自身直径的“自转项”与偏离中心的“平移项”组成：
  $ dif I = 1 / 4 (dif m) R^2 + (dif m) l^2 $
  展开代入密度：
  $ dif I = 1 / 4 (rho pi R^2 dif l) R^2 + (rho pi R^2 dif l) l^2 $

对整个圆柱体长度进行积分：
$ I = integral_(-L/2)^(L/2) ( 1 / 4 rho pi R^4 + rho pi R^2 l^2 ) dif l $
利用偶函数性质并化简，代入 $m = rho pi R^2 L$，得最终结果：
$ I = 1 / 4 m R^2 + 1 / 12 m L^2 $
*物理意义*：该结果完美体现了空间分布的叠加性，第一项是圆柱体作为“粗圆盘”的径向贡献，第二项是其作为“长细杆”的轴向贡献。

==== (2) 转动做功与转动动能定理 (Rotational Kinetic Energy)
如同力对平动物体做功，力矩对转动物体也做功。
- *微元做功*：$dif W = tau_z dif theta$
- *转动动能定义*：$E_k = 1 / 2 I_z omega^2$

由动力学方程 $tau_z = I_z (dif omega) / (dif t)$，同乘 $dif theta$ 并积分：
$ integral_(theta_0)^(theta_t) tau_z dif theta = integral_(omega_0)^(omega_t) I_z omega dif omega $
$ integral tau_z dif theta = 1 / 2 I_z omega_t^2 - 1 / 2 I_z omega_0^2 $
*结论*：合外力矩对刚体所做的功，等于该刚体转动动能的变化量。这打通了定轴转动中力与能量的计算壁垒。

SO: $K=1/2 m v^2+1 /2 I_c omega^2$

=== 21. 均匀圆柱体横轴惯量的微观构建

==== (1) 微元受力分析：为什么必须拆项？
根据 *平行轴定理*，任意微元对定轴的转动惯量 $dif I$ 必须考虑其 *自身分布* 与 *位置偏离*：
$ dif I = dif I_"自转" + dif I_"平移" $
- 若忽略 $dif I_"自转"$，则相当于将厚度为 $dif l$ 的圆盘压缩为质点，会导致 $R$ 方向上的质量分布丢失。

==== (2) 关键系数 $1/4$ 的几何解释
由于切片圆盘是绕其 *直径*（位于盘面内）旋转，而非绕中心垂直轴旋转：
- 绕中心轴（垂直）：$I_"vertical" = 1/2 m R^2$
- 依据垂直轴定理：$I_"vertical" = I_"直径1" + I_"直径2"$
- 对称性得出：$I_"直径" = 1/2 I_"vertical" = 1/4 m R^2$

==== (3) 积分表达式的物理构成
代入体密度 $rho$ 与微元体积 $dif V = pi R^2 dif l$：
$ dif I = underbrace(1/4 (rho pi R^2 dif l) R^2, "自转项：盘面内的翻转惯量") + underbrace((rho pi R^2 dif l) l^2, "平移项：质点化的公转惯量") $

对全长 $L$ 积分（从 $-L/2$ 到 $L/2$）：
$ I = integral_(-L/2)^(L/2) rho pi R^2 (1/4 R^2 + l^2) dif l $
最终化简得：$I = 1/4 m R^2 + 1/12 m L^2$

=== 22. 垂直轴定理 (Perpendicular Axis Theorem) 详解

==== (1) 适用范围
该定理仅适用于 *薄板类* 刚体（即厚度远小于半径的物体）。

==== (2) 定理内容
若薄板位于 $x-y$ 平面，则其绕垂直于板面的 $z$ 轴的转动惯量 $I_z$ 与绕板内互相垂直的 $x, y$ 轴的转动惯量满足：
$ I_z = I_x + I_y $

==== (3) 圆盘 $1/4$ 系数的推演逻辑
- *前提*：已知圆盘绕中心垂直轴 $I_z = 1/2 m R^2$。
- *对称性*：因圆盘关于直径对称，故 $I_x = I_y$（$x, y$ 均为直径轴）。
- *求解*：
  $ 1/2 m R^2 = 2 I_x => I_x = 1/4 m R^2 $

==== (4) 总结
在圆柱体横向积分公式中，出现的 $1/4 rho pi R^4 dif l$ 项（即 $1/4 dif m R^2$），本质上就是每一层微元圆盘绕其 *自身直径* 转动的“自转惯量”。

=== 23. 纯滚动、细杆摆动、悠悠球和其他杂项

==== (1) 纯滚动 (Pure Rolling) 扩展

$a=beta R,f <=|mu|F_N$ 也是纯滚动条件。

做事情一定要同时考虑*纯滚动、转动、平动三大约束！*

=== 24. 细杆转动补充

距离 $O$ 点 $x$ 处，角速度 $(3g)/(2l)sin theta$，切向加速度 $a=(3g x)/(2l)sin theta$

张力公式：分析的时候从 $x$ 到 $l$ 分析，取这一段的质心。

最后答案 $T_"切向"=m g sin theta 3/4 (l-x)(x-l/3)1/l^2
\ T_"径向     " 1/2 I omega^2=m g l/2(1-cos theta)$ 能量守恒先愣算一波。然后 $|F_n - m^' g cos theta|=m omega^2 r$



=== 刚体动力学核心考点汇总

---

==== 1. 沿杆向心内力的计算 ($F_n$)
计算杆内张力的关键在于识别**向心力需求**与**重力分量**的差异。

- *步骤一*：能量守恒求角速度 $omega$。
  $ 1/2 I omega^2 = m g l/2 (1 - cos theta) => omega^2 = (3g) / l (1 - cos theta) $
- *步骤二*：隔离分析。取支点外侧段 $(x, l)$，质量 $m' = m (l-x)/l$。
- *步骤三*：列方程。$F_n(x) - m' g cos theta = m' omega^2 (l+x)/2$。张力方向始终指向支点。

==== 2. 刚体动力学三大约束
解决复杂问题的标准“翻译”逻辑：

1. *动力学约束*：平动 $sum vec(F) = m vec(a)_c$ 与转动 $sum vec(M)_c = I_c vec(beta)$。
2. *运动学约束*：纯滚动 $v_c = omega R$，$a_c = beta R$。
3. *接触约束*：摩擦力极限 $f <= mu_s N$。

==== 3. 角动量与天体系统模型
在角动量守恒 ($L = I omega$) 的前提下，半径收缩会导致加速度剧增。

- *动量矩守恒*：$L = m R^2 omega$。
- *加速度演化*：
  因为 $omega = L / (m R^2)$，代入向心加速度 $a_n = omega^2 R$：
  $ a_n = (L / (m R^2))^2 R = L^2 / (m^2 R^3) $
  即半径缩小到 $1/10$，加速度会飙升到 $1000$ 倍。

==== 4. 转动惯量关键定理
- *平行轴定理*：$I = I_c + m d^2$。
- *垂直轴定理*：$I_z = I_x + I_y$（仅限薄板）。
- *圆柱体横轴惯量*：
  $ I = 1/12 m L^2 + 1/4 m R^2 $
  其中 $1/4 m R^2$ 项是考虑了圆柱作为“厚圆盘”绕直径旋转的贡献。

==== 5. 势能场与力（带符号模型）
力是势能的空间负梯度，指向能量降低的方向。

- *定义式*：$vec(F) = - nabla E_p quad or quad F = - (d U) / (d r)$
- *质心原则*：计算刚体势能场时，只需盯着质心（COM）：$E_p = m g h_"com"$。

==== 6. 质心系与惯性系转换
- *柯尼希定理（动能）*：$E_k = 1/2 m v_c^2 + 1/2 I_c omega^2$。
- *转换优势*：在质心系中，总动量为 $0$。即使质心在加速，对质心的转动定律 $M = I_c beta$ 依然成立，因为惯性力矩为 $0$。

==== 7. 杆内张力的“正负反转”现象
在分析切向张力 $T_t$ 时，存在一个由重力分配导致的临界点：

- *物理逻辑*：张力的本质是“补差价”。
- *临界位置*：在细杆绕端点摆动时，若 $x < l/3$，重力分量大于该处所需的向心力/切向力，张力向上“顶”；若 $x > l/3$，重力不够用，张力向下“拉”。
- *结论*：在 $x = l/3$ 处，杆内部的切向张力恰好为零。

==== 8. 纯滚动的临界静摩擦
判断物体是“纯滚动”还是“滑动”的唯一标准：

- *摩擦力需求*：$f = (k / (1+k)) m g sin theta$（实心球 $k=2/5$，则 $f=2/7 m g sin theta$）。
- *临界条件*：要求 $f <= mu_s N$。
- *判据公式*：$mu_s >= k / (1+k) tan theta$。
  - 对于实心球：$mu_s >= 2/7 tan theta$。
  - 对于实心圆柱：$mu_s >= 1/3 tan theta$。

==== 9. 动能计算的“瞬时转轴”捷径
计算动能不一定要用“平动 + 转动”的柯尼希定理，可以一步到位：

- *公式*：$E_k = 1/2 I_P omega^2$。
- *条件*：$P$ 必须是速度为零的**瞬时转轴**（如纯滚动接触点或固定支点）。
- *等价性证明*：
  $ 1/2 I_P omega^2 = 1/2 (I_c + m d^2) omega^2 = 1/2 I_c omega^2 + 1/2 m v_c^2 $
  *注意*：使用此法时，平动能已包含在内，不可重复叠加。

==== 10. 冲量矩与撞击中心 (Center of Percussion)
对应板书左上角关于 $r_c, r_h$ 的推导：

- *冲量矩定理*：$integral tau d t = Delta L = I Delta omega$。
- *撞击中心*：当外力作用在距离支点 $h = I / (m r_c)$ 的位置时，支座处的瞬时反力为 $0$。
  - 对于细杆绕端点：$I = 1/3 m l^2, r_c = l/2$，则 $h = 2/3 l$。
  - 这解释了为什么球棒打在 $2/3$ 处最“不震手”。