# Graph Pathfinding at Scale: Avoiding the Duplicate Stack Ingestion Trap 🌐⚡

When checking if a path exists between two nodes in an undirected graph (LeetCode 1971: $N \le 200,000$, $|E| \le 200,000$), what data structures and traversal guards do you reach for?

A common implementation pattern looks like this:
```python
# ❌ SUBOPTIMAL: Pushes unvisited/queued neighbors repeatedly
while stack:
    curr = stack.pop()
    if curr not in visited:
        visited.add(curr)
        stack.extend(graph[curr])  # Stacks up duplicate nodes!
```

---

### 🚨 Why This Causes Performance & Memory Degradation

1️⃣ **Redundant Stack Bloat**: In dense or star topologies, nodes can be pushed to the stack dozens or hundreds of times before being popped. Peak stack memory degrades to $\mathcal{O}(E)$ instead of $\mathcal{O}(V)$.
2️⃣ **Hashing Overhead**: Constructing `graph = {i: [] for i in range(n)}` and `visited = set()` on $200,000$ integer keys triggers heavy dynamic memory allocations and hash table lookups.

---

### 💡 The Fix: High-Performance Iterative Traversal

1️⃣ **Contiguous Memory Arrays**:
• Use `graph: list[list[int]] = [[] for _ in range(n)]`
• Track visited states with a flat `visited = [False] * n` boolean array ($3\times\text{--}5\times$ faster than `set`).

2️⃣ **Mark on Ingestion + Early Exit**:
• Flag `visited[neighbor] = True` **immediately upon pushing or enqueueing**, guaranteeing each vertex enters the stack/queue at most once.
• Check `if neighbor == destination: return True` right at exploration time to terminate instantly without exploring unrelated subgraphs.

---

### ⚖️ Traversal Comparison

| Metric | Unchecked Stack DFS | Optimized Iterative DFS | Iterative BFS |
| :--- | :--- | :--- | :--- |
| **Max Queue/Stack Size** | $\mathcal{O}(E)$ (Redundant) | $\mathcal{O}(V)$ (Optimal) | $\mathcal{O}(V)$ (Optimal) |
| **Visited Lookup** | `set()` Hash Overhead | `[False] * n` $\mathcal{O}(1)$ Direct | `[False] * n` $\mathcal{O}(1)$ Direct |
| **Early Termination** | On pop | Immediate on discovery | Immediate on discovery |

---

Check out the clean implementations in the attached snippet! 📸

In Part 2 tomorrow, we’ll look at how **Disjoint Set Union (Union-Find)** eliminates adjacency list allocation entirely to solve path queries in $\mathcal{O}(V)$ auxiliary memory.

Do you prefer DFS or BFS when finding paths in large graphs? Let's discuss below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #ComputerScience
