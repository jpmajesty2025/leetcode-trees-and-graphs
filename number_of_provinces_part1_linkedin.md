# Adjacency Matrix into Adjacency List: Are You Accidentally Blowing Up Auxiliary Space? 🌐💾

**The Problem:**
There are n cities. A province is a group of directly or indirectly connected cities and no other 
cities outside of the group. You are given an n x n matrix isConnected where 
isConnected[i][j] = isConnected[j][i] = 1 if the ith city and the jth city are directly connected, 
and isConnected[i][j] = 0 otherwise. Return the total number of provinces.

With connected component problems like this, the standard input is an adjacency matrix. Maybe your instinct is to convert it to an adjacency list. It feels clean, but consider the trade-offs:
❌ In a dense graph, building an explicit adjacency list allocates $\mathcal{O}(N^2)$ auxiliary memory.
❌ It introduces hash map and dynamic list allocation overhead before traversal even starts.

---

### 💡 The Smart Alternative: Direct Matrix Traversal in $\mathcal{O}(N)$ Space

Since the matrix already provides $\mathcal{O}(1)$ neighbor lookups, you can traverse it directly:

1️⃣ **Direct Recursive DFS**
• Iterate through the node's row: `if isConnected[curr][neighbor] == 1 and not visited[neighbor]`
• Tracks components with a flat `visited = [False] * n` array.
• **Complexity:** $\mathcal{O}(N^2)$ time, $\mathcal{O}(N)$ call-stack space.

2️⃣ **Iterative BFS (Stack-Safe)**
• Employs a `deque` for FIFO queue management.
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

In Part 2 tomorrow, we’ll look at why you might choose Disjoint Set Union (Union-Find) instead of traversal when edges arrive as a dynamic stream.

Do you default to DFS or BFS for component counting in interviews?

#LearningInPublic #SoftwareEngineering #Python #Algorithms #DataStructures #Graphs #DFS #BFS #LeetCode #CleanCode #ComputerScience
