# Memory Profiles: Mutable Backtracking Stack vs Queue BFS 🌲🧙‍♂️

In Part 1, we used a single backtracking stack to collect all matching root-to-leaf paths in O(H) auxiliary space.

*What happens when we implement Path Sum II using Level-Order BFS or immutable tuples?*

Let's dissect the memory and garbage collection profiles.

---

### 💡 Iterative BFS Path Propagation

In Breadth-First Search, nodes at different depths and across different branches are processed concurrently.

Because multiple paths are active simultaneously, a single shared stack is impossible. Each queue entry must hold its own immutable path copy:

```python
from collections import deque

def path_sum_bfs(root: TreeNode | None, target_sum: int) -> list[list[int]]:
    if not root:
        return []

    result = []
    # Queue stores: (node, remaining_sum, path_so_far)
    queue = deque([(root, target_sum - root.val, [root.val])])

    while queue:
        node, remaining, path = queue.popleft()

        if not node.left and not node.right and remaining == 0:
            result.append(path)
            continue

        if node.left:
            queue.append((node.left, remaining - node.left.val, path + [node.left.val]))
        if node.right:
            queue.append((node.right, remaining - node.right.val, path + [node.right.val]))

    return result
```

---

### 📊 Strategy & Memory Comparison

| Dimension | Shared Backtracking DFS | Iterative Path BFS | Naive Immutable DFS |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | **O(N + K * H)** | O(N * H) | O(N * H) |
| **Auxiliary Memory** | **O(H) Single Stack** | O(N * H) Queue Tuples | O(N * H) Call Stack Lists |
| **Heap Allocations** | **K Snapshots only** | Every branch extension | Every recursive call |
| **Stack Safety** | Call Stack Bounded | **100% Stack Safe** | Call Stack Bounded |

---

### 🎯 Key Engineering Takeaways

• **Sequential vs Concurrent Path State**: DFS follows a single linear exploration path at any instant, making a single mutable stack with `append`/`pop` optimal.
• **GC Overhead Awareness**: In high-throughput backend services, avoiding intermediate array copies (`path + [node.val]`) drastically reduces memory allocator churn and tail latency spikes.

Check out both implementations in the attached image! 📸

Do you prefer backtracking with mutable state or immutable data propagation in production pipelines? Let's discuss in the comments! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CleanCode #Performance
