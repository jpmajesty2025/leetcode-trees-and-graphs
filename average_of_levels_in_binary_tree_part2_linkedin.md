# Average of Levels: Parallel DFS Accumulators vs. Queue Memory (Part 2 of 2) 🌲🧠

In Part 1, we examined how BFS computes level averages on the fly (LeetCode 637). While BFS provides a clean horizontal sweep, Depth-First Search (DFS) offers an elegant alternative using parallel accumulator arrays—delivering massive memory savings on balanced trees.

Here is how depth-indexed DFS calculates level averages!

---

### 💡 The DFS Mental Model: Dual Accumulator Lists

Instead of visiting nodes tier by tier, DFS dives deep along branches. To compute level averages without a queue, we track two parallel lists:
1. `sums`: stores the running sum of all node values visited at depth `i`.
2. `counts`: stores the total number of nodes visited at depth `i`.

---

### ⚙️ How DFS Accumulation Works

1. **Dynamic Allocation**: When visiting a node at `depth`, check if `depth == len(sums)`. If true, allocate new entries by appending `0.0` to `sums` and `0` to `counts`.
2. **In-Place Updates**: Add `node.val` to `sums[depth]` and increment `counts[depth]` by 1.
3. **Branch Traversal**: Recurse down `node.left` and `node.right` with `depth + 1`.
4. **Vectorized Average**: After traversal finishes, compute the final averages in a single list comprehension: `[s / c for s, c in zip(sums, counts)]`.

---

### ⚖️ Memory Profile: Queue Width vs. Stack Height

Both BFS and DFS achieve linear O(N) time complexity, but their memory footprints differ significantly:

1. **Balanced Trees**:
   - **BFS Queue**: Must hold the widest tier simultaneously in memory. For a balanced tree with 1,000,000 nodes, the queue holds ~500,000 nodes at the bottom level.
   - **DFS Stack**: Auxiliary memory scales with tree height (log₂ N ≈ 20 frames) plus two 20-element arrays for `sums` and `counts`. Working memory drops by orders of magnitude.

2. **Skewed Trees & Stack Safety**:
   - In single-line linked list trees, BFS uses O(1) queue space.
   - Recursive DFS uses O(N) stack frames. Using an **Iterative DFS** with an explicit stack `[(node, depth)]` retains O(H) space while eliminating recursion depth limits.

---

### 📊 Complexity Summary

- **Time: O(N)** — Every node is visited once across both algorithms.
- **Space**:
  - **BFS**: O(W) queue space (up to N/2 on balanced trees).
  - **DFS**: O(H) auxiliary space (O(log N) for balanced trees, O(N) for skewed chains).

---

Do you prefer streaming BFS or depth-indexed DFS for tree reductions?

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #TreeTraversal #DFS #BFS #Recursion #PerformanceOptimization
