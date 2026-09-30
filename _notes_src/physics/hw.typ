#import "../module/myutils.typ" : *
#import "engine.typ":*

#show : conf

#let g = 9.80

= 大学物理 英 1 作业 紫荆 53 郭嘉乐

#outline()

== HW 2 #datetime(year:2026,month:3,day:19).display()

=== 1. Rock Climber

==== a
 #image("../Assets/img/20260319_224719.png",width:150pt)

==== b
根据受力分析，由牛顿第一定律，人在水平方向受力平衡，故 $F_L=F_R$；则对于摩擦力， $f_L=1.2 F_L,f_R=0.8 F_R$ 且 $G = f_L + f_R=1.2 F_L + 0.8 F_R = 2 F_L = m g= cal("55 * 9.8") "N"$，那么可知  $F_L=F_R= G / 2 = cal("55 * 9.8 / 2",digits:#1) "N"$

==== c
显然的这个比例是 $iota = mu_1 / (mu_1+mu_2) = cal("1.2 / (1.2+0.8)")$

=== 2. Three-Mass Pulley System

==== a
设绳 1 张力为 $T_1$，绳 2 张力为 $T_2$。设 $m_1$ 向上加速度为 $a_1$，则动滑轮 $B$ 向下加速度亦为 $a_1$。设 $m_2$ 相对于滑轮 $B$ 向下的加速度为 $a_r$。
$
cases(
  T_1 - m_1 g = m_1 a_1,
  T_1 = 2 T_2,
  m_2 g - T_2 = m_2 (a_1 + a_r),
  T_2 - m_3 g = m_3 (a_r - a_1)
)
$
代入数据 $m_1=0.20 "kg", m_2=0.10 "kg", m_3=0.05 "kg"$：
$a_1 = (2 m_2 m_3 - m_1(m_2 + m_3)) / (m_1(m_2 + m_3) + 4 m_2 m_3) g$
$a_1 = -3.92 "m/s"^2$ （负号表示 $m_1$ 实际向下加速）：
- $m_1$ 加速度：$3.92 "m/s"^2$ (向下)
- $m_2$ 加速度：$0.78 "m/s"^2$ (向下)
- $m_3$ 加速度：$8.62 "m/s"^2$ (向上)

==== b
$T_1 = m_1 (g + a_1) = 0.20 times (9.80 - 3.92) = 1.18 "N"$
$T_2 = T_1 / 2 = 0.59 "N"$

=== 3\*. 斜面问题

（卡住了一会……难……）

对于斜面而言：由牛顿第二定律，实际上受力分析只能得到 $N sin theta = M a_2$

对于小物块而言，以地面作为惯性参考系，我们看到此时他对于垂直斜面方向的加速度为 $a_"垂"$，则

$
a_"垂" = a_2 sin theta \ 
m a_"垂" = m g cos theta - N\
$
联立上述三个方程，得到 $a_2=(m g sin theta cos theta) / (M+ m sin^2 theta)$



=== 4. Blocks and Pulley on an Accelerating Cart I

若 $m_1, m_2$ 相对小车静止，系统共同水平加速度为 $a$：
对 $m_2$：$T = m_2 g$
对 $m_1$：$T = m_1 a$
得 $a = (m_2 g) / m_1$。
所需水平力：$F = (M + m_1 + m_2) (m_2 g) / m_1$

=== 5. Blocks and Pulley on an Accelerating Cart II

由于 $m_2$ 只能垂直移动，其水平加速度必与小车 $M$ 一致（设为 $A$）。
由水平方向合力为零：$(M + m_1 + m_2) A + m_1 a_r = 0$。
联立，解得 $A = 0$。
- (a) $T = (m_1 m_2 g) / (m_1 + m_2)$
- (b) $a_2 = (m_2 g) / (m_1 + m_2)$ (向下)
- (c) $A = 0$
- (d) $a_1 = (m_2 g) / (m_1 + m_2)$ (向右)

=== 6. Bead on a Rotating Circular Hoop

==== a
周期 $T = 0.450 "s"$ 时，$omega = (2 pi) / T$。
$ cos theta = g / (omega^2 R) = (g T^2) / (4 pi^2 R) $
代入数据：$cos theta = (9.80 times 0.450 times 0.450) / (4 times pi^2 times 0.15) approx 0.33$
解得：$theta approx 70.43 degree$

==== b
$T = 0.850 "s"$ 时，$cos theta approx 1.19 > 1$，故 $theta = 0 degree$。

=== 7. Pressure Inside a Self-Gravitating Sphere

==== a
（抽象）

考虑球内半径 $r$ 处厚度为 $dif r$ 的一个微元层。该层以内质量 $M(r) = 4/3 pi r^3 rho$，引力加速度 $g(r) = (G M(r)) / r^2 = 4/3 pi G rho r$。
层内外压力差抵消重力：$d p = - rho g(r) d r$。
$ integral_(p_c)^0 d p = - integral_0^R 4/3 pi G rho^2 r d r $
$ p_c = 2/3 pi G rho^2 R^2 $

==== b
代入 $rho approx 1.3 times 10^3 "kg/m"^3, R approx 7.0 times 10^8 "m"$：
$p_c approx 1.15 times 10^14 "Pa" approx 1.14 times 10^9 "atm"$

=== 8. Mass and String

==== a
忽略重力，角动量守恒：$m r_0^2 omega_0 = m (r_0 - V t)^2 omega(t)$。
$ omega(t) = omega_0 (r_0 / (r_0 - V t))^2 $

==== b
拉力 $F$ 提供向心力：
$ F = m omega(t)^2 r(t) = (m omega_0^2 r_0^4) / (r_0 - V t)^3 $

== HW 3 #datetime(year:2026,month:3,day:31).display()

=== 1. Bullet Fired into a Block
#[

助教你好，你接下来可能会看见一些奇怪的重复的物理量说明。但是这是我所使用的标记语言所必需的QAQ

#cpt("h=1",unit:"m")
#cpt("m=0.008",unit: "k g")
#cpt("M=2.5",unit:"k g")
#cpt("d=2",unit:"m")

首先计算物块下落到地面的时间 #cpt("t=sqrt((2*h)/g)",unit:"s")


 
则从桌面飞出去的速度为 #cpt("v_1=d/t",unit:"m/s ")

由动量定理，
$
  m v_0 = (m+M) v_1
$

则得到子弹初速度为 #cpt("v_0=(m+M)*v_1/m",unit:"m/s")
]
#let mf = 3000 // kg
#let dv = 10000 // m/s

