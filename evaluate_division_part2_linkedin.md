# Scaling to O(1) Queries: The Power of Weighted Union-Find ➗🧙‍♂️

In Part 1, we answered division queries using graph DFS traversals in O(Q * N) time.

*Can we evaluate arbitrary ratio queries in O(1) amortized time without traversing any graph paths at query time?*

Yes! Using **Weighted Disjoint Set Union (Weighted Union-Find)**.

---

### 💡 The Weighted DSU Model

In standard Union-Find, we only track connectivity. In **Weighted DSU**, every node also tracks its **multiplicative ratio relative to its parent**:
`weight[x] = x / parent[x]`

1️⃣ **Path Compression with Multiplier Updates**:
• When flattening paths in `find(x)`, we recursively multiply ratios:
  `weight[x] = weight[x] * weight[original_parent]`
• After `find(x)`, `weight[x]` holds the direct ratio to the component's root: `x / root`.

2️⃣ **Union with Relative Offset**:
• Given equation `a / b = val` (so `a = b * val`):
• Let `root_a = find(a)` and `root_b = find(b)`.
• Merging `parent[root_a] = root_b` sets:
  `weight[root_a] = (weight[b] * val) / weight[a]`

---

### ⚡ Answering Queries in O(1) Time

To answer query `c / d`:
1. If `find(c) != find(d)` (different components), return `-1.0`.
2. If they share a root:
   `c / d = (c / root) / (d / root) = weight[c] / weight[d]`

A single division of pre-computed root weights answers the query in **O(1) time**!

---

### 📊 Complexity Comparison

| Dimension | Graph DFS / BFS | Weighted Union-Find |
| :--- | :--- | :--- |
| **Preprocessing Time** | O(N) | O(N * α(N)) |
| **Per-Query Complexity** | O(N) linear scan | **O(1) amortized (O(α(N)))** |
| **Total Runtime (Q queries)** | O(N + Q * N) | **O((N + Q) * α(N))** |
| **Auxiliary Memory** | O(N) graph + stack | **O(N) parent + weight arrays** |

---

### 🎯 Key Engineering Takeaways

• **Scale Shift**: When query volume dominates (Q >> N), shifting computation to an augmented DSU structure yields massive performance gains.
• **Weighted Compression**: Any associative operation (multiplication, addition, XOR) can be integrated into DSU path compression.

Have you used weighted DSU in production constraint systems? Let's discuss below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #UnionFind #SystemDesign
