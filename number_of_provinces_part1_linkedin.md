# Adjacency Matrix to Adjacency List: Are You Accidentally Blowing Up Auxiliary Space? 🌐💾

When solving connected component problems like "Number of Provinces" (LeetCode 547), the standard input is an $n \times n$ adjacency matrix (`isConnected`).

A common instinct is to immediately convert it:
`graph = defaultdict(list)`

It feels clean, but look closer at the trade-off:
❌ In a dense graph, building an explicit adjacency list allocates $\mathcal{O}(N^2)$ auxiliary memory.
❌ It introduces hash map and dynamic list allocation overhead before traversal even starts.

---

### 💡 The Fix: Direct Matrix Traversal in $\mathcal{O}(N)$ Space

Since the matrix already provides $\mathcal{O}(1)$ neighbor lookups, you can traverse it directly:

1️⃣ **Direct DFS**
• Iterate through the node's row: `if isConnected[curr][neighbor] == 1 and not visited[neighbor]`
• Tracks components with a flat `visited = [False] * n` array.
• **Complexity:** $\mathcal{O}(N^2)$ time, $\mathcal{O}(N)$ call-stack space.

2️⃣ **Iterative BFS (Stack-Safe)**
• Employs `collections.deque` for FIFO queue management.
• Eliminates any risk of `RecursionError` on large or deep graphs without manual recursion limit tweaks.
• **Complexity:** $\mathcal{O}(N^2)$ time, $\mathcal{O}(N)$ heap-allocated queue space.

---

### ⚖️ Trade-off Summary

| Approach | Time Complexity | Auxiliary Space | Key Advantage |
| :--- | :--- | :--- | :--- |
| **Adjacency List + DFS** | $\mathcal{O}(N^2)$ | $\mathcal{O}(N^2)$ | Familiar representation |
| **Direct Matrix DFS** | $\mathcal{O}(N^2)$ | $\mathcal{O}(N)$ | Minimal boilerplate, memory optimal |
| **Iterative Matrix BFS** | $\mathcal{O}(N^2)$ | $\mathcal{O}(N)$ | Stack-safe on deep graphs |

---

Check out the clean implementation in the attached code snippet! 📸

In Part 2 tomorrow, we’ll look at why you might choose Disjoint Set Union (Union-Find) instead of traversal when edges arrive as a dynamic stream.

Do you default to DFS or BFS for component counting in interviews? Let's discuss below! 👇

#SoftwareEngineering #Python #Algorithms #DataStructures #LeetCode #CleanCode #ComputerScience
