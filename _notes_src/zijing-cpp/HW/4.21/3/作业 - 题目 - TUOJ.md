# K-th Smallest Number

## Description

Given an integer array $(a\_0, a\_1, \cdots, a\_{n-1})$, find the $k$-th smallest number in the array.

## Input

The first line contains two integers $n$ and $k$, where:

* $1 \leq n \leq 5000$
* $1 \leq k \leq n$

The second line contains $n$ integers, each in the range $[1, 5000]$.

## Output

Output the $k$-th smallest number in the array.

## Sample Input

```
4 2
1 2 3 4
```

## Sample Output

```
2
```

## Hint

You may use `std::sort` or `std::nth_element` in C++.

If you are not familiar with them, you can search online for how to use them.
