# Mastering Binary Trees (Part 1): The Elegant 10-Line Recursive Lowest Common Ancestor (LCA) 🌲

Finding the **Lowest Common Ancestor (LCA)** of two nodes in a binary tree is a classic interview questions—and a masterclass in post-order tree recursion.

---

### 💡 The Problem
Given a binary tree and two nodes `p` and `q`, find the lowest node that has both `p` and `q` as descendants (a node can be a descendant of itself).

---

### 🧠 The Recursive Intuition (Bottom-Up DFS)

Instead of searching from the top down and re-scanning subtrees, we let our recursive calls report findings from the bottom up:

1. **Base Case:** If the current node is `None`, `p`, or `q`, return it immediately.
2. **Divide:** Recurse on `node.left` and `node.right`.
3. **Combine:**
   - **Both subtrees return a node?** $p$ and $q$ sit in separate branches of the current node $\to$ **current node is the LCA!**
   - **Only one subtree returns a node?** Pass that node up.
   - **Neither returns a node?** Return `None`.

```python
from typing import Optional
from tree_node import TreeNode


def lowest_common_ancestor(root: Optional[TreeNode], p: Optional[TreeNode], q: Optional[TreeNode]) -> Optional[TreeNode]:
    """Find LCA using bottom-up post-order recursion."""
    if not root or root is p or root is q:
        return root

    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    if left and right:
        return root

    return left if left else right
```

### ⏱️ Complexity
- **Time:** $\mathcal{O}(N)$ — visits each node at most once.
- **Space:** $\mathcal{O}(H)$ call stack frames ($H = \log N$ balanced, $H = N$ skewed).

---

### 🤔 The Catch...
What happens if your tree is skewed with a depth of 10,000+ nodes, blowing past Python's default call stack limit with a `RecursionError`?

👉 **In Part 2**, we'll eliminate the call stack entirely - something we've done before with other tree traversal algorithms - using instead an **iterative parent-pointer traversal with early stopping**. Stay tuned!

#LearningInPublic #Python #DataStructures #Algorithms #LeetCode #SoftwareEngineering #CleanCode #Recursion
