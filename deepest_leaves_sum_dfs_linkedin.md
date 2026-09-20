# Mastering Binary Trees: Depth-First Summing of Deepest Leaves, Recursive v. Iterative (Part 2) 🌲🔄

### The Problem:
Given the root of a binary tree, return the sum of values of its deepest leaves.

In **Part 1**, we saw how Breadth-First Search (BFS) provides a natural level-by-level solution for summing the deepest leaves of a binary tree.

However, on wide, balanced binary trees, BFS queues can balloon to hold up to $50\%$ of all tree nodes ($\approx N/2$) simultaneously. 

Can we achieve $\mathcal{O}(\log N)$ auxiliary space using **Depth-First Search (DFS)**? Indeed we can. Let's see how!

---

### 💡 The DFS Insight: Dynamic Depth Tracking

Unlike BFS, DFS traverses branches vertically. To find the sum of only the *deepest* leaves in a single pass, we maintain two dynamic state variables: `max_depth` and `total`.

When visiting any node at `depth` we face three possibilities:
1. **New Deepest Level Found (`depth > max_depth`)**: We've reached a deeper layer than anything seen before! Reset  `max_depth = depth` and reset `total = node.val`.
2. **Same Deepest Level (`depth == max_depth`)**: Another leaf at our current record depth $\to$ accumulate `total += node.val`.
3. **Shallower Level (`depth < max_depth`)**: Ignore since this cannot contribute to the max-depth sum we're after.

---

### 🛡️ Recursive DFS vs. Iterative Stack DFS

- **Recursive DFS**: Clean and declarative. It traverses left and right subtrees while passing `depth + 1`, utilizing $\mathcal{O}(H)$ call stack space ($\mathcal{O}(\log N)$ on balanced trees).
- **Iterative DFS**: For deep or skewed trees ($H > 1,000$), recursion risks hitting Python's recursion limit. By managing an explicit stack of `(node, depth)` tuples on the heap, we guarantee $100\%$ stack-overflow safety.

---

### ⚖️ BFS vs. DFS Architectural Comparison

| Metric | Level-Order BFS | Recursive DFS | Iterative DFS (Stack) |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| **Auxiliary Space (Balanced Tree)** | $\mathcal{O}(N)$ queue ($\approx N/2$ nodes) | $\mathcal{O}(\log N)$ call stack | $\mathcal{O}(\log N)$ heap stack |
| **Auxiliary Space (Skewed Tree)** | $\mathcal{O}(1)$ queue | $\mathcal{O}(N)$ call stack | $\mathcal{O}(N)$ heap stack |
| **State Management** | Level-scoped reset | Dynamic `(max_depth, total)` | Dynamic `(max_depth, total)` |
| **Stack Overflow Risk** | None | Possible on deep trees ($H > 1,000$) | **None** |

---

When designing tree algorithms in production, do you favor the intuitive level scoping of BFS or the $\mathcal{O}(\log N)$ memory footprint of DFS?

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #DFS #TreeTraversal #Recursion
