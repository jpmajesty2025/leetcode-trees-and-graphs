# Longest Weighted Path on Trees: Informing All Employees (Part 1 of 2) 🌳⏱️

How long does it take for broadcast news to reach every leaf in an organization?

In "Time Needed to Inform All Employees", we are given `n` employees, a root `headID`, a `manager` array, and an `informTime` array representing the delay required for each manager to notify direct reports.

Let's explore tree modeling and stack-safe broadcast traversal!

---

### 💡 The Problem & Graph Invariant

Subordination relationships form a **directed rooted tree**:
- Root: `headID` (`manager[headID] = -1`).
- Edges: Directed edges from manager to subordinates.
- Edge Weights: `informTime[manager]`.

**The Critical Invariant**:
Because managers notify subordinates in parallel, child branches propagate concurrently. Total time required is the **maximum weighted path from root to any leaf** (the makespan).

---

### ⚙️ Top-Down Iterative Traversal (Stack-Safe)

With some languages, recursive DFS can hit call stack limits on deep hierarchies.

Instead, an **iterative BFS queue** ensures stability:
1. Build an adjacency list `adj[manager] = [subordinates]`.
2. Push `(headID, 0)` into a queue tracking `(employee_id, accumulated_time)`.
3. For each subordinate, enqueue `(sub, accumulated_time + informTime[employee_id])`.
4. Maintain a running maximum of `accumulated_time`.

---

### 📊 Complexity Profile

- **Time: O(N)** — Every employee and subordinate edge is processed once.
- **Space: O(N)** — Adjacency list and BFS queue.

---

### 🧠 Engineering Takeaway

In broadcast trees with parallel fanout, total delay equals the longest path, not the sum of edges. Iterative queue traversals ensure memory stability across deep trees.

👉 **In Part 2**, we will explore **Zero-Adjacency Bottom-Up Memoization and P2P Gossip Broadcast Networks**!

How do you model message propagation delays in your distributed services?

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #TreeAlgorithms #CleanCode #PerformanceOptimization
