# Even-Odd Trees: Depth-Indexed DFS & Stack-Safe Traversal (Part 2 of 2) 🌲🧠

In Part 1, we explored validating Even-Odd trees using Breadth-First Search (BFS). While BFS follows the horizontal rows naturally, Depth-First Search (DFS) provides an alternative that substantially reduces memory footprint on wide trees.

How can a vertical DFS validate horizontal left-to-right rules? Let's dive in!

---

### 💡 The DFS Mental Model: Preorder Guarantees

How can DFS check horizontal left-to-right monotonicity when it traverses vertically down branches?

The key insight is in **Preorder Traversal (Root $\to$ Left $\to$ Right)**:
- At any given depth `d`, all nodes in the left subtree are visited **before** any nodes in the right subtree.
- Therefore, as DFS visits nodes at depth `d`, they arrive in **exact left-to-right order**!

By maintaining a single list `prev_values` where `prev_values[d]` stores the value of the most recently visited node at depth `d`, we can validate monotonicity without needing a level queue.

---

### ⚙️ How Depth-Indexed DFS Works

1. **Parity Guard**:
   - Depth is even: `node.val` must be odd.
   - Depth is odd: `node.val` must be even.
2. **Monotonicity Guard**:
   - If `depth == len(prev_values)`: This is the very first node at this depth, so append `node.val`.
   - Otherwise, compare `node.val` against `prev_values[depth]`:
     - Even depth: fail if `node.val <= prev_values[depth]` (must be strictly increasing).
     - Odd depth: fail if `node.val >= prev_values[depth]` (must be strictly decreasing).
     - Update `prev_values[depth] = node.val`.
3. **Short-Circuit Recursion**: Recurse down `node.left` and `node.right`.

---

### ⚖️ Memory Profile & Iterative Safety

- **Balanced Trees**:
  - **BFS Queue**: Must store the entire widest level in heap memory (up to N/2 nodes).
  - **DFS Call Stack**: Stores only the height of the tree (log₂ N ≈ 20 frames for 1M nodes) plus a 20-element `prev_values` list. Memory usage drops significantly!

- **Iterative DFS Safety**:
  - To prevent call-stack overflow on deep, skewed trees, use an explicit heap stack of `(node, depth)` tuples.
  - Push `node.right` before `node.left` so that the left child is popped and processed first, preserving strict left-to-right visitation.

---

### 📊 Complexity Summary

- **Time: O(N)** — Fast early termination on any rule violation.
- **Space**:
  - **BFS**: O(W) queue space (up to N/2).
  - **DFS**: O(H) stack space (O(log N) for balanced trees, O(N) for skewed chains).

---

Do you prefer validating tier constraints horizontally via BFS or vertically via preorder DFS?

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #TreeTraversal #DFS #BFS #Recursion #PerformanceOptimization
