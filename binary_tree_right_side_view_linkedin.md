# LeetCode 199: Binary Tree Right Side View (BFS vs. Right-First DFS) 👁️🌲

When looking at a binary tree from the right side, which nodes do you actually see?

It's tempting to think you only see the right children. But if the left subtree goes deeper than the right subtree, those deeper left nodes peek through!

Let's explore two optimal ways to solve **LeetCode 199: Binary Tree Right Side View**.

---

### 💡 The Core Problem

Given a binary tree, return the values of the visible nodes when looking from the right side, ordered from top to bottom.

**Key Insight:** For each depth level in the tree, we need exactly **one** node: the rightmost node at that depth.

---

### 1️⃣ Approach 1: Level-Order BFS (Intuitive & Breadth-First)

BFS visits nodes level by level using a `deque`. At each level, the last element in the queue is by definition the rightmost visible node.

```python
from collections import deque
from typing import Optional, List
from tree_node import TreeNode


def right_side_view(root: Optional[TreeNode]) -> List[int]:
    """Iterative BFS level-order traversal."""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        result.append(queue[-1].val)  # Rightmost element at this level

        for _ in range(level_size):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return result
```

- **Time Complexity:** $\mathcal{O}(N)$ — each node is visited once.
- **Space Complexity:** $\mathcal{O}(W)$ where $W$ is maximum tree width (up to $N/2$ for balanced trees).

---

### 2️⃣ Approach 2: Right-to-Left Recursive DFS (Memory-Efficient)

Can we do it in $\mathcal{O}(H)$ space instead of $\mathcal{O}(W)$?

Yes! By traversing the **right child before the left child**, the first node we encounter at any depth level $d$ is guaranteed to be the rightmost node. We append it to `result` whenever `len(result) == depth`.

```python
from typing import Optional, List
from tree_node import TreeNode


def right_side_view_dfs(root: Optional[TreeNode]) -> List[int]:
    """Right-first recursive DFS."""
    result = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if not node:
            return

        # First time visiting this depth level -> rightmost node!
        if depth == len(result):
            result.append(node.val)

        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)

    dfs(root, 0)
    return result
```

- **Time Complexity:** $\mathcal{O}(N)$
- **Space Complexity:** $\mathcal{O}(H)$ call stack space ($H = \log N$ balanced, $H = N$ skewed).

---

### ⚖️ Trade-off Comparison

| Dimension | Level-Order BFS | Right-First DFS |
| :--- | :--- | :--- |
| **Traversal Order** | Level by level (Top to Bottom) | Depth-first (Right child first) |
| **Time Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| **Space Complexity** | $\mathcal{O}(W)$ Queue | $\mathcal{O}(H)$ Call Stack |
| **Best Memory Usage** | Tall, skinny / skewed trees ($W = 1$) | Wide, balanced trees ($H = \log N$) |
| **Intuition** | Very natural mental model | Clever condition (`len(result) == depth`) |

---

### 🧪 Verification with Property-Based Testing
Using **Hypothesis**, both implementations were tested against an independent level-order oracle across randomized tree structures, single nodes, linear chains, and deep unbalanced subtrees with 100% agreement.

---

Do you default to BFS for level-by-level problems, or do you prefer right-first DFS to optimize space on balanced trees? Drop your thoughts below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #TreeAlgorithms #CleanCode
