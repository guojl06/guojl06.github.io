# Chapter 12: The Standard Template Library (STL)

**Prerequisites:** Arrays, functions, classes, basic pointers/references, `std::string`

### Reading Map

| Section | Content | Priority |
| --- | --- | --- |
| §1 | Move log design — why `vector` | **Essential** |
| §2 | Log operations — append, undo, search | **Essential** |
| §3 | Sorting algorithms — analysis & comparison | **Essential** |
| §4 | Sorting the move log with `std::sort` | **Essential** |
| §5 | Defensive programming & exceptions | **Essential** |
| §6 | Summary and common mistakes | **Review** |

> **Chapter focus**: Every STL idea in this chapter serves the **chess move log** — a growable list of `Move` records. Sorting gets full treatment because you will order that log for analysis and compare algorithm choices in real projects.

Compile: `g++ -std=c++17 main.cpp -o main` (add extra `.cpp` files as shown)

***

## Bilingual Reference — Log & Sort Terms

| English | Chinese (中文) | Meaning |
| --- | --- | --- |
| Move log | 走棋记录 | Ordered list of moves played in a game |
| `vector<Move>` | 走法向量 | Dynamic array holding `Move` structs |
| Iterator | 迭代器 | `begin()` / `end()` — range for algorithms |
| Comparator | 比较器 | Function defining sort order (e.g. by `toRow`) |
| Stable sort | 稳定排序 | Equal elements keep their original relative order |
| Time complexity | 时间复杂度 | How runtime grows: O(n), O(n²), O(n log n) |
| Defensive programming | 防御性编程 | Validate inputs and bounds before they cause crashes |
| Exception | 异常 | Runtime error signal; catch with `try` / `catch` |
| `std::out_of_range` | 越界异常 | Thrown by `vector::at()` on invalid index |

***

## 1. Move Log Design — Why `vector`

### 1.1 The Problem

A chess game records every move in order. You might have 40–200 moves, but the count is unknown at compile time.

A **fixed-size array** forces you to guess capacity and track `moveCount` yourself:

```cpp
const int MAX_MOVES = 100;
Move moveLog[MAX_MOVES];
int moveCount = 0;   // Easy to get out of sync with the array

moveLog[moveCount++] = {6, 4, 4, 4};  // e4 — what if move 101 arrives?
```

**Design flaws:**

| Issue | Consequence |
| --- | --- |
| Fixed capacity | Overflow or wasted space |
| Manual `moveCount` | Off-by-one bugs, overwrite previous moves |
| No undo helper | You implement shrink logic by hand |
| No sort/search | Every analysis feature starts from scratch |

![Fixed array vs dynamic vector](assets/ch12_vector_vs_array.png)
*Figure 1: Fixed array vs `vector` — the log grows with each move*

### 1.2 The Design Choice — `vector<Move>`

`std::vector` is a **dynamic array**: append at the end, track size automatically, compatible with STL algorithms.

```cpp
#include <vector>

struct Move {
    int fromRow, fromCol;
    int toRow, toCol;
};

vector<Move> moveLog;
moveLog.push_back({6, 4, 4, 4});   // e4
moveLog.push_back({0, 1, 2, 2});   // Nc6
// moveLog.size() == 2 — no separate counter
```

**Why `vector` fits the log:**

| Log requirement | `vector` support |
| --- | --- |
| Append moves in order | `push_back` — O(1) amortized |
| Undo last move | `pop_back` |
| Random access by index | `moveLog[i]` — replay move *n* |
| Pass range to `sort` | `begin()` / `end()` iterators |
| Sequential replay | Index loop or iterator loop |

### 1.3 Encapsulating the Log — `MoveLog` Class

Hide the `vector` inside a class so game code calls `addMove` / `getCount` instead of touching the container directly.

```cpp
// chess/move_log.h
#ifndef CHESS_MOVE_LOG_H
#define CHESS_MOVE_LOG_H

#include <vector>

struct Move {
    int fromRow, fromCol, toRow, toCol;
};

class MoveLog {
public:
    void addMove(int fromRow, int fromCol, int toRow, int toCol);
    int getCount() const;
    bool undoLast();   // returns false if log is empty

private:
    std::vector<Move> moves_;
};

#endif
```

