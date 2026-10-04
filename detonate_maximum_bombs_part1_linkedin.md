# Directed Chain Reactions: Avoiding the Floating-Point Trap 💣⚡

Given: `n` bombs, each with a location `(x, y)` and blast radius `r`.

Detonating a bomb triggers a chain reaction that detonates all bombs within its circular blast zone.

If we can only manually trigger ONE bomb, what is the maximum number of bombs we can detonate?

---

### 🚨 Pitfall 1: Asymmetric Edge Direction

A common mistake is treating bomb connectivity as an undirected graph:
• Bomb A might have a huge radius `rA = 100` that easily covers Bomb B.
• But Bomb B might only have `rB = 1` and cannot reach Bomb A!

Because connectivity is **directed and asymmetric**, we cannot simply use Disjoint Set Union (Union-Find) or undirected components. This requires finding the maximum reachable set in a **Directed Graph**.

---

### 🚨 Pitfall 2: The Floating-Point `sqrt` Trap

When determining if Bomb B is within Bomb A's radius:
```python
# ❌ DANGEROUS: Floating-point precision loss + CPU penalty
distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
if distance <= r1:
    graph[i].append(j)
```

Floating-point square roots can introduce subtle precision errors near boundary conditions.

**The Fix**: Use exact integer squared distance arithmetic:
```python
# ✅ SAFE & FAST: Exact integer arithmetic
dx = x1 - x2
dy = y1 - y2
if dx * dx + dy * dy <= r1 * r1:
    graph[i].append(j)
```

---

### 💡 Multi-Source BFS with Short-Circuiting

1. Build a directed adjacency list `graph` where edge `i -> j` exists if `dist_sq(i, j) <= ri^2`.
2. Run Breadth-First Search (BFS) starting from each bomb `i = 0, ..., n - 1` to count all reachable nodes.
3. **Early Exit**: If any BFS detonates all `n` bombs, immediately return `n`!

---

### ⚖️ Algorithm Complexity

| Metric | Multi-Source BFS |
| :--- | :--- |
| **Graph Construction** | **O(N^2)** pairwise integer distance checks |
| **Traversal Time** | **O(N * (V + E)) = O(N^3)** in worst-case dense graph |
| **Auxiliary Space** | **O(N^2)** for directed adjacency lists + visited sets |
| **Early Exit Optimization** | **O(1) best case** if starting bomb triggers full chain |

---

In Part 2 tomorrow, we’ll explore **Bitset Transitive Closure to accelerate reachability using 64-bit CPU parallelism!**

How do you handle geometric precision and asymmetric relations in graph models? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #GraphTheory #SystemDesign
