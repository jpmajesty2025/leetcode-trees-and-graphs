# Even-Odd Trees: Level Invariants & Early-Exit BFS (Part 1 of 2) 🌲⚖️

When validating structural invariants across trees—such as alternating parity and strict monotonicity per horizontal tier (LeetCode 1609)—Breadth-First Search (BFS) offers a natural mental model.

Let's break down the rules and how to implement an optimal, early-exiting queue architecture!

---

### 💡 The Problem & Invariant Rules

A binary tree is classified as **Even-Odd** if it satisfies two conditions across all depths (with the root at level 0):

1. **Even-Indexed Levels (0, 2, 4...)**:
   - Every node must have an **odd integer value**.
   - Values must be in **strictly increasing** order from left to right.

2. **Odd-Indexed Levels (1, 3, 5...)**:
   - Every node must have an **even integer value**.
   - Values must be in **strictly decreasing** order from left to right.

If any node violates its level's parity or monotonicity constraint, the entire tree is invalid.

---

### ⚙️ How Early-Exit BFS Works

1. **Double-Ended Queue**: Initialize a `collections.deque` with the root node and set `level = 0`.
2. **Tier Isolation**: Capture `level_size = len(queue)` at the start of each iteration.
3. **Previous Value State**: Reset `prev_value = None` at the start of each level to track monotonicity across adjacent siblings.
4. **Validation Checks**:
   - For even levels: Fail immediately if `node.val` is even, or if `prev_value is not None` and `node.val <= prev_value`.
   - For odd levels: Fail immediately if `node.val` is odd, or if `prev_value is not None` and `node.val >= prev_value`.
5. **Enqueue Children**: Append non-null left and right children to build the next tier.

---

### ⚠️ Optimization Note: Avoid List Queue Overhead

Always use `collections.deque` rather than a standard Python list. Calling `pop(0)` shifts all remaining pointers in memory (O(K) time per pop). In wide trees, this turns an O(N) linear sweep into an O(N²) quadratic crawl. `deque.popleft()` provides guaranteed O(1) removals.

---

### 📊 Complexity Profile

- **Time: O(N)** — Every node is checked at most once, with early termination on the first violation.
- **Space: O(W)** — Queue memory is proportional to maximum tree width (up to N/2).

---

👉 **In Part 2**, we'll explore **DFS validation with depth-indexed last-seen tracking**—and see how DFS cuts working memory on wide trees!

How do you organize multi-condition tree validations?

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #TreeTraversal #BFS #PerformanceOptimization