```cpp
// chess/move_log.cpp
#include "move_log.h"

void MoveLog::addMove(int fr, int fc, int tr, int tc) {
    moves_.push_back({fr, fc, tr, tc});
}

int MoveLog::getCount() const { return moves_.size(); }

bool MoveLog::undoLast() {
    if (moves_.empty()) return false;
    moves_.pop_back();
    return true;
}
```

> **Design rule**: The log is **append-only during play**; undo removes from the **tail** only. That matches `vector`'s strengths — no need for `list` unless you insert in the middle.
> **Checkpoint §1**: Explain why a fixed array is a poor log design and how `vector<Move>` + `MoveLog` fixes it.

***

## 2. Log Operations — Append, Undo, Walk, Search

Once the log is a `vector<Move>`, daily operations are a small set of patterns.

### 2.1 Core Log Operations

| Operation | Code pattern | Log use case |
| --- | --- | --- |
| Record move | `log.push_back(m);` | After each legal move |
| Undo | `if (!log.empty()) log.pop_back();` | Take back last move |
| Count | `log.size()` | Move number, draw rules |
| Last move | `log.back()` | Highlight last ply |
| Walk all moves | `for (… it = log.begin(); …)` | Print PGN, analysis |
| Find move | `find_if(…, predicate)` | Locate d4, row-4 lands |

> **Safety**: Check `!log.empty()` before `back()` or `pop_back()`. Use `it != log.end()` after `find_if`.

### 2.2 Example — Record, Undo, and Print

```cpp
#include <iostream>
#include <vector>
using namespace std;

struct Move { int fromRow, fromCol, toRow, toCol; };

int main() {
    vector<Move> log;
    log.push_back({6, 4, 4, 4});
    log.push_back({0, 1, 2, 2});

    cout << "Moves: " << log.size() << endl;
    if (!log.empty()) log.pop_back();
    cout << "After undo: " << log.size() << endl;

    for (size_t i = 0; i < log.size(); ++i)
        cout << "  [" << i << "] -> row " << log[i].toRow << endl;
    return 0;
}
```

### 2.3 Iterators — How Algorithms See the Log

Algorithms do not know about `vector` directly. They take a **range** `[begin, end)` — from first move to one-past-last.

```cpp
for (vector<Move>::iterator it = log.begin(); it != log.end(); ++it)
    cout << "(" << it->toRow << "," << it->toCol << ")\n";
```

![Iterator range](assets/ch12_iterator_range.png)
*Figure 2: `[begin, end)` on a move log — `end` is after the last move*

### 2.4 Example — Find a Move in the Log

```cpp
#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;

struct Move { int fromRow, fromCol, toRow, toCol; };

bool landsOnRow4(const Move& m) { return m.toRow == 4; }

int main() {
    vector<Move> log = {{6, 4, 4, 4}, {0, 4, 2, 4}, {6, 3, 4, 3}};

    auto it = find_if(log.begin(), log.end(), landsOnRow4);
    if (it != log.end())
        cout << "Found move to row 4 at index " << (it - log.begin()) << endl;
    else
        cout << "No move to row 4.\n";
    return 0;
}
```

Sorting the log — by destination row, move number, or piece type — is the main algorithm topic; see §3 and §4.

> **Checkpoint §2**: Record moves, undo safely, walk the log, and search with `find_if` + end check.

***

## 3. Sorting Algorithms — Detailed Analysis and Comparison

### 3.1 Why Sorting Matters for the Move Log

| Use case | What sorting gives you | Typical n |
| --- | --- | --- |
| Analyze by landing row | Group moves reaching the same rank | 40–200 |
| Opening report | Order lines by first move | 100–500 |
| Engine move list | Rank candidates by evaluation score | 10–50 |
| Duplicate PGN lines | Equal entries become adjacent after sort | 1000+ |
| Club rating display | Top players first (same algorithm, different data) | 10–500 |

