# BFS vs. DFS: Summing the Deepest Leaves in Binary Trees 🌲🍃

When aggregating values at the deepest layer of a tree, how do you balance **intuitive level-order processing** against **memory-efficient depth traversal** and **stack safety**?

Let's break down **LeetCode 1302: Deepest Leaves Sum** and explore the architectural trade-offs across Breadth-First Search (BFS), Recursive DFS, and Iterative DFS.

---

### 💡 The Problem
Given the `root` of a binary tree, return the sum of values of its deepest leaves (i.e., all nodes located at the tree's maximum depth).

---

### 1️⃣ Approach 1: Level-Order BFS (The Natural & Intuitive Fit)

Because the problem specifically asks for properties of the *deepest* horizontal row, Breadth-First Search offers an elegant mental model:
1. Traverse the tree layer by layer using a `deque`.
2. At the start of each level, reset `deepest_sum = 0`.
3. Accumulate node values across the current level.
4. When the loop terminates, `deepest_sum` holds the sum of the final (deepest) layer!

```python
from collections import deque
from typing import Optional
from tree_node import TreeNode


def deepest_leaves_sum(root: Optional[TreeNode]) -> int:
    """Iterative BFS level-order traversal."""
    if not root:
        return 0

    queue = deque([root])
    deepest_sum = 0

    while queue:
        deepest_sum = 0
        for _ in range(len(queue)):
            node = queue.popleft()
            deepest_sum += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return deepest_sum
```

**Key Advantage:** Self-contained and level-scoped — no need to track or compare explicit depth indices.

---

### 2️⃣ Approach 2: Recursive DFS (Memory-Efficient for Balanced Trees)

Can we do this in a single recursive DFS pass? Yes, by tracking `max_depth` dynamically:
- If `depth > max_depth`: We've discovered a strictly deeper layer! Update `max_depth = depth` and reset `total = node.val`.
- If `depth == max_depth`: Another leaf at the current deepest layer $\to$ add `total += node.val`.
- If `depth < max_depth`: Ignore.

```python
from typing import Optional
from tree_node import TreeNode


def deepest_leaves_sum_dfs(root: Optional[TreeNode]) -> int:
    """Single-pass DFS tracking maximum depth dynamically."""
    if not root:
        return 0

    max_depth = -1
    total = 0

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        nonlocal max_depth, total
        if not node:
            return

        if depth > max_depth:
            max_depth = depth
            total = node.val
        elif depth == max_depth:
            total += node.val

        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return total
```

**Key Advantage:** Uses only $\mathcal{O}(H)$ call stack space ($\mathcal{O}(\log N)$ on balanced trees), compared to BFS's queue storing up to $N/2$ nodes at the widest level.

---

### 3️⃣ Approach 3: Iterative DFS with Explicit Stack (Stack-Safe for Deep Trees)

For environments with strict call stack limits (e.g., Python's 1,000 recursion frame limit), we can move the call frame onto the heap using an explicit stack of `(node, depth)` tuples:

```python
from typing import Optional, List, Tuple
from tree_node import TreeNode


def deepest_leaves_sum_iterative(root: Optional[TreeNode]) -> int:
    """Iterative DFS using an explicit stack."""
    if not root:
        return 0

    max_depth = -1
    total = 0
    stack: List[Tuple[TreeNode, int]] = [(root, 0)]

    while stack:
        node, depth = stack.pop()

        if depth > max_depth:
            max_depth = depth
            total = node.val
        elif depth == max_depth:
            total += node.val

        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))

    return total
```

**Key Advantage:** Guarantees zero `RecursionError` risk even on skewed trees with tens of thousands of levels.

---

### ⚖️ Architectural Trade-off Summary

| Metric | Level-Order BFS | Recursive DFS | Iterative DFS (Stack) |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| **Auxiliary Space (Balanced Tree)** | $\mathcal{O}(N)$ queue ($\approx N/2$ nodes) | $\mathcal{O}(\log N)$ call stack | $\mathcal{O}(\log N)$ heap stack |
| **Auxiliary Space (Skewed Tree)** | $\mathcal{O}(1)$ queue | $\mathcal{O}(N)$ call stack | $\mathcal{O}(N)$ heap stack |
| **State Management** | Level-scoped reset per iteration | Dynamic `(max_depth, total)` state | Dynamic `(max_depth, total)` state |
| **Stack Overflow Risk** | None | Possible if depth > 1,000 | None |

---

### 🧪 Property-Based Verification
Using **Hypothesis**, all three implementations were validated against an independent oracle across random trees with varied topologies, single nodes, asymmetric branches, and negative values with 100% agreement.

---

When designing tree traversals in production pipelines, do you default to BFS for simplicity or DFS for memory optimization? Let's discuss in the comments! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #TreeTraversal
