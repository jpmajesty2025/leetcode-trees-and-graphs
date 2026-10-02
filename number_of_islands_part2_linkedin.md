# From 2D Grids to 1D Disjoint Sets: Solving Number of Islands with Union-Find 🏝️🔗

In Part 1, we tackled stack safety and memory optimization with DFS and BFS. But what if the landscape isn't static?

What if land cells are added one by one over time, and you need to report the number of islands after each addition?

Running DFS or BFS from scratch after every new cell would take $\mathcal{O}(K \times M \times N)$ time.

This is where **2D Disjoint Set Union (DSU / Union-Find)** shines.

---

### 💡 The Core Techniques for 2D Union-Find:

1️⃣ **2D Coordinate Flattening**:
To map a 2D matrix cell $(r, c)$ into a 1D Disjoint Set array of size $M \times N$:
$$\text{index} = r \times \text{cols} + c$$

2️⃣ **Deduplicated Neighbor Unions**:
Because connectivity is undirected, iterating over all 4 directions performs duplicate `union()` operations. You only need to merge with **Right** $(r, c+1)$ and **Down** $(r+1, c)$ neighbors! For instance, when $r = 0$, the algorithm will inspect the cell below, row 1, to see if it is a neignboring bit of land in need of a merge. In a later iteration, when $r = 1$, there is no need to look above to row 0, to check if the cell above is a land neighbor - this would be duplicate work! So we need only work our way down and to the right, starting from the upper left grid corner.

3️⃣ **Component Tracking in $\mathcal{O}(1)$**:
• Initialize `count` to the total number of `'1'` cells.
• Each successful `union()` decrements `count` by 1.

---

### ⚡ Near-Linear Performance

With **Path Compression** and **Union by Rank**, any sequence of $K$ operations runs in:
$$\mathcal{O}(K \cdot \alpha(M \times N))$$
where $\alpha$ is the Inverse Ackermann function ($\le 4$ for all realistic inputs).

---

### 📊 When to Choose Traversal vs. Union-Find

| Scenario | Recommended Strategy | Why? |
| :--- | :--- | :--- |
| **Static Grid (One-Time Query)** | **Iterative BFS / DFS** | Lower constant factors, zero class boilerplate |
| **Dynamic / Streaming Land Additions** | **2D Union-Find** | Incremental $\mathcal{O}(\alpha(N))$ component updates per edge |
| **Distributed / Parallel Processing** | **2D Union-Find** | Subgrids can be solved locally and merged along boundaries |

---

Have you used coordinate flattening for grid-based graph algorithms before? Drop your thoughts below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #UnionFind #LeetCode #SystemDesign #CodingInterview
