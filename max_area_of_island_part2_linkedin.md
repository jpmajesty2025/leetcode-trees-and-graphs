# Dynamic Area Aggregation: Solving Max Area of Island with 2D Union-Find by Size 🏝️⚡

In Part 1, we optimized DFS & BFS grid traversal to eliminate duplicate stack allocations.

Now consider this scenario:
*What if land cells are added dynamically to a grid, and you need to query the maximum island area after every update?*

Re-running DFS/BFS from scratch after every cell takes $\mathcal{O}(M \times N)$ per query.

With **2D Disjoint Set Union (Union-Find) weighted by size**, area tracking becomes instantaneous.

---

### 💡 The Core Mechanism: Union by Size & Dynamic Max

1️⃣ **2D Coordinate Flattening**:
Map each grid cell $(r, c)$ into a 1D index:
$$\text{idx} = r \times \text{cols} + c$$

2️⃣ **Size Tracking Array**:
• Initialize `size[idx] = 1` for every land cell `'1'`.
• Maintain a global `max_size = 1` (or `0` if all water).

3️⃣ **Size Merging Logic**:
When uniting components rooted at `root_x` and `root_y`:
```python
if self.size[root_x] < self.size[root_y]:
    self.parent[root_x] = root_y
    self.size[root_y] += self.size[root_x]
    self.max_size = max(self.max_size, self.size[root_y])
else:
    self.parent[root_y] = root_x
    self.size[root_x] += self.size[root_y]
    self.max_size = max(self.max_size, self.size[root_x])
```

4️⃣ **Directional Deduplication**:
Since grid edges are undirected, you only need to union each land cell with its **Right** $(r, c+1)$ and **Down** $(r+1, c)$ neighbors!

---

### ⚡ Complexity Comparison

| Dimension | Traversal (DFS / BFS) | 2D Union-Find by Size |
| :--- | :--- | :--- |
| **Static Grid Query** | $\mathcal{O}(M \times N)$ | $\mathcal{O}(M \times N \cdot \alpha(MN))$ |
| **Dynamic Land Addition** | $\mathcal{O}(M \times N)$ per query | **$\mathcal{O}(\alpha(MN))$ instantaneous** |
| **Auxiliary Memory** | $\mathcal{O}(M \times N)$ visited matrix | $\mathcal{O}(M \times N)$ parent & size |

---

### 🎯 Key Engineering Takeaways

• For static one-off checks, iterative BFS/DFS has zero class boilerplate.
• For streaming land updates, dynamic clustering, or partition management, **Union-Find by Size** maintains maximum component metrics in near-constant amortized time.

Check out the modular 2D Union-Find implementation in the attached image! 📸

Have you implemented Union by Size for weighted graph clustering? Let's discuss in the comments! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CodingInterview
