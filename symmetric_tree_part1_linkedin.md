# Mirror Symmetry in Binary Trees: The Dual-Tree Recursive Paradigm 🌲🪞

We are given the root of a binary tree and asked:
*Is this tree a mirror reflection of itself around its vertical center axis?*

```
        1                     1
      /   \                 /   \
     2     2      vs       2     2
    / \   / \               \     \
   3   4 4   3               3     3
   [Symmetric ✅]        [Asymmetric ❌]
```

How do we formulate a clean mathematical invariant to verify mirror symmetry?

---

### 💡 The Dual-Tree Paradigm Shift

Attempting to reason about self-symmetry using a single tree pointer is cumbersome.

The key insight is transforming the problem into a **two-tree mirror comparison**:
• A tree is symmetric if and only if its left subtree and right subtree are **mirror images of each other**:
  `is_symmetric(root) = is_mirror(root.left, root.right)`

---

### ⚡ The 3 Mirror Invariants

Consider the possibilities for two trees `t1` and `t2`:

1. **Both are Empty**: `not t1 and not t2` ➡️ `True`
2. **One is Empty (Structural Asymmetry)**: `not t1 or not t2` ➡️ `False`
3. **Values Match & Subtrees Mirror**:
   • `t1.val == t2.val`
   • **Outer Subtrees Mirror**: `is_mirror(t1.left, t2.right)`
   • **Inner Subtrees Mirror**: `is_mirror(t1.right, t2.left)`

---

### 💻 Clean Pythonic Implementation

```python
def is_symmetric(root: TreeNode | None) -> bool:
    if not root:
        return True

    def is_mirror(t1: TreeNode | None, t2: TreeNode | None) -> bool:
        if not t1 and not t2:
            return True
        if not t1 or not t2:
            return False

        return (
            t1.val == t2.val
            and is_mirror(t1.left, t2.right)
            and is_mirror(t1.right, t2.left)
        )

    return is_mirror(root.left, root.right)
```

---

### ⚖️ Algorithm Complexity

| Metric | Recursive Mirror DFS |
| :--- | :--- |
| **Time Complexity** | **O(N)** (Each node visited at most once) |
| **Call Stack Memory** | **O(H)** (O(log N) balanced, O(N) skewed) |
| **Short-Circuiting** | **Instant failure** on first mismatch |

---

In Part 2 tomorrow, we’ll explore **Iterative Queue BFS Pair Verification for Call-Stack Safety!**

How do you decompose self-referential tree problems into multi-tree invariants? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #TreeTraversals #CleanCode #Recursion
