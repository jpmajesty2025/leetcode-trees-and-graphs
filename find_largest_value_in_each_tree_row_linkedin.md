# BFS vs. DFS: Finding Row-Level Extremes in Binary Trees 🌲📊

When tasked with aggregating statistics level by level in a binary tree (such as finding the maximum value in each row), which algorithm should you reach for first: **Level-Order BFS** or **Depth-Indexed DFS**?

Let's examine **LeetCode 515: Find Largest Value in Each Tree Row** and break down the space, time, and architectural trade-offs.

---

### 💡 The Problem
Given the root of a binary tree, return an array containing the maximum value found in each horizontal row (0-indexed, from top to bottom).

---

### 1️⃣ Approach 1: Iterative BFS (The Natural Fit)

Because the problem explicitly asks for row-by-row metrics, Breadth-First Search offers the cleanest mental model:
1. Traverse level by level using a `deque`.
2. Compute the maximum of the current level directly.
3. Append the finalized maximum to `result`.

```python
from collections import deque
from typing import Optional, List
from tree_node import TreeNode


def largest_values(root: Optional[TreeNode]) -> List[int]:
    """Iterative BFS level-order traversal."""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        max_val = float('-inf')

        for _ in range(level_size):
            node = queue.popleft()
            max_val = max(max_val, node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(max_val)

    return result
```

**Key Advantage:** Early level finalization and $\mathcal{O}(1)$ space on skewed/tall trees.

---

### 2️⃣ Approach 2: Depth-Indexed DFS (Memory-Efficient for Balanced Trees)

Can we solve row aggregation depth-first? Absolutely! By passing the current `depth`:
- If `depth == len(result)`, this is the first node visited at this depth $\to$ `result.append(node.val)`.
- Otherwise, update `result[depth] = max(result[depth], node.val)`.

```python
from typing import Optional, List
from tree_node import TreeNode


def largest_values_dfs(root: Optional[TreeNode]) -> List[int]:
    """Recursive DFS tracking row maxima by depth index."""
    result: List[int] = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if not node:
            return

        if depth == len(result):
            result.append(node.val)
        else:
            result[depth] = max(result[depth], node.val)

        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return result
```

**Key Advantage:** Requires only $\mathcal{O}(\log N)$ call stack space on balanced trees (versus $\mathcal{O}(N)$ queue memory for BFS).

---

### ⚖️ Architectural Trade-off Summary

| Metric | Iterative BFS | Recursive DFS | Iterative DFS (Stack) |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| **Space (Balanced Tree)** | $\mathcal{O}(N)$ queue ($\approx N/2$ nodes) | $\mathcal{O}(\log N)$ call stack | $\mathcal{O}(\log N)$ heap stack |
| **Space (Skewed Tree)** | $\mathcal{O}(1)$ queue | $\mathcal{O}(N)$ call stack | $\mathcal{O}(N)$ heap stack |
| **State Finalization** | Streamed per level | Finalized at end of traversal | Finalized at end of traversal |
| **Stack Overflow Risk** | None | Possible if depth > 1000 | None |

---

### 🧪 Property-Based Verification
Using **Hypothesis**, all three solutions were validated against an independent oracle across random trees with negative values, extreme bounds, and varying topologies with 100% agreement.

---

When designing tree aggregations in production, do you favor BFS for streaming row completion or DFS for minimal memory footprint? Share your perspective below! 👇

#Python #DataStructures #Algorithms #LeetCode #SoftwareEngineering #CleanCode #TreeTraversal