Sorting does **not** change which moves were played — it **reorders** the log (or a copy) for easier reading and binary search.

### 3.2 Big-O Basics (for Comparison)

| Notation | Growth intuition | Log example (n moves) |
| --- | --- | --- |
| **O(1)** | Constant — size does not matter | Read `log[i]` |
| **O(n)** | Double data → double time | Scan entire log once |
| **O(n log n)** | Efficient sort class | `std::sort` on full game |
| **O(n²)** | 10× data → ~100× time | Bubble sort on 10,000 plies |

**Reality check — comparison counts (approximate):**

| n | O(n²) comparisons | O(n log n) comparisons |
| --- | --- | --- |
| 10 | 100 | ~33 |
| 100 | 10,000 | ~664 |
| 1,000 | 1,000,000 | ~9,966 |
| 10,000 | 100,000,000 | ~132,877 |

For a **single game log** (n ≈ 80), even O(n²) feels instant. For **opening databases** or **rating lists**, O(n²) becomes unusable — that is why production code uses **`std::sort`**.

![Sort complexity](assets/ch12_sort_complexity.png)
*Figure 3: O(n²) classic sorts vs O(n log n) `std::sort`*

### 3.3 What Makes One Sort Different from Another?

When comparing algorithms, ask five questions:

1. **Best / average / worst time** — depends on input shape?
2. **Stable?** — do equal keys keep their original order?
3. **In-place?** — extra memory beyond a few variables?
4. **Comparisons vs swaps** — expensive if elements are large `Move` structs?
5. **Adaptive?** — faster when data is already nearly sorted?

### 3.4 Bubble Sort

**Idea**: Repeated passes; swap each adjacent out-of-order pair. After pass *i*, the *i* largest items sit at the end.

**Trace** on club ratings `{1500, 1200, 1800, 1350}`:

```
Initial:  [1500, 1200, 1800, 1350]
Pass 1:   [1200, 1500, 1350, 1800]   ← 1800 bubbled to end
Pass 2:   [1200, 1350, 1500, 1800]
Pass 3:   [1200, 1350, 1500, 1800]   ← no swaps, done
```

```cpp
void bubbleSort(vector<int>& v) {
    size_t n = v.size();
    for (size_t i = 0; i + 1 < n; ++i) {
        bool swapped = false;
        for (size_t j = 0; j + 1 < n - i; ++j) {
            if (v[j] > v[j + 1]) {
                swap(v[j], v[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;   // no swaps this pass — already sorted
    }
}
```

Each outer pass sets `swapped = false`. If the inner loop completes without any swap, the array is sorted and the algorithm **stops early** — best case O(n) instead of always running all n passes.

| Aspect | Analysis |
| --- | --- |
| Best case | O(n) — already sorted, one pass, no swaps |
| Average | O(n²) comparisons |
| Worst case | O(n²) — reverse sorted |
| Stable | Yes — equal elements never cross |
| In-place | Yes |
| Swaps | Up to O(n²) — costly for fat `Move` objects |
| Adaptive | **Yes** — stops when a pass performs zero swaps (`!swapped`) |
| Production? | **No** — teach only |

**When bubble sort still appears in conversation**: tiny n, hardware with swap-heavy teaching demos, or detecting “one pass = sorted” as a quick check.

### 3.5 Selection Sort

**Idea**: Split into sorted prefix (left) and unsorted suffix (right). Each pass pick the **minimum** of the unsorted part and swap it into position *i*.

**Trace** on `{1500, 1200, 1800, 1350}`:

```
Pass i=0: min at index 1 (1200) → swap with index 0 → [1200, 1500, 1800, 1350]
Pass i=1: min at index 3 (1350) → swap with index 1 → [1200, 1350, 1800, 1500]
Pass i=2: min at index 2 (1500) → already in place
Result:   [1200, 1350, 1500, 1800]
```

