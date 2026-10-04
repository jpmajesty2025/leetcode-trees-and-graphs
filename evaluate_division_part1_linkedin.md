# Evaluate Division: Algebraic Equations as Directed Multiplicative Graphs ➗🌲

Given a system of fraction equations such as:
A / B = 2.0,  B / C = 3.0

We need to answer queries like A / C = ? or x / y = ?.

How do you translate abstract algebraic fractions into concrete graph data structures?

---

### 💡 The Multiplicative Directed Graph Abstraction

Every variable is a **graph vertex**, and every ratio is a **weighted directed edge**:
• Equation A / B = v creates two directed edges:
  1. Forward edge: A -> B with weight v (A = B * v)
  2. Reciprocal edge: B -> A with weight 1/v (B = A * 1/v)

Evaluating any query C / D:
• Is equivalent to finding a path from C to D and **multiplying all edge weights along the path**!
A -> B (2.0) -> C (3.0)  =>  A / C = 2.0 * 3.0 = 6.0

---

### ⚡ Query Traversal via DFS / BFS

1️⃣ **Component Verification**:
• If either C or D is missing from the graph => return -1.0.
• If C == D and present in graph => return 1.0.

2️⃣ **Path Multiplication**:
• Run DFS/BFS from C looking for D.
• Track `visited: set()` to prevent infinite cycles.
• Multiply edge weights along the active branch.

---

### 🚨 The Scale Bottleneck of Graph Traversals

While intuitive, running DFS/BFS for each query yields:
O(N + Q * N) Total Time (where N = equations, Q = queries).

When Q climbs to 100,000 queries on a system of 1,000 equations, executing 100,000 graph traversals creates a severe bottleneck!

---

### ⚖️ Graph Traversal Breakdown

| Metric | Graph DFS / BFS Traversal |
| :--- | :--- |
| **Graph Construction** | O(N) adjacency map |
| **Per-Query Runtime** | O(V + E) = O(N) per query |
| **Total Query Workload** | O(Q * N) (Expensive at high Q) |
| **Cycle Handling** | Requires per-query visited set |

---

In Part 2 tomorrow, we’ll explore how **Weighted Union-Find slashes query time from O(N) down to instant O(1) amortized response!**

How do you model variable dependencies and constraint systems in your services? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #SystemDesign #ComputerScience
