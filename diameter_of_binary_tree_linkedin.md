# Demystifying LeetCode 543: Diameter of Binary Tree (Functional Recursion vs. Iterative Post-Order) 🌲

When finding the longest path in a binary tree, many developers quickly write a helper with a global or `nonlocal` variable. But how do we scale this into clean, functional code or production-ready iterative systems that never blow up the call stack?

Let's explore **LeetCode 543: Diameter of Binary Tree** through two distinct engineering lenses!

---

### 💡 The Core Problem & Intuition

The diameter of a binary tree is the **longest path (number of edges) between any two nodes**. Crucially:
> **The longest path does NOT necessarily pass through the root.**

At any given node `u`, the longest path where `u` acts as the highest ancestor is:
$$\text{path\_length}(u) = \text{depth}(\text{left\_subtree}) + \text{depth}(\text{right\_subtree})$$

The tree's diameter is simply $\max_{u \in \text{Tree}} \text{path\_length}(u)$.

---

### 1️⃣ Solution 1: Pure Functional Recursion (No `nonlocal`, No Mutation)

Instead of mutating an external state variable, the post-order recursive helper returns a tuple: `(depth, max_diameter_in_subtree)`.

```python
from typing import Optional, Tuple
from tree_node import TreeNode


def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    """Pure functional recursion returning (depth, diameter)."""
    def dfs(node: Optional[TreeNode]) -> Tuple[int, int]:
        if not node:
            return 0, 0  # (depth, diameter)

        left_depth, left_diam = dfs(node.left)
        right_depth, right_diam = dfs(node.right)

        current_depth = max(left_depth, right_depth) + 1
        current_diam = max(left_diam, right_diam, left_depth + right_depth)

        return current_depth, current_diam

    return dfs(root)[1]
```

#### Why this is great:
- **Zero Side Effects:** Self-contained, immutable, deterministic, and easy to reason about in parallel or concurrent settings.
- **Complexity:** $\mathcal{O}(N)$ Time, $\mathcal{O}(H)$ Call Stack Space ($H = \text{tree height}$).

---

### 2️⃣ Solution 2: Explicit Stack Iterative Post-Order (Recursion-Proof)

In environments with strict stack limits (like Python's 1,000 recursion frame limit), deep skewed trees risk a `RecursionError`. We can simulate the post-order traversal using an explicit stack on the heap and a hash map of computed subtree depths.

```python
from typing import Optional, Dict
from tree_node import TreeNode


def diameter_of_binary_tree_iterative(root: Optional[TreeNode]) -> int:
    """Iterative post-order traversal using an explicit stack."""
    if not root:
        return 0

    max_diameter = 0
    stack = [root]
    depths: Dict[Optional[TreeNode], int] = {None: 0}

    while stack:
        node = stack[-1]

        # Push unvisited children to stack (post-order: process children before parent)
        if (node.left and node.left not in depths) or (node.right and node.right not in depths):
            if node.right and node.right not in depths:
                stack.append(node.right)
            if node.left and node.left not in depths:
                stack.append(node.left)
        else:
            stack.pop()
            left_depth = depths[node.left]
            right_depth = depths[node.right]

            max_diameter = max(max_diameter, left_depth + right_depth)
            depths[node] = max(left_depth, right_depth) + 1

    return max_diameter
```

#### Why this is great:
- **Stack-Overflow Immune:** Safe for arbitrarily deep trees ($N = 100,000+$).
- **Complexity:** $\mathcal{O}(N)$ Time, $\mathcal{O}(N)$ Heap Space.

---

### ⚖️ Architectural Comparison

| Metric | Functional Recursive | Iterative Post-Order |
| :--- | :--- | :--- |
| **Paradigm** | Declarative / Functional | Imperative / Stack Simulation |
| **Time Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| **Auxiliary Space** | $\mathcal{O}(H)$ Call Stack | $\mathcal{O}(N)$ Heap (Stack + Depths Map) |
| **Strengths** | Concise, zero mutation, elegant | Stack safety, resilience on skewed inputs |

---

### 🧪 Verified with Property-Based Testing
Both solutions were verified with **Hypothesis** against an independent brute-force $\mathcal{O}(N^2)$ oracle across arbitrary tree topologies, single nodes, linear chains, and balanced configurations with 100% agreement.

---

Do you prefer pure functional returns or explicit state loops in tree algorithms? Share your thoughts below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #FunctionalProgramming #CleanCode