```cpp
void selectionSort(vector<int>& v) {
    size_t n = v.size();
    for (size_t i = 0; i + 1 < n; ++i) {
        size_t minIdx = i;
        for (size_t j = i + 1; j < n; ++j)
            if (v[j] < v[minIdx]) minIdx = j;
        if (minIdx != i) swap(v[i], v[minIdx]);
    }
}
```

| Aspect | Analysis |
| --- | --- |
| Best case | O(n²) — always scans unsorted region |
| Average | O(n²) |
| Worst case | O(n²) |
| Stable | **No** — swap can jump equal elements over each other |
| In-place | Yes |
| Swaps | At most **n − 1** — fewer than bubble for large structs |
| Adaptive | No |
| Production? | **No** |

**Bubble vs selection (summary):**

| Criterion | Bubble sort | Selection sort |
| --- | --- | --- |
| Comparisons | O(n²) | O(n²) |
| Swaps | O(n²) | O(n − 1) |
| Stable | Yes | No |
| Best on sorted input | O(n) | O(n²) |
| Good for fat `Move` | No (many swaps) | Slightly better |

### 3.6 Insertion Sort

**Idea**: Like sorting cards in your hand. For each index *i*, pull `v[i]` left into the already-sorted prefix.

**Trace** on `{1500, 1200, 1800, 1350}`:

```
Start:     [1500 | 1200, 1800, 1350]
Insert 1200: [1200, 1500 | 1800, 1350]
Insert 1800: [1200, 1500, 1800 | 1350]
Insert 1350: [1200, 1350, 1500, 1800]
```

```cpp
void insertionSort(vector<int>& v) {
    size_t n = v.size();
    for (size_t i = 1; i < n; ++i) {
        int key = v[i];
        size_t j = i;
        while (j > 0 && v[j - 1] > key) {
            v[j] = v[j - 1];
            --j;
        }
        v[j] = key;
    }
}
```

| Aspect | Analysis |
| --- | --- |
| Best case | O(n) — already sorted, inner while never runs |
| Average | O(n²) |
| Worst case | O(n²) — reverse sorted |
| Stable | Yes |
| In-place | Yes |
| Swaps | Shifts instead of swaps — still O(n²) work worst case |
| Adaptive | **Yes** — excellent on nearly sorted logs |
| Production? | Only tiny n or as subroutine inside `std::sort` |

**Insertion sort on move logs**: If you append moves chronologically and only need “almost sorted by row” after a few edits, insertion-style passes can be fast — but for general reordering, still use `std::sort`.

### 3.7 Quick Sort (Conceptual)

**Idea**: Pick a **pivot**, partition so left ≤ pivot ≤ right, recurse on both sides.

| Aspect | Analysis |
| --- | --- |
| Average | O(n log n) |
| Worst case | O(n²) — bad pivot choices on sorted input |
| Stable | No (typical in-place partition) |
| In-place | Yes |
| Production? | Core of many libraries, including `std::sort` hybrid |

You rarely call quicksort directly in application code; **`std::sort`** wraps an introspective variant (quicksort + heapsort fallback + insertion sort on small chunks).

### 3.8 `std::sort` and `stable_sort`

```cpp
#include <algorithm>
sort(log.begin(), log.end(), byDestRow);           // default production choice
stable_sort(log.begin(), log.end(), byDestRow);    // preserve order of equal keys
```

| Aspect | `std::sort` | `stable_sort` |
| --- | --- | --- |
| Average time | O(n log n) | O(n log n) |
| Worst time | O(n log n) — introspective | O(n log n) |
| Stable | **No** | **Yes** |
| Extra memory | O(log n) typical | O(n) possible |
| Use when | General sorting of move logs | Equal `toRow` must keep play order |

**Stability example on move log**: Two moves both land on row 4 — e4 then d4. After sorting by `toRow` only, `stable_sort` keeps e4 before d4 if their keys tie; plain `sort` may swap them.

### 3.9 Master Comparison Table

