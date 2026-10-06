# Maximum Level Sum: DFS Accumulation vs. Queue Memory (Part 2 of 2) 🌲🧠

In Part 1, we explored finding the level with the maximum sum using BFS (LeetCode 1161). While BFS is intuitive for horizontal layers, Depth-First Search (DFS) provides a powerful alternative that drastically reduces memory consumption on balanced trees.

Here is how depth-indexed DFS works and how its memory footprint compares to BFS.

---

### 💡 The DFS Mental Model: Depth Accumulation

Instead of sweeping horizontally level by level, DFS traverses vertically and accumulates sums into a dynamic array:

1. **State Tracking**: Maintain a `level_sums` list where index `i` stores the sum of nodes at depth `i`.
2. **Dynamic Allocation**: When visiting a node at `depth`, if `depth == len(level_sums)`, append `0` to allocate a new level sum.
3. **In-Place Summation**: Add `node.val` to `level_sums[depth]`.
4. **Recursive Step**: Traverse `node.left` and `node.right` with `depth + 1`.

---

### 🎯 Built-In Tie-Breaking Elegance

How do we extract the smallest 1-based level that produced the maximal sum?

In Python: `level_sums.index(max(level_sums)) + 1` handles this automatically:
- `max(level_sums)` finds the peak sum.
- `list.index()` returns the **first occurrence** of that maximum value.
- Adding `1` converts the 0-based index to the required 1-based level, resolving ties without manual conditional logic.

---

### ⚖️ Memory Profile: Queue Width vs. Stack Height

Both approaches run in linear O(N) time, but their spatial behavior differs significantly:

1. **Balanced Trees (Width vs. Height)**:
   - **BFS Queue**: Must hold the widest level in memory. For a balanced tree with 1,000,000 nodes, the queue holds ~500,000 nodes at the bottom level.
   - **DFS Recursion**: Holds at most the height of the tree (log₂ N ≈ 20 frames) plus a 20-element `level_sums` list. Working memory drops by orders of magnitude!

2. **Skewed Trees**:
   - In degenerate single-branch trees, BFS uses O(1) queue space.
   - Recursive DFS uses O(N) call-stack frames. Using an **Iterative DFS** with an explicit heap stack preserves O(H) space while eliminating recursion limit concerns.

---

### 📊 Complexity Summary

- **Time Complexity: O(N)** for both approaches.
- **Space Complexity**:
  - **BFS**: O(W) queue space (up to N/2 for balanced trees).
  - **DFS**: O(H) auxiliary space (O(log N) for balanced trees, O(N) for skewed chains).

---

### 🚀 Engineering Takeaway

On wide, balanced trees, vertical depth accumulation can slash memory consumption from hundreds of thousands of heap objects down to a few dozen stack frames.

Do you prioritize streaming queue processing or recursion memory efficiency in tree traversals?

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #TreeTraversal #DFS #BFS #Recursion #PerformanceOptimization #SystemDesign
