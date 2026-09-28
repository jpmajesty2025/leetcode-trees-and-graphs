# 8-Directional Shortest Paths: Why BFS Wins & The Tuple Hashing Trap 🧭⚡

When finding the shortest clear path in an $N \times N$ binary grid (LeetCode 1091), what algorithm and state management do you choose?

A common instinct is writing BFS with a set of visited tuples:
```python
# ⚠️ Common Pattern: Tuple hashing in set
seen = {(0, 0)}
queue = deque([(0, 0, 1)])
```

While correct, let's examine the mechanics and low-level performance traps:

---

### 🚨 Why BFS is Non-Negotiable (and DFS Fails)

In an unweighted graph where every step has cost 1:
• **DFS** explores deep branches arbitrarily, meaning you must explore *all* exponential paths to prove optimality ($\mathcal{O}(8^{N^2})$ without memoization).
• **BFS** explores in concentric wavefronts. The **first time** BFS encounters the destination `(N-1, N-1)`, the path length is mathematically guaranteed to be minimal.

---

### 💡 3 Key Optimizations That 3x Your BFS Speed

1️⃣ **8-Directional Diagonal Shortcuts**:
Because diagonal movement is permitted, the minimum theoretical path across an $N \times N$ open grid is strictly $N$ steps (straight down the main diagonal), compared to $2N - 1$ steps in 4-directional grids!

2️⃣ **Eliminating Tuple Hashing Overhead**:
Hashing `(r, c)` tuples on every neighbor inspection creates memory churn. A flat 2D boolean array `visited = [[False] * n for _ in range(n)]` delivers instant $O(1)$ memory lookups.

3️⃣ **Enqueue-Time Target Verification**:
Check `if nr == n - 1 and nc == n - 1: return steps + 1` **before appending to the queue**, terminating the search an entire level earlier.

---

### ⚖️ Complexity Summary

| Metric | Standard Set BFS | Optimized 2D-Array BFS |
| :--- | :--- | :--- |
| **Time Complexity** | $\mathcal{O}(N^2)$ | $\mathcal{O}(N^2)$ (Faster constant factor) |
| **Auxiliary Memory** | $\mathcal{O}(N^2)$ + Tuple overhead | $\mathcal{O}(N^2)$ contiguous array |
| **Termination Check** | On pop from queue | **Immediate on enqueue** |

---

Check out the clean implementation in the attached snippet! 📸

In Part 2 tomorrow, we’ll explore how **Bidirectional BFS** and **A\* Search with Chebyshev Distance** drastically cut down explored state spaces!

Do you default to 2D arrays or hash sets when marking matrix visits? Let's discuss below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #ComputerScience