= 2. Rocket Propulsion in Deep Space

根据齐奥尔科夫斯基火箭方程：
$ Delta v = v_"ex" ln(m_0 / m_f) arrow m_0 = m_f e^(Delta v / v_"ex") $
其中负载 $m_f = 3000 "kg"$, 速度增量 $Delta v = 10000 "m/s"$。

== (a) 排气速度 $v_"ex" = 2000 "m/s"$ 时：
$ m_0 = 3000 times e^(10000 / 2000) = 3000 times e^5 approx 445239 "kg" $
$ m_"fuel" = m_0 - m_f = 445239 - 3000 = 442239 "kg" approx 442.2 "t" $

== (b) 排气速度 $v_"ex" = 5000 "m/s"$ 时：
$ m_0 = 3000 times e^(10000 / 5000) = 3000 times e^2 approx 22167 "kg" $
$ m_"fuel" = m_0 - m_f = 22167 - 3000 = 19167 "kg" approx 19.2 "t" $

=== 3. Falling Chain on a Table

#image("../Assets/hw3/hw3-img-002.png", width: 180pt)

设链条长度为$L$，总质量为$M$。当链条下落距离$x$时，已经落在桌面上的链条重量为：
$F_g = M g x / L$

同时，不断有新的小段链条落到桌面上，其动量变化产生附加冲击力。由自由落体，下落$x$后的速度满足$v^2 = 2 g x$，即$v = sqrt(2 g x)$。

在$dif t$时间内，落到桌面的链条长度$dif x = v dif t$，其动量变化为：
$dif p = dif m v = (M / L dif x) v = M v^2 dif t / L$

由动量定理，附加冲击力 $F' dif t = dif p$，得：
$F' = M v^2 / L = 2 M g x / L$

总作用力为重量与附加冲击力之和（牛顿第三定律保证桌子对链条的力与桌子受到的力大小相等）：
#box($F = 3 M g x / L$)

=== 4. Center\*

假设原点在这个半圆的圆心，$x$ 轴在其直线段边上。

$vct(r_c)=(integral rho vct(r) dif V) / (integral rho dif V ) = (integral vct(r) dif V) / (integral dif V ) = (integral vct(r) dif A) / (integral dif A )$

此时让 $vct(r)=(x,y);x=r cos theta ,y=r sin theta$

