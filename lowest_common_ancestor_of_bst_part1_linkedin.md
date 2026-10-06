# Lowest Common Ancestor in a BST: The Split Point Strategy (Part 1 of 2) 🌲⚡

Finding the Lowest Common Ancestor (LCA) of two nodes is a classic tree problem. While general binary trees require full tree exploration, the Binary Search Tree (BST) invariant unlocks an optimal single-path search.

Let's break down the split point mental model and how to implement it in O(1) space!

---

### 💡 The Problem & The "Split Point" Intuition

Given a BST and two nodes `p` and `q`, find the lowest node that has both `p` and `q` as descendants (where a node can be a descendant of itself).

In a BST, all values to the left are smaller and all values to the right are larger. This gives us three mutually exclusive scenarios at any node `curr`:

1. **Both Nodes in Left Subtree**: If `p.val < curr.val` and `q.val < curr.val`, both targets reside in the left subtree. Advance `curr = curr.left`.
2. **Both Nodes in Right Subtree**: If `p.val > curr.val` and `q.val > curr.val`, both targets reside in the right subtree. Advance `curr = curr.right`.
3. **The Split Point (LCA Found)**:
   - One node is in the left subtree and the other is in the right subtree (`p.val < curr.val < q.val`).
   - OR `curr` matches `p` or `q` directly.

The moment `p` and `q` diverge to opposite sides of `curr`, `curr` is guaranteed to be their Lowest Common Ancestor!

---

### ⚙️ Why Iterative Pointer Traversal Wins

Because we only ever follow a single branch down the tree toward the split point, we never need to backtrack:
- Start with a pointer `curr = root`.
- Walk left or right based on the comparisons.
- As soon as the branch splits, return `curr`.

Zero stack frames allocated, zero recursion overhead.

---

### 📊 Complexity Profile

- **Time Complexity: O(H)** — Where H is tree height (O(log N) for balanced BSTs, O(N) for degenerate chains). We inspect at most one node per level.
- **Auxiliary Space: O(1)** — A single pointer walk with constant memory.

---

### 🧠 Key Engineering Takeaways

1. **Single-Path Directness**: Unlike general binary trees that require searching both subtrees, the BST invariant eliminates 50% of remaining candidates at every step.
2. **Deterministic Divergence**: The first node where paths to `p` and `q` separate is mathematically proven to be the LCA.

👉 **In Part 2**, we'll compare **LCA in a BST vs. LCA in a General Binary Tree** and examine why structural invariants revolutionize algorithmic complexity!

How often do you leverage BST ordering to prune search spaces?

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #BinarySearchTree #BST #LCA #PerformanceOptimization
