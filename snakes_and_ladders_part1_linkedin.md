# Snakes and Ladders: Escaping 2D Boustrophedon Math with 1D Board Pre-Flattening 🎲⚡

We are asked to find the minimum number of 6-sided dice rolls required to navigate from square $1$ to square $n^2$ of an $n x n$ game board.

The board is numbered $1 \dots n^2$ in **Boustrophedon style**:
• Starting at bottom-left `board[n - 1][0]`.
• Moving right across the bottom row.
• Alternating direction (left-to-right, right-to-left) with each ascending row.

Some developers evaluate this 2D coordinate conversion inside the core search loop:
`r, c = divmod(next_square - 1, n)`
`row = n - 1 - r`
`col = c if (r % 2 == 0) else (n - 1 - c)`

But, calculating 2D coordinates inside your search loop an anti-pattern!

---

### 🚨 The Overhead of Repeated Coordinate Arithmetic

With up to 6 die roll outcomes per state:
• Every potential move recomputes integer division, modulo operations, and branching logic.
• In a grid of $N = 20$ ($400$ cells), you execute thousands of redundant arithmetic operations during graph exploration!

---

### 💡 The High-Performance Fix: 1D Board Pre-Flattening

Instead of translating 2D indices on every die roll, **flatten the board into a 1D lookup array upfront** in $\mathcal{O}(N^2)$ time!

1️⃣ **One-Time Pre-Pass**:
• Scan rows bottom-to-top, toggling a `left_to_right` boolean flag.
• Store values in a flat 1D array: `flat_board[1 ... n^2]`.

2️⃣ **Ultra-Fast 1D BFS**:
• The BFS state becomes a pure integer `curr` from $1$ to $n^2$.
• Transition logic simplifies to a simple 1D index lookup:
  `dest = flat_board[curr + roll]`

Zero division, zero modulo, and zero branch mispredictions inside the hot search loop!

---

### ⚖️ Performance Comparison

| Metric | On-The-Fly 2D Math | 1D Board Pre-Flattening |
| :--- | :--- | :--- |
| **Coordinate Calculations** | $6 \times$ per BFS expansion | **Single initial pre-pass ($\mathcal{O}(N^2)$)** |
| **Inner Loop Logic** | `divmod`, row invert, col parity | **Direct array index: `flat_board[sq]`** |
| **Time Complexity** | $\mathcal{O}(N^2)$ | $\mathbf{O(N^2)}$ **(Significantly lower constant factor)** |
| **Code Readability** | Complex index transformations | **Clean, linear graph transitions** |

---

In Part 2 tomorrow, we’ll explore how to **model game rules and teleportation mechanics as directed unweighted graphs with BFS!**

Do you pre-flatten complex game boards or compute coordinates dynamically? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #BFS #LeetCode #CleanCode #SystemDesign #ComputerScience
