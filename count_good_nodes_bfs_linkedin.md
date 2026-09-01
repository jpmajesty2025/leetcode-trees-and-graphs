**Mastering Binary Trees: Breadth-First Search (BFS) for Good Nodes 🌲**

Most path-property problems are tackled with Depth-First Search. But did you know that **Breadth-First Search (BFS)** can evaluate path-monotonic properties like **LeetCode 1448 (Count Good Nodes in Binary Tree)** just as effectively?

Here is how layer-by-layer traversal handles branch ancestor maximums.

---

### The Strategy: Level-Order Queue with State Snapshotting

Using a double-ended queue (`collections.deque`), we traverse the tree level by level while associating each node with the maximum value on its root-to-node path:
- Initialize `queue = deque([(root, root.val)])`.
- Pop `(node, max_val)` from the front of the queue.
- If `node.val >= max_val`, increment `count` and update `max_val = node.val`.
- Enqueue children with the updated branch maximum.

```python
from collections import deque
from typing import Optional
from tree_node import TreeNode


def good_nodes_bfs(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    count = 0
    queue = deque([(root, root.val)])

    while queue:
        node, max_val = queue.popleft()
        if node.val >= max_val:
            count += 1
            max_val = node.val

        if node.left:
            queue.append((node.left, max_val))
        if node.right:
            queue.append((node.right, max_val))

    return count
```

---

### Complexity & Memory Trade-offs: BFS vs. DFS

- ⏱️ **Time Complexity:** **O(N)** — every node is processed once.
- 💾 **Space Complexity:** **O(W)** — proportional to the maximum width of the tree.
  - **In Skewed Trees:** BFS queue size stays **O(1)**, while DFS stack memory grows to **O(N)**!
  - **In Balanced Trees:** BFS queue size reaches `⌈N/2⌉` at the bottom layer (**O(N)**), while DFS stack memory is only **O(log N)**.

---

### Engineering Takeaway

Understanding the memory trade-off between **Tree Height (DFS)** and **Tree Width (BFS)** allows you to select the optimal traversal strategy based on the shape of your data.

When analyzing trees or graph structures, how do you decide between BFS and DFS? Let's discuss below! 👇

#SoftwareEngineering #Python #LeetCode #DataStructures #Algorithms #BFS #BreadthFirstSearch #CleanCode #TechInterview