| Algorithm | Best | Average | Worst | Stable | In-place | Use in chess project |
| --- | --- | --- | --- | --- | --- | --- |
| Bubble sort | O(n) | O(n²) | O(n²) | Yes | Yes | Learn only |
| Selection sort | O(n²) | O(n²) | O(n²) | No | Yes | Learn only |
| Insertion sort | O(n) | O(n²) | O(n²) | Yes | Yes | Tiny n / nearly sorted |
| Quick sort | O(n log n) | O(n log n) | O(n²) | No | Yes | Via `std::sort` internals |
| **`std::sort`** | O(n log n) | O(n log n) | O(n log n) | No | Yes | **Default for move logs** |
| **`stable_sort`** | O(n log n) | O(n log n) | O(n log n) | Yes | No\* | Tie-break by move order |

\* `stable_sort` may use O(n) auxiliary memory depending on implementation.

### 3.10 Choosing a Sort — Decision Guide

```
flowchart TD
    A["Need to sort move log or ratings?"] --> B{"n > a few hundred?"}
    B -->|Yes| C["Use std::sort or stable_sort"]
    B -->|No, learning| D["Implement bubble/insertion once"]
    C --> E{"Equal keys must keep play order?"}
    E -->|Yes| F["stable_sort + comparator"]
    E -->|No| G["sort + comparator"]
    G --> H["O(n log n) — production default"]
    F --> I["O(n log n) — stable tie-breaking"]
```

**Rules of thumb:**

1. **Game log analysis (n ≤ 200)** — `std::sort` is always fast enough; clarity beats hand-rolled sort.
2. **Opening / PGN database (n ≥ 1000)** — never O(n²); profile if needed, but start with `std::sort`.
3. **Equal sort keys** — if two moves share `toRow`, use `stable_sort` when original chronological order must survive.
4. **Teaching / exams** — know bubble and insertion traces; explain *why* O(n²) fails at scale using the table in §3.2.

> **Checkpoint §3**: Compare bubble, selection, and insertion on stability, swaps, and best-case behavior; explain the `swapped` flag in bubble sort; justify `std::sort` for large logs.

***

## 4. Sorting the Move Log with `std::sort`

### 4.1 Comparator Design

To sort `Move` by landing row, write a **comparator** — returns `true` if `a` should appear **before** `b`:

```cpp
bool byDestRow(const Move& a, const Move& b) {
    return a.toRow < b.toRow;
}
```

For primary row and secondary column:

```cpp
bool byDestRowThenCol(const Move& a, const Move& b) {
    if (a.toRow != b.toRow) return a.toRow < b.toRow;
    return a.toCol < b.toCol;
}
```

### 4.2 Example — Sort Log Before Printing Report

```cpp
#include <algorithm>
#include <vector>
#include <iostream>
using namespace std;

struct Move { int fromRow, fromCol, toRow, toCol; };

bool byDestRow(const Move& a, const Move& b) {
    return a.toRow < b.toRow;
}

int main() {
    vector<Move> log = {{6,4,4,4}, {0,1,2,2}, {6,3,4,3}, {1,4,3,4}};

    sort(log.begin(), log.end(), byDestRow);

    cout << "Moves sorted by destination row:\n";
    for (const Move& m : log)
        cout << "  (" << m.fromRow << "," << m.fromCol
             << ") -> row " << m.toRow << ", col " << m.toCol << "\n";
    return 0;
}
```

**Before sort** (chronological): e4, Nc6, d4, …

**After sort** (by `toRow`): lower landing rows first — easier to tally how many moves hit each rank.

### 4.3 Descending Order (e.g. Club Ratings)

Same pattern — flip the comparison:

```cpp
bool ratingHigher(int a, int b) { return a > b; }
sort(ratings.begin(), ratings.end(), ratingHigher);
```

> **Checkpoint §4**: Sort `vector<Move>` with a custom comparator; pick `sort` vs `stable_sort` based on stability needs.

***

## 5. Defensive Programming and Exception Handling

A move log is written to, read from, searched, and sorted many times per game. **Defensive programming** means checking assumptions at the boundary — before bad data causes a crash, silent corruption, or undefined behavior.

