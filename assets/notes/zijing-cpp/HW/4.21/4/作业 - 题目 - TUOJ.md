# One-Move Chess Problem

## Description

You are given an `n × m` chessboard.  
There are `Q` independent queries. In each query, you are given:

* the **type of a chess piece**,
* its starting position `(x1, y1)`,
* and a target position `(x2, y2)`.

For each query, determine whether this piece can move from `(x1, y1)` to `(x2, y2)` in **exactly one move**.

The board uses **1-based indexing**:

* rows are numbered from `1` to `n`,
* columns are numbered from `1` to `m`.

You may assume both given positions are valid cells on the board.

The piece type is given as a string, and it will be one of the following:

* `king`
* `queen`
* `rook`
* `bishop`
* `knight`
* `pawn`

Their movement rules follow standard chess movement rules, with the following clarifications:

* **king**: moves one square in any direction.
* **queen**: moves any number of squares in the same row, same column, or along a diagonal.
* **rook**: moves any number of squares in the same row or same column.
* **bishop**: moves any number of squares along a diagonal.
* **knight**: moves in an `L` shape: `(2,1)` or `(1,2)`.
* **pawn**: moves **forward by exactly one row**, without considering captures, initial two-step moves, en passant, promotion, or color differences.  
  For this problem, define "forward" as from row `x` to row `x + 1`, so a pawn can move from `(x, y)` to `(x + 1, y)`.

---

## Input

The first line contains two integers `n` and `m`, the number of rows and columns of the chessboard.

The second line contains an integer `Q`, the number of queries.

Each of the next `Q` lines contains:

```
piece x1 y1 x2 y2
```

* `piece` is a string representing the type of the chess piece,
* `(x1, y1)` is the starting position,
* `(x2, y2)` is the target position.

---

## Output

For each query, output:

* `Yes` if the piece can move from `(x1, y1)` to `(x2, y2)` in exactly one move,
* `No` otherwise.

---

## Constraints

You may choose constraints such as:

* `1 ≤ n, m ≤ 10^9`
* `1 ≤ Q ≤ 2 × 10^5`

The solution should process each query in `O(1)` time.

---

## Notes

* Queries are **independent**.
* No other pieces are placed on the board, so movement is checked only by geometric rules.
* Remaining at the same position does **not** count as a move.

---

## Sample Input

```
8 8
6
king 4 4 5 5
rook 2 3 2 8
bishop 1 1 2 3
knight 3 3 5 4
pawn 4 2 5 2
queen 6 6 6 6
```

## Sample Output

```
Yes
Yes
No
Yes
Yes
No
```
