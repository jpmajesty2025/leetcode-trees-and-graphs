# Contaminated Trees: The O(N) Query Anti-Pattern & Hash Set Precomputation 🌲⚡

We are given a tree whose values have been wiped to `-1` and need to recover it following these rules:
• `root.val = 0`
• `left.val = 2 * parent.val + 1`
• `right.val = 2 * parent.val + 2`

Once recovered, the class must answer repeated queries: `find(target) -> bool`.

A common pitfall is writing `find()` as an on-demand tree search:
`return self._find(root, target)`

Why is this an architectural bottleneck?

---

### 🚨 The Hidden $O(Q \cdot N)$ Query Churn

If your system receives $Q = 10,000$ queries on a tree of $N = 10,000$ nodes:
1️⃣ Searching the tree on every query costs $\mathcal{O}(N)$ per call.
2️⃣ Total runtime explodes to $\mathcal{O}(Q \cdot N) = 10^8$ operations, leading to Time Limit Exceeded (TLE) errors and high latency.

---

### 💡 The Clean Optimization: Precomputed Hash Set

Shift the work to initialization (`__init__`):
1. Traverse the tree once during construction ($\mathcal{O}(N)$ time).
2. Assign recovered values and store each encountered value in a hash set `self.seen: set[int]`.
3. Answering `find(target)` reduces to a simple set membership check: `return target in self.seen`.

• **Query Latency**: Drops from $\mathcal{O}(N)$ down to instant $\mathbf{O(1)}$ average time.
• **Iterative BFS Option**: Level-order recovery with `collections.deque` ensures complete stack safety on deep or skewed trees ($H > 1,000$).

---

### ⚖️ Performance Comparison

| Metric | On-Demand Tree Search | Precomputed Hash Set (DFS / BFS) |
| :--- | :--- | :--- |
| **Initialization Time** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| **Query Time (`find`)** | $\mathcal{O}(N)$ per query (Sluggish) | **$\mathcal{O}(1)$ Instant** |
| **Total Time ($Q$ Queries)**| $\mathcal{O}(Q \cdot N) \approx 10^8$ ops | **$\mathcal{O}(N + Q) \approx 2 \times 10^4$ ops** |
| **Auxiliary Memory** | $\mathcal{O}(1)$ extra | $\mathcal{O}(N)$ set |

---

In Part 2 tomorrow, we’ll uncover the **hidden Binary Heap property** that allows navigating directly to `target` in $\mathcal{O}(\log(\text{target}))$ time with **ZERO extra hash set memory!**

Do you prefer upfront precomputation or on-demand lazy evaluation in your services? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #SystemDesign #ComputerScience
