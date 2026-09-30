#import "../module/myutils.typ":*
#show : conf

= Calculus A(2) Homework 郭嘉乐 2025013332

#outline()

== HW 2 #(datetime(day: 15, month: 3, year: 2026)).display()

=== Problem 2.1

#image("屏幕截图 2026-03-15 233242.png",width: 300pt)

1. For 1st of the left, the level curves are rectangles with rounded corners and their vertexs are on the axes, which you can only get it by "cut" the 4th of the right.
2. For 2nd of the left, the level curves are exactly squares with the same center and their vertexs are on the axes, which only fit the 1st of the right.
3. For 3rd of the left, the level curves are circles with the same center, which only fit the 2nd of the right.
4. For 4th of the left, the level curves are rectangles with rounded corners and their sides are parallel to the axes, which you can only get it by "cut" the 5th of the right.
5. For 5th of the left, the level curves like "indents" with their vertexs on the axes, which only fit the 3rd of the right.

=== Problem 2.2

#image("屏幕截图 2026-03-16 161309.png",width: 300pt)

(Here the indexes mean the index of the left pictures.)

1. Obviously the density of curves is becoming larger and larger as the distance from the origin increases, which fits 4(R).
2. The density is always the same as the distance from the origin increases, which fits 5(R) as 5(R) looks like a cone.
3. 4. 5. Their densitues are becoming larger as the distance from the origin increases. Also, The densities of them are bigger than the one before, and from 3 to 5 and the ratio of the length of the first curve in the middle to the others is also becoming larger, which means 3(L)-2(R), 4(L)-1(R), 5(L)-3(R).

=== Problem 2.3

#image("屏幕截图 2026-03-16 162800.png", width: 300pt)

(I think it's hard to describe the picture.)

(Here the indexes mean the index of the left pictures.)

1. The only one which the elliptical symmetrical figures of the level curves are on the axes.

(2.,3.,4.,5. are the same type.)

2. The density is the largest form the origin, and level curves are like radiations.
3. The density is the smallest form the origin.
4. The density is between the 3. and 5.
5. The density is the larger the 4. and the "original" figure is mostly like a square.

=== Problem 2.4 \*\*\*\*

1. figure 4.see 2.
2. figure 5. for obviously the concave-convex is sharper then 1. as they all have 3 "saddles" and tops.
3. 3. for the last problem we found.
4. figure 2. see in 5.
5. figure 1. for obviously the concave-convex is sharper then 4. as they all have 5 "saddles" and tops.

=== Problem 2.5

// 常见二次曲面类型 (Common Quadric Surfaces):
// 1. 椭球面 (Ellipsoid)
// 2. 单叶双曲面 (Hyperboloid of one sheet)
// 3. 双叶双曲面 (Hyperboloid of two sheets)
// 4. 椭圆抛物面 (Elliptic paraboloid)
// 5. 双曲抛物面 (Hyperbolic paraboloid)
// 6. 椭圆锥面 (Elliptic cone)
// 7. 椭圆柱面 (Elliptic cylinder)
// 8. 双曲柱面 (Hyperbolic cylinder)
// 9. 抛物柱面 (Parabolic cylinder)

1. We fix $z$, and get like $y=x^2-4z_0-2$, it is a parabola. So it is a parabolic cylinder.

2. We get $x^2/1+y^2/1+z^2/4=1/4$. Obviously it is a ellipsoid.
3.\* We fix $z$, then $x^2+y^2=(1-z_0)/4$. It's obviously what we taught: paraboloid.

// 注意第一次分析错了！！！
  
1. We fix $z$, then $x^2-y^2=(z_0-1)/4$. From slices to the whole, we find it a hyperbolic paraboloid.

=== Problem 2.6

1. matches figure 4., $f(r, theta) = r^3 cos(3 theta)$, makes the figure smooth and 3 tops and bottoms.
2. matches figure 2., for (let $z=f(x,y)$) $x^2+y^2=ln (1/z)$, which compares to 4. the radius of each slice decreases faster as $z$ increases. And they all make bumps. So it is sharper.
3. matches figure 3. for it has $cos,sin$ to make the figure have many tops and bottoms by period.
4. matches figure 1., for (let $z=f(x,y)$) $x^2+y^2=1/z -1$. As we say in 2., it is not the shaper one but a bump.


=== Problem 2.7 \*
1. $(x-1)^2+(y-1)^2+(z-1)^2=4$
2.\* Set a point P on the line, a direction vector $vct(v)$, then it means $
r=(|vct(O P) times vct(v)|) / (|vct(v)|) \
=> 1 = (|vec(x,y,z) times vec(1,1,1)|) / sqrt(1^2+1^2+1^2) \
=>
(y-z)^2+(z-x)^2+(x-y)^2=3
$

from the definition.

3. While $x = r cos theta,  quad y = r sin theta,  quad r^2 = x^2+y^2$,
$
z=r^2 cos (2 theta) \
=> z=r^2 (cos^2 theta-sin^2 theta) \
=> z=(r cos theta)^2-(r sin theta)^2 \
=> z=x^2-y^2
$

4.
$
z=r^3 cos (3 theta) \
=> z=r^3(4 cos^3 theta-3 cos theta) \
=> z=4(r cos theta)^3-3 r^2(r cos theta) \
=> z=4x^3-3r^2x \
=> z=4x^3-3(x^2+y^2)x \
=> z=x^3 - 3x y^2
$

5. $x = rho sin phi cos theta ,y = rho sin phi sin theta ,z = rho cos phi, x^2+y^2+z^2= rho^2$
So
$
x = 2 cos theta, y= 2 sin theta,z= rho cos phi \
=> x^2 + y^2 = 4
$

6. Obviously it is $z=2$.

7. 
$
rho sin ^2 phi = cos phi \
=> rho dot (x^2+y^2)/rho^2 = z/rho \
=> x^2+y^2=z
$


=== Problem 2.8 \*
#import "@preview/cetz:0.4.2"
#import "@preview/cetz-plot:0.1.3": plot

#cetz.canvas({
  plot.plot(
    size: (5, 5),
    x-min: -1.1, x-max: 1.1,
    y-min: -1.1, y-max: 1.1,
    {
      plot.add(
        domain: (0, 6 * calc.pi),
        samples: 600,
        t => {
          let b = 0.3
          (
            (1 - b) * calc.cos(t) + b * calc.cos((1 - b) / b * t),
            (1 - b) * calc.sin(t) - b * calc.sin((1 - b) / b * t),
          )
        }
      )
    }
  )
})

No. It's not regular, for from the figure there're many "sudden direction changes", which means there the vector of velocity is 0, so it's not regular.

== HW 3 #datetime(day:23,month:3,year:2026).display()

