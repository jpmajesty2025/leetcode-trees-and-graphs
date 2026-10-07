# Graph Infrastructure & Pairwise Deduplication: Maximal Network Rank (Part 1 of 2) 🏙️🌉

When evaluating infrastructure capacity — whether for road networks, fiber backbones, or airline routes — a fundamental metric is combined connectivity. 

In "Maximal Network Rank" (LeetCode 1615), we determine the maximum joint reach of any two cities. Let's explore graph modeling and memory optimization!

---

### 💡 The Problem & Core Invariant

Given `n` cities and a list of bidirectional roads:
- The **network rank** of two cities `u` and `v` is the total number of directly connected roads to either city.
- If a road directly connects `u` and `v`, it serves both and must be counted **only once**.

Formula:
`NetworkRank(u, v) = Degree(u) + Degree(v) - (1 if Connected(u, v) else 0)`

We want to find the maximum rank across all distinct pairs `(u, v)` where `u != v`.

---

### ⚙️ Memory Optimization: Matrix vs. Edge Set

The standard approach checks all O(V²) pairs:

1. **Adjacency Matrix Approach**:
   - Maintains an `n × n` boolean table `connected[u][v]` plus a `degree` array.
   - Takes **O(V²) space**. Fine for small `n`, but wasteful on large sparse graphs.
2. **Edge Set Approach**:
   - Stores normalized pairs `(min(u, v), max(u, v))` in a hash set.
   - Reduces space to strictly **O(E)** memory with O(1) edge lookups.

---

### 📊 Complexity Profile

- **Time Complexity: O(V² + E)** — Ingesting `E` roads takes O(E) time; scanning all pairs takes O(V²) time.
- **Auxiliary Space: O(E)** — Active edges in a hash set and degrees in an array of size V.

---

### 🧠 Engineering Takeaway

Deduplication at the boundary of two entities (`Degree(u) + Degree(v) - 1`) is common in graph analytics and relational joins. Using an edge set over a full matrix preserves cache locality and minimizes footprint on sparse networks.

👉 **In Part 2**, we will break the **O(V²)** barrier down to **O(V + E)** using **Degree Clustering and the Pigeonhole Principle**!

How do you handle overlap deduplication in your distributed graph pipelines?

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #GraphTheory #NetworkAnalysis #PerformanceOptimization
