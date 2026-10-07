# Inverse Boundary Flood Fill: Number of Enclaves (Part 1 of 2) 🏝️🌊

Inverting your perspective on grid reachability can turn an expensive search into a single linear pass.

In "Number of Enclaves", we are given a binary matrix where `1` represents land and `0` represents water. A move consists of walking 4-directionally from cell to cell, or off the grid edge. We need to count all land cells that **cannot** reach the boundary.

Let's break down the inverse boundary traversal strategy!

---

### 💡 The Mindset Shift: Search Inward, Not Outward

A naive approach checks every interior land cell to see if any path reaches the border, causing redundant traversals.

**The Inversion Trick**:
Instead of asking *"Can this interior land reach the boundary?"*, ask:
👉 *"Which land cells are reachable FROM the boundary?"*

Any land connected to the boundary is "flooded" (eliminated). Whatever land survives this flood is an isolated enclave!

---

### ⚙️ The 2-Phase Algorithm

1. **Phase 1: Boundary Flood Fill**
   - Iterate along all 4 grid perimeters (top, bottom, left, right).
   - When a boundary cell is land (`1`), trigger DFS/BFS to traverse its connected component and sink it (mark as `0` or visited).

2. **Phase 2: Interior Accounting**
   - Scan the grid.
   - Count all remaining `1`s. Since boundary-connected land was removed, every surviving `1` is a guaranteed enclave cell.

---

### 📊 Complexity Profile

- **Time: O(M * N)** — Every cell is visited at most a constant number of times.
- **Space: O(M * N)** — For the traversal stack/queue (or O(1) auxiliary space with in-place mutation).

---

### 🧠 Key Engineering Takeaway

When solving reachability toward a shared perimeter, starting traversal from the boundary reduces the problem to a single bounded flood fill.

👉 **In Part 2**, we will explore **Multi-Source BFS, Virtual-Node Union-Find, and Coastal Flood Inundation Modeling**!

How do you handle inverse boundary traversals in your graph pipelines?

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #GraphTheory #CleanCode #PerformanceOptimization
