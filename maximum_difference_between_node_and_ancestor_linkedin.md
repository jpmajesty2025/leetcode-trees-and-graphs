# Cracking LeetCode 1026: Maximum Difference Between Node and Ancestor (3 Ways) 🌲

When solving binary tree problems, the intuitive first approach often involves passing information up from subtrees or checking ancestor pairs. But what happens when you flip the mental model from **bottom-up aggregation** to **top-down state tracking**?

Let's dive into **LeetCode 1026: Maximum Difference Between Node and Ancestor**.

---

### 💡 The Core Insight

The problem asks for $\max |a.\text{val} - b.\text{val}|$ where $a$ is an ancestor of $b$.

Rather than comparing each node with all its ancestors individually ($\mathcal{O}(N^2)$ brute-force), recognize this fundamental property:
> **Along any root-to-leaf path, the maximum difference between any ancestor-descendant pair is simply:**
> $$\max(\text{path}) - \min(\text{path})$$

Because both the path minimum and path maximum lie on the same simple path from root to leaf, one is guaranteed to be an ancestor of the other!

Thus, we only need to track the `(min_val, max_val)` along each root-to-leaf traversal.

---

### 1️⃣ Approach 1: Top-Down Recursive DFS (Clean & Expressive)

In recursive DFS, we pass the running `(cur_min, cur_max)` down the call stack. When reaching a null child (past a leaf), we return `cur_max - cur_min`.

```python
from typing import Optional
from tree_node import TreeNode


def max_ancestor_diff(root: Optional[TreeNode]) -> int:
    """Recursive DFS tracking running min and max along root-to-leaf paths."""
    if not root:
        return 0

    def dfs(node: Optional[TreeNode], cur_min: int, cur_max: int) -> int:
        if not node:
            return cur_max - cur_min

        cur_min = min(cur_min, node.val)
        cur_max = max(cur_max, node.val)

        left_diff = dfs(node.left, cur_min, cur_max)
        right_diff = dfs(node.right, cur_min, cur_max)

        return max(left_diff, right_diff)

    return dfs(root, root.val, root.val)
```

- **Time Complexity:** $\mathcal{O}(N)$ — visits each node exactly once.
- **Space Complexity:** $\mathcal{O}(H)$ call stack space ($H = \log N$ balanced, $H = N$ skewed).

---

### 2️⃣ Approach 2: Explicit Iterative DFS (Production-Safe & Recursion-Proof)

In languages like Python with default recursion limits (e.g. 1000 frames), deep skewed trees can trigger `RecursionError`. We can eliminate call stack overhead using an explicit heap-allocated stack storing `(node, cur_min, cur_max)`.

```python
from typing import Optional
from tree_node import TreeNode


def max_ancestor_diff_iterative(root: Optional[TreeNode]) -> int:
    """Iterative DFS using an explicit stack."""
    if not root:
        return 0

    max_diff = 0
    stack = [(root, root.val, root.val)]

    while stack:
        node, cur_min, cur_max = stack.pop()
        cur_min = min(cur_min, node.val)
        cur_max = max(cur_max, node.val)

        # Evaluate difference at leaf nodes
        if not node.left and not node.right:
            max_diff = max(max_diff, cur_max - cur_min)
            continue

        if node.right:
            stack.append((node.right, cur_min, cur_max))
        if node.left:
            stack.append((node.left, cur_min, cur_max))

    return max_diff
```

- **Time Complexity:** $\mathcal{O}(N)$
- **Space Complexity:** $\mathcal{O}(H)$ explicit memory on the heap.

---

### 3️⃣ Approach 3: Level-Order BFS (Queue-based Exploration)

Prefer breadth-first exploration? We can track the path state level by level using a `deque`.

```python
from collections import deque
from typing import Optional
from tree_node import TreeNode


def max_ancestor_diff_bfs(root: Optional[TreeNode]) -> int:
    """Iterative BFS using a double-ended queue."""
    if not root:
        return 0

    max_diff = 0
    queue = deque([(root, root.val, root.val)])

    while queue:
        node, cur_min, cur_max = queue.popleft()
        cur_min = min(cur_min, node.val)
        cur_max = max(cur_max, node.val)

        if not node.left and not node.right:
            max_diff = max(max_diff, cur_max - cur_min)
            continue

        if node.left:
            queue.append((node.left, cur_min, cur_max))
        if node.right:
            queue.append((node.right, cur_min, cur_max))

    return max_diff
```

- **Time Complexity:** $\mathcal{O}(N)$
- **Space Complexity:** $\mathcal{O}(W)$ where $W$ is the maximum width of the tree (up to $N/2$ for balanced trees).

---

### ⚖️ Trade-off Summary

| Pattern | Time | Auxiliary Space | Best Suited For |
| :--- | :--- | :--- | :--- |
| **Recursive DFS** | $\mathcal{O}(N)$ | $\mathcal{O}(H)$ call stack | Interviews, readability, concise code |
| **Iterative DFS** | $\mathcal{O}(N)$ | $\mathcal{O}(H)$ heap memory | Skewed trees, systems with strict stack limits |
| **Iterative BFS** | $\mathcal{O}(N)$ | $\mathcal{O}(W)$ queue memory | Shallow wide trees, streaming / level processing |

---

### 🧪 Verification with Property-Based Testing
Beyond deterministic unit tests, we verified all 3 implementations against a brute-force $\mathcal{O}(N^2)$ oracle using **Hypothesis** across randomized trees with negative, zero, and boundary values. Zero discrepancies across 100+ generated test topologies!

---

What's your go-to strategy when handling binary tree path problems—top-down state propagation or bottom-up aggregation? Let's discuss in the comments! 👇

#Python #Algorithms #DataStructures #LeetCode #SoftwareEngineering #CodingInterview #CleanCode
