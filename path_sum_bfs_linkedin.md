**Mastering Binary Trees: Solving Path Sum with Breadth-First Search (BFS) 🌲**

When solving a path sum problem on a tree, you might be inclned to instinctively reach for Depth-First Search (DFS). Indeed, the three prior installations of this series did just that. But what if the tree is vast, and a valid path sum exists at a shallow depth?

This is where **Iterative Breadth-First Search (BFS)** shines!

---

### The Strategy: Level-by-Level Path Exploration

Using a FIFO queue (e.g. using `collections.deque`), we explore all nodes layer-by-layer while tracking the cumulative path sum for each branch:
- Enqueue `(root, root.val)`.
- Dequeue `(node, curr_sum)` from the front of the queue.
- If the node is a leaf and `curr_sum == targetSum`, return `True` immediately.
- Enqueue children with their respective accumulated sums: `(child, curr_sum + child.val)`.

```python
from collections import deque
from typing import Optional
from tree_node import TreeNode


def has_path_sum_bfs(root: Optional[TreeNode], targetSum: int) -> bool:
    if not root:
        return False

    queue = deque([(root, root.val)])
    while queue:
        node, curr_sum = queue.popleft()

        # Leaf node check
        if not node.left and not node.right and curr_sum == targetSum:
            return True

        if node.left:
            queue.append((node.left, curr_sum + node.left.val))
        if node.right:
            queue.append((node.right, curr_sum + node.right.val))

    return False
```

---

### Complexity & Memory Dynamics: BFS vs. DFS

- ⏱️ **Time Complexity:** **O(N)** — in the worst case, visits all nodes. However, if a shallow leaf satisfies the target sum, BFS will discover it much earlier than deep DFS branches.
- 💾 **Space Complexity:** **O(W)** — where `W` is the maximum width of the tree.
  - In a balanced binary tree, the leaf layer has up to `⌈N/2⌉` nodes, making space **O(N)**.
  - In a tall, skewed tree (linked-list shape), width is `O(1)`, making BFS extremely memory efficient!

---

### Architectural Takeaway

- **Use DFS (Stack/Recursion)** when the tree is wide and balanced, prioritizing minimal memory footprint (`O(log N)` height vs `O(N)` width).
- **Use BFS (Queue)** when you want shortest/shallowest path guarantees, or when dealing with narrow, deep trees where level-order guarantees prevent deep call stacks.

When do you choose BFS over DFS for tree-based search problems? Share your thoughts below! 👇

#LearningInPublic #SoftwareEngineering #Python #LeetCode #DataStructures #Algorithms #DFS #BFS #BreadthFirstSearch #TechInterview #CleanCode
