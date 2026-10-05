# Symmetric Tree Traversal: Reversing Odd Levels with Dual-Pointer DFS 🌲🔀

For a change of pace, we are given a **perfect binary tree**.

Our goal is to reverse the node values at every **odd level** (0-indexed root is level 0, children are level 1, grandchildren level 2, etc.):

```
        2 (L0)                      2 (L0)
      /   \                       /   \
     3     5 (L1)       ==>      5     3 (L1)
    / \   / \                   / \   / \
   8  13 21 34 (L2)            8  13 21 34 (L2)
```

How do we swap values between nodes that live in completely separate subtrees?

---

### 🚨 The Single-Pointer DFS Bottleneck

Standard DFS visits one node at a time. But reversing a level requires swapping symmetric pairs across the entire breadth of the tree (e.g., pairing the leftmost node with the rightmost node).

Passing a single pointer cannot easily coordinate cross-subtree swaps.

---

### 💡 Dual-Pointer Symmetric DFS

Because the tree is a **perfect binary tree**, every level is completely filled and symmetric!

We can traverse two mirror nodes simultaneously: `dfs(node_left, node_right, is_odd)`.

1. If `is_odd` is True, swap their values:
   ```python
   node_left.val, node_right.val = node_right.val, node_left.val
   ```

2. Recurse down symmetrically:
   • **Outer Pair**: `dfs(node_left.left, node_right.right, not is_odd)`
   • **Inner Pair**: `dfs(node_left.right, node_right.left, not is_odd)`

---

### ⚡ Clean Implementation

```python
def reverse_odd_levels(root: TreeNode | None) -> TreeNode | None:
    if not root or not root.left:
        return root

    def dfs(node_left: TreeNode | None, node_right: TreeNode | None, is_odd: bool) -> None:
        if not node_left or not node_right:
            return

        if is_odd:
            node_left.val, node_right.val = node_right.val, node_left.val

        dfs(node_left.left, node_right.right, not is_odd)
        dfs(node_left.right, node_right.left, not is_odd)

    dfs(root.left, root.right, True)
    return root
```

---

### ⚖️ Algorithm Complexity

| Metric | Dual-Pointer Symmetric DFS |
| :--- | :--- |
| **Time Complexity** | **O(N)** (Each node visited once) |
| **Call Stack Memory** | **O(log N)** (Perfect tree depth is exactly log2(N + 1)) |
| **Auxiliary Heap Space** | **O(1)** (In-place integer value swaps) |

---

In Part 2 tomorrow, we’ll contrast **Level-Order BFS Two-Pointer Swapping vs Symmetric DFS!**

How do you handle multi-pointer traversals across symmetric tree structures? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #TreeTraversals #CleanCode #Recursion
