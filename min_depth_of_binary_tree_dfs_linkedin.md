# Mastering Binary Trees (Part 1): The Single-Child Trap & DFS (Recursive vs. Iterative) 🌲

Finding the *maximum* depth of a binary tree is straightforward: explore all paths and take the maximum. 

Finding the **minimum depth**, however, introduces a common pitfalls in technical interviews: **a leaf node must have NO children**.

---

### ⚠️ The "Hidden" Single-Child Trap
If a node only has one child (e.g., a left child but no right child), blindly taking `min(left_depth, right_depth) + 1` fails. Why? Because the empty right child returns `0`, which would falsely declare the current parent node a leaf with depth 1!

To solve this properly with **Depth-First Search (DFS)**, we have two distinct approaches (as is always the case with DFS!):

---

### 1. The Recursive DFS Approach

Recursive DFS mirrors post-order traversal with explicit child checks:
- **Base Case:** Empty root $\to$ return `0`.
- **Single Child:** If one side is empty, we *must* explore the non-empty subtree.
- **Two Children:** Only when both exist do we take `min(left, right) + 1`.

```python
from typing import Optional
from tree_node import TreeNode


def min_depth(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    if not root.left and not root.right:
        return 1
    if not root.left:
        return min_depth(root.right) + 1
    if not root.right:
        return min_depth(root.left) + 1

    return min(min_depth(root.left), min_depth(root.right)) + 1
```

---

### 2. The Iterative Stack Approach (DFS with Pruning) 🛡️

To avoid Python's call-stack limits on deep trees, we simulate DFS using an explicit heap stack `(node, depth)` and apply **branch-and-bound pruning**:

```python
from typing import Optional, List, Tuple
from tree_node import TreeNode


def min_depth_iterative(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    stack: List[Tuple[TreeNode, int]] = [(root, 1)]
    min_d = float('inf')

    while stack:
        node, depth = stack.pop()

        if not node.left and not node.right:
            min_d = min(min_d, depth)
            continue

        # Prune branches already deeper than the minimum found so far
        if depth >= min_d:
            continue

        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))

    return int(min_d)
```

---

### ⏱️ The Fundamental Limitation of DFS
Both DFS approaches have an inherent weakness: **DFS must dive deep first**. 

If a shallow leaf sits at depth 2 on the right, but DFS dives down a 10,000-node branch on the left, it still visits all 10,000 nodes before discovering the shallow answer!

👉 **In Part 2**, we'll explore why **Breadth-First Search (BFS)** is the architectural winner for shortest-path tree problems, terminating in $\mathcal{O}(1)$ best-case time. Stay tuned!

#LearningInPublic #Python #DataStructures #Algorithms #LeetCode #SoftwareEngineering #CleanCode #Recursion