### 5.1 The Core Idea — Validate at the Boundary

Put checks where data **enters** your log module: user input, replay index, imported PGN, undo button.

| Risky pattern on the log | Safer approach |
| --- | --- |
| `log[i]` with unknown `i` | `i < log.size()` or `log.at(i)` inside `try/catch` |
| `log.back()` | `if (!log.empty())` first |
| `log.pop_back()` on undo | `if (!log.empty())` — return `false` if nothing to undo |
| `*it` after `find_if` | `if (it != log.end())` before dereferencing |
| `addMove` with bad coordinates | Validate row/col in `[0, 7]` before `push_back` |
| `freq[m.toRow]++` in tally | Check `0 <= m.toRow < BOARD_SIZE` |

> **Plain English — undefined behavior**: With `log[i]` and invalid `i`, the program may crash immediately, corrupt memory, or appear to work — never rely on “it usually works.”

### 5.2 `operator[]` vs `at()` — Speed vs Safety

| Access | Bounds check? | On invalid index | When to use on log |
| --- | --- | --- | --- |
| `log[i]` | No | Undefined behavior | Inner loops when `i` is already validated |
| `log.at(i)` | Yes | Throws `std::out_of_range` | User-supplied replay move number |

```cpp
#include <vector>
#include <iostream>
#include <stdexcept>
using namespace std;

struct Move { int fromRow, fromCol, toRow, toCol; };

int main() {
    vector<Move> log = {{6, 4, 4, 4}, {0, 1, 2, 2}};
    int moveNumber;
    cout << "Replay move # (0-" << log.size() - 1 << "): ";
    cin >> moveNumber;

    try {
        const Move& m = log.at(moveNumber);
        cout << "Move lands on row " << m.toRow << endl;
    } catch (const out_of_range& e) {
        cout << "Invalid move number — log has " << log.size() << " moves.\n";
    }
    return 0;
}
```

> **Plain English — `try` / `catch`**: Code in the `try` block runs normally. If `at()` throws `out_of_range`, execution jumps to `catch` — you handle the error instead of crashing.

Include `<stdexcept>` when you catch standard exceptions by name.

### 5.3 How `try` / `catch` Works

When code in a `try` block **throws** an exception, normal execution stops and control jumps to the matching `catch` block. If nothing throws, the `catch` blocks are skipped.

```
flowchart TD
    A["Enter try block"] --> B{"Exception thrown?"}
    B -->|No| C["Continue after catch"]
    B -->|Yes| D["Jump to matching catch"]
    D --> E["Handle error — no crash"]
    E --> C
```

| Keyword | Role |
| --- | --- |
| `try` | Wrap code that might throw |
| `catch` | Handle a specific exception type (or any) |
| `throw` | Signal an error yourself (rare in beginner logs) |

You can chain multiple `catch` blocks — most specific first:

```cpp
try {
    const Move& m = log.at(index);
    cout << "Move to row " << m.toRow << endl;
} catch (const out_of_range& e) {
    cout << "Index out of range: " << e.what() << endl;
} catch (const exception& e) {
    cout << "Other standard error: " << e.what() << endl;
} catch (...) {
    cout << "Unknown error.\n";
}
```

`e.what()` returns a short message from the library — useful for debugging, not always shown to end users.

### 5.4 Example — Replay Move with `try` / `catch`

User-supplied replay index is a classic case for exceptions — you cannot know the value at compile time:

```cpp
#include <vector>
#include <iostream>
#include <stdexcept>
using namespace std;

struct Move { int fromRow, fromCol, toRow, toCol; };

void replayMove(const vector<Move>& log, int moveNumber) {
    try {
        const Move& m = log.at(moveNumber);
        cout << "Move #" << moveNumber << " lands on row "
             << m.toRow << ", col " << m.toCol << endl;
    } catch (const out_of_range& e) {
        cout << "Invalid move number. Log has "
             << log.size() << " moves (0-"
             << (log.empty() ? 0 : log.size() - 1) << ").\n";
    }
}

int main() {
    vector<Move> log = {{6, 4, 4, 4}, {0, 1, 2, 2}, {6, 3, 4, 3}};
    replayMove(log, 1);    // OK
    replayMove(log, 99);   // caught — program keeps running
    return 0;
}
```

