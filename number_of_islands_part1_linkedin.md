# Number of Islands: The Hidden Recursion Trap in 2D Grid Traversal 🏝️⚡

When asked to count connected components on a 2D grid (LeetCode 200: "Number of Islands"), most engineers reach for recursive DFS:

```python
def dfs(r, c):
    visited[r][c] = True
    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
        # recurse into neighbors...
```

It is concise and readable. But what happens in production when your grid isn't a small toy example?

---

### 🚨 The Hidden Bug: `RecursionError`

Python's default recursion limit is `1,000`.

If you have a $300 \times 300$ grid ($90,000$ cells) containing a single serpentine, spiral, or large solid island, recursive DFS will exceed the call-stack limit and crash:
`RecursionError: maximum recursion depth exceeded`

You *could* increase `sys.setrecursionlimit()`, but in production systems, relying on OS call-stack expansion risks segmentation faults.

---

### 💡 Two Stack-Safe Alternatives:

1️⃣ **Iterative BFS (Optimal Peak Memory)**
• Uses a heap-allocated `collections.deque`.
• Marks cells as visited **immediately upon enqueueing** (preventing duplicate queue entries).
• **Peak Auxiliary Space:** Bounded by the perimeter of the wavefront — $\mathcal{O}(\min(M, N))$ on average, far better than DFS's $\mathcal{O}(M \times N)$ worst-case stack.

2️⃣ **Iterative DFS with Explicit Stack**
• Uses a Python list `stack = [(r, c)]` on the heap.
• Completely immune to Python call-stack overflow while retaining depth-first exploration order.

---

### ⚖️ Traversal Trade-Offs

| Approach | Time Complexity | Aux Space | Stack Safety |
| :--- | :--- | :--- | :--- |
| **Recursive DFS** | $\mathcal{O}(M \times N)$ | $\mathcal{O}(M \times N)$ call stack | ❌ Fails on deep/spiral paths ($>1,000$ cells) |
| **Iterative DFS** | $\mathcal{O}(M \times N)$ | $\mathcal{O}(M \times N)$ heap stack | ✅ 100% Stack-Safe |
| **Iterative BFS** | $\mathcal{O}(M \times N)$ | $\mathcal{O}(\min(M, N))$ queue | ✅ 100% Stack-Safe + Memory-Efficient |

---

Check out the clean implementations in the attached snippet! 📸

In Part 2 tomorrow, we’ll explore how to model 2D grids with **Disjoint Set Union (Union-Find)** for dynamic, streaming land additions.

Do you default to BFS or DFS when exploring matrices? Let's discuss in the comments! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #ComputerScience