则对于 $x$ 分量，$integral x dif A = integral_0^pi integral_0^R (r cos theta )(r dif r dif theta) = ( integral_0^pi cos theta  d theta ) dot ( integral_0^R r^2 dif r )= 0 dot integral_0^R r^2 dif r =0$，故 $x_c=0$

对于 $y$ 分量，$integral y dif A = integral_0^pi integral_0^R (r sin theta )(r dif r dif theta) = ( integral_0^pi sin theta  d theta ) dot ( integral_0^R r^2 dif r )= -cos theta |_0^pi dot integral_0^R r^2 dif r =2 dot R^3 / 3 = (2 R^3) / 3$，

$integral dif A = (pi R^2)/2$，故 $y_c=(4 R) / (3 pi)$，故 $vct(r_c)=(0,(4 R) / (3 pi))$

=== 5. Two Orbiting Astronauts

#image("../Assets/hw3/hw3-img-004.png", width: 180pt)

两宇航员质量均为$M$，用长$d$的轻绳连接，各以速率$v$绕质心转动。两宇航员绕系统质心做圆周运动，每个宇航员到质心的距离为 $d / 2$。

==== a
每个宇航员的角动量大小为 $L_i = M v d / 2$，总角动量为：
#box($L = 2 M v d / 2 = M v d$)

==== b
绳子缩短是宇航员之间的内力作用，系统不受外力矩，因此由*角动量守恒*，新的角动量仍为：
#box($L' = M v d$)

==== c
绳子缩短到 $d / 2$ 后，每个宇航员到质心的距离变为 $d / 4$。设新速度为 $v'$，则总角动量：
$L' = 2 M v' d / 4 = M v' d / 2$

由角动量守恒 $L' = L$：
$M v' d / 2 = M v d$
解得
#box($v' = 2 v$)

=== 6. Collision Involving a Rotating Rod

建立坐标系：碰撞前，原杆质心在原点 $O$。碰撞瞬间，粒子 $A$ 在位置 $(+a / 2, 0)$，速度 $v_A = +omega a / 2$（沿 $y$ 方向）；粒子 $B$ 在位置 $(-a / 2, 0)$，速度 $v_B = -omega a / 2$；粒子 $C$ 静止在碰撞位置 $(a / 2, 0)$，速度为 $0$。

==== a
质心坐标由定义计算：
$
x_"cm" = (m a / 2 + m (-a / 2) + m a / 2) / (3 m) = (m a / 2) / (3 m) = a / 6
$
$y_"cm" = 0$

质心位置在原杆质心与碰撞点连线上，距离原质心 $a / 6$，距离碰撞点 $a / 3$。

质心速度：
$
v_"cm" = (m v_A + m v_B + m v_C) / (3 m) = (m omega a / 2 + m (-omega a / 2) + m 0) / (3 m) = #box($0$)
$

故碰撞前质心速度为零。

==== b
计算相对于质心（位置 $x = a / 6$）的总角动量：

- 粒子 $A$：相对位置 $a / 2 - a / 6 = a / 3$，速度 $omega a / 2$，角动量 $L_A = m (a / 3) (omega a / 2) = m omega a^2 / 6$
- 粒子 $B$：相对位置 $-a / 2 - a / 6 = -2 a / 3$，速度 $-omega a / 2$，角动量 $L_B = m (-2 a / 3) (-omega a / 2) = m omega a^2 / 3$
- 粒子 $C$：相对位置 $a / 2 - a / 6 = a / 3$，速度 $0$，角动量 $L_C = 0$

总角动量：
#box($L = L_A + L_B + L_C = m omega a^2 / 2$)

碰撞过程中，外力矩为零，*角动量守恒*，所以碰撞后瞬间角动量大小不变，仍为 $m omega a^2 / 2$。

==== c
碰撞后，计算系统绕质心的转动惯量：

- 复合粒子 $A+C$：质量 $2m$，距质心 $a / 3$，$I_1 = 2m (a / 3)^2 = 2 m a^2 / 9$
- 粒子 $B$：质量 $m$，距质心 $2 a / 3$，$I_2 = m (2 a / 3)^2 = 4 m a^2 / 9$

总转动惯量：
$I = I_1 + I_2 = 2 m a^2 / 9 + 4 m a^2 / 9 = 2 m a^2 / 3$

由角动量关系 $L = I omega'$：
$m omega a^2 / 2 = (2 / 3) m a^2 omega'$

解得：
#box($omega' = 3 omega / 4$)