# All Nodes Distance K: Escaping One-Way Trees with Parent-Pointer Wavefront BFS 🌲⚡

In this binary tree problem, we are given a `target` node and must find all nodes exactly distance $k$ away.

The fundamental challenge:
• Binary tree pointers are strictly **unidirectional** (`node.left`, `node.right`).
• But nodes at distance $k$ can live **above** the target, in sibling subtrees, or down below!

How do you traverse "upward" without over-engineering an entire graph?

---

### 🚨 The Overhead of Full Graph Conversion

Many developers convert the entire tree into an undirected adjacency list graph:
`graph[u.val] = [parent.val, left.val, right.val]`

While correct, this approach allocates:
1. Extra dictionaries and lists for every node.
2. Adjacency lists storing redundant edge relationships that the tree pointers already represent!

---

### 💡 The Clean Optimization: Parent Pointer Map + Wavefront BFS

Instead of rebuilding a full graph from scratch, we only need to supply the missing link: **the parent pointer**!

1️⃣ **Step 1: Map Parents ($\mathcal{O}(N)$)**:
• Run a single tree traversal to record `parents[child] = parent`.

2️⃣ **Step 2: Level-Order Wavefront BFS**:
• Start a BFS queue at `[target]` with a `visited = {target}` set.
• At each step, expand outward in **3 directions**: `node.left`, `node.right`, and `parents.get(node)`.
• Increment distance layer by layer.

3️⃣ **Step 3: Instant Level Extraction**:
• The instant `curr_distance == k`, stop the loop!
• The nodes sitting in the queue are **the exact answer** — no filtering required!

---

### ⚖️ Performance Comparison

| Metric | Adjacency List Graph | Parent Map + Wavefront BFS |
| :--- | :--- | :--- |
| **Time Complexity** | $\mathcal{O}(N)$ | $\mathbf{O(N)}$ |
| **Graph Construction** | Full Adjacency List Allocation | **Lightweight `parents` Dict** |
| **Traversal Style** | Graph BFS with Distance Tuples | **Clean Layer-by-Layer Wavefront** |
| **Result Extraction** | Loop & filter on distance | **Instant snapshot of queue at level $k$** |

---

Check out the clean Parent-Pointer BFS implementation in the attached snippet! 📸

In Part 2 tomorrow, we’ll explore how to solve this in **pure $\mathcal{O}(H)$ call stack space without ANY graph or queue allocations!**

How do you handle upward traversals in tree structures? Let's discuss below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #SystemDesign #ComputerScience
