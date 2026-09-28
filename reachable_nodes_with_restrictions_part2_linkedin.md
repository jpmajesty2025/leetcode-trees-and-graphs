# Zero-Graph Tree Pruning: Reachability with Disjoint Set Union 🌲⚡

In Part 1, we eliminated redundant dual-set lookups by pre-marking restricted nodes into a unified boolean array.

Now consider this alternative perspective:
*What if we skip building the tree altogether and model reachability as component connectivity?*

By filtering the raw edge list before building any data structure, **Disjoint Set Union (DSU / Union-Find)** solves the problem directly.

---

### 💡 The Strategy: Edge Filtering + Component Sizing

1️⃣ **Filter Restricted Edges**:
Convert `restricted` to a set for $O(1)$ edge validation. Any edge connecting to or from a restricted node is completely discarded:
```python
restricted_set = set(restricted)
for u, v in edges:
    if u not in restricted_set and v not in restricted_set:
        uf.union(u, v)
```

2️⃣ **Union by Size**:
Each disjoint set tracks the size of its connected component:
```python
if self.size[root_x] < self.size[root_y]:
    self.parent[root_x] = root_y
    self.size[root_y] += self.size[root_x]
else:
    self.parent[root_y] = root_x
    self.size[root_x] += self.size[root_y]
```

3️⃣ **Instant Result**:
The answer is simply the component size containing node `0`:
`return uf.get_size(0)`

---

### ⚡ Complexity & Architectural Comparison

| Dimension | Unified BFS / DFS Traversal | Disjoint Set Union (DSU) |
| :--- | :--- | :--- |
| **Tree Adjacency Allocation** | Required ($\mathcal{O}(N)$ space) | **Zero (Filters edges on-the-fly)** |
| **Time Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(N \cdot \alpha(N))$ |
| **Auxiliary Memory** | $\mathcal{O}(N)$ adjacency + queue | **$\mathcal{O}(N)$ parent & size arrays** |
| **Dynamic Edge Additions** | Re-run traversal $\mathcal{O}(N)$ | $\mathcal{O}(\alpha(N))$ incremental merge |

---

### 🎯 Key Engineering Takeaways

• **Unified BFS/DFS** is optimal for static, one-pass reachability queries with minimal constant factors.
• **Union-Find by Size** shines when processing streaming edges, dynamic barrier removals, or when avoiding graph allocation entirely.

Check out the clean, modular Union-Find implementation in the attached image! 📸

How often do you reach for edge-filtering with DSU in graph modeling? Let's discuss below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CodingInterview