Without `try/catch`, [`log.at`](http://log.at)`(99)` would **terminate** the program on many systems.

### 5.5 Example — Sort Report with Exception-Safe Access

When building a sorted report, you might read indices from a file or UI. Wrap access so one bad index does not abort the whole analysis:

```cpp
#include <algorithm>
#include <vector>
#include <iostream>
#include <stdexcept>
using namespace std;

struct Move { int fromRow, fromCol, toRow, toCol; };

bool byDestRow(const Move& a, const Move& b) {
    return a.toRow < b.toRow;
}

void printSortedReport(const vector<Move>& log, int highlightIndex) {
    vector<Move> copy = log;   // sort a copy — chronological log unchanged
    sort(copy.begin(), copy.end(), byDestRow);

    cout << "Sorted by destination row:\n";
    for (size_t i = 0; i < copy.size(); ++i)
        cout << "  [" << i << "] row " << copy[i].toRow << endl;

    try {
        const Move& h = copy.at(highlightIndex);
        cout << "Highlight: row " << h.toRow << endl;
    } catch (const out_of_range&) {
        cout << "Highlight index invalid — skipped.\n";
    }
}

int main() {
    vector<Move> log = {{6,4,4,4}, {0,1,2,2}, {6,3,4,3}};
    printSortedReport(log, 0);   // OK
    printSortedReport(log, 10);  // caught — report still printed
    return 0;
}
```

> **Design note**: Sorting uses `copy[i]` only after `i < copy.size()` in the loop — safe without exceptions. User-provided `highlightIndex` still needs `at()` + `catch` or a bounds `if`.

### 5.6 Guard Empty Logs — Undo and Last Move

`MoveLog::undoLast()` already returns `false` when empty. The same rule applies everywhere:

```cpp
bool undoLast(vector<Move>& log) {
    if (log.empty()) {
        cout << "Nothing to undo.\n";
        return false;
    }
    log.pop_back();
    return true;
}

void printLastMove(const vector<Move>& log) {
    if (log.empty()) {
        cout << "No moves yet.\n";
        return;
    }
    cout << "Last move to row " << log.back().toRow << endl;
}
```

**Design choice**: For undo and “show last move,” an **if-check** is clearer than an exception — an empty log is a normal state, not a failure.

### 5.7 Validate Coordinates Before Recording

Reject illegal squares before they enter the log:

```cpp
const int BOARD_SIZE = 8;

bool isValidSquare(int row, int col) {
    return row >= 0 && row < BOARD_SIZE &&
           col >= 0 && col < BOARD_SIZE;
}

bool addMoveSafe(vector<Move>& log, const Move& m) {
    if (!isValidSquare(m.fromRow, m.fromCol) ||
        !isValidSquare(m.toRow, m.toCol)) {
        cout << "Rejected: coordinates out of range.\n";
        return false;
    }
    log.push_back(m);
    return true;
}
```

This keeps invalid data out of sort, search, and frequency tally — downstream code stays simpler.

### 5.8 Search Results — Always Check Before Dereference

```cpp
auto it = find_if(log.begin(), log.end(), landsOnRow4);

if (it != log.end()) {
    cout << "Found at index " << (it - log.begin()) << endl;
} else {
    cout << "No matching move — do not use *it.\n";
}
```

Dereferencing `log.end()` is as dangerous as `log[log.size()]`.

### 5.9 When to Use Exceptions vs Plain `if`

| Situation | Recommended approach | Example on log |
| --- | --- | --- |
| Expected “not found” | `if (it != log.end())` | Search by destination row |
| Empty log on undo | `if (!log.empty())` | Undo button |
| User types invalid replay index | `try/catch` on `at()` | Jump to move 99 in 40-move game |
| Invalid square from UI | Validate, return `false` | `addMoveSafe` |
| Programmer bug (should never happen) | Fix the code; assert in debug | Loop index `i < log.size()` |

> **Rule of thumb**: Use **exceptions** for unexpected input you cannot prevent at compile time (bad index into `at()`). Use **if-checks** for normal control flow (empty log, search miss).

### 5.10 Defensive `MoveLog` — Putting It Together

Extend the log class so callers get safe behavior by default:

```cpp
// chess/move_log.h (excerpt)
class MoveLog {
public:
    bool addMove(int fromRow, int fromCol, int toRow, int toCol);
    bool undoLast();
    int getCount() const;
    bool getMoveAt(int index, Move& out) const;  // safe replay access

private:
    std::vector<Move> moves_;
};
```

```cpp
// chess/move_log.cpp (excerpt)
bool MoveLog::addMove(int fr, int fc, int tr, int tc) {
    Move m{fr, fc, tr, tc};
    if (!isValidSquare(m.fromRow, m.fromCol) ||
        !isValidSquare(m.toRow, m.toCol))
        return false;
    moves_.push_back(m);
    return true;
}

bool MoveLog::getMoveAt(int index, Move& out) const {
    if (index < 0 || index >= static_cast<int>(moves_.size()))
        return false;
    out = moves_.at(index);   // or moves_[index] after check above
    return true;
}
```

`getMoveAt` returns `false` instead of throwing — friendly for game UI that shows “invalid move number” without exception overhead.

### 5.11 Defensive Checklist for the Chess Project

| Location | Check |
| --- | --- |
| Record move | `isValidSquare` on from/to |
| Undo | `!log.empty()` before `pop_back()` |
| Replay by index | Bounds check or `at()` + `catch` |
| `find_if` result | `it != log.end()` before `*it` |
| Row frequency tally | `0 <= m.toRow < BOARD_SIZE` |
| Sort / analyze | Log is non-empty or handle empty case in report |

> **Checkpoint §5**: Explain the difference between `log[i]` and [`log.at`](http://log.at)`(i)`; show safe undo, safe search, and when to use `try/catch` vs `if`.

***

## 6. Summary and Common Mistakes

### Key Ideas

- Design the **move log** as `vector<Move>` (or `MoveLog` wrapper) — append, undo, iterate, search.
- **Iterators** connect the log to STL algorithms via `[begin, end)`.
- **Classic sorts** teach O(n²) vs O(n log n); **`std::sort`** is the production default.
- **`stable_sort`** when equal `toRow` values must keep chronological order.
- **Defensive programming**: validate coordinates, guard empty logs, check search results; use `at()` + `try/catch` for user-supplied indices.
- **Exception handling**: `try` / `catch` keeps replay and report code running after a bad index; chain catches from specific to general.

### Log & Sort Quick Reference

| Task | Approach |
| --- | --- |
| Record move | `push_back` after coordinate check |
| Undo | `pop_back` after `empty()` check |
| Replay by index | `at(i)` + `catch`, or `getMoveAt` |
| Find by condition | `find_if` + `it != end` |
| Sort by landing row | `sort(log.begin(), log.end(), cmp)` |
| Keep tie order | `stable_sort` |
| User replay index | `log.at(i)` inside `try/catch` |

### Common Mistakes

| Mistake | Correct approach |
| --- | --- |
| Fixed array for game log | `vector<Move>` |
| `pop_back()` on empty log | Check `empty()` first |
| `log[i]` with unchecked `i` | Validate index or use `at()` + `catch` |
| Dereference failed `find_if` | Always `if (it != log.end())` |
| Store move with row/col = 9 | Validate with `isValidSquare` first |
| Hand bubble sort on 10k+ lines | `std::sort` |
| Expect `sort` to be stable | Use `stable_sort` |
| Missing `#include <algorithm>` | Add header for `sort` / `find_if` |
| Missing `#include <stdexcept>` | Add when catching `out_of_range` |
| Uncaught exception from `at()` | Wrap in `try/catch` or validate index first |

***

*End of Chapter 12*
