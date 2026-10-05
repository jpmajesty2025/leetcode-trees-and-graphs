# Iterative Queue BFS: Validating Symmetric Trees Without Recursion 🌲🛡️

In Part 1, we formulated tree mirror symmetry as a dual-tree recursive predicate in O(H) call-stack space.

*How can we translate this pairwise symmetry logic into an iterative queue-based BFS that is 100% stack-safe?*

Let's dissect the **Iterative Pair BFS Pattern**.

---

### 💡 Enqueuing Symmetric Pairs

Instead of enqueuing individual nodes, we enqueue **symmetric tuples**: `(t1, t2)`!

1. Initialize `queue = deque([(root.left, root.right)])`.
2. While `queue` is not empty, pop `(t1, t2)`:
   • If both are `None` ➡️ Continue (empty subtrees are symmetric).
   • If only one is `None` OR `t1.val != t2.val` ➡️ Return `False` immediately.
3. Push the symmetric child pairs:
   • **Outer Pair**: `queue.append((t1.left, t2.right))`
   • **Inner Pair**: `queue.append((t1.right, t2.left))`
4. If queue exhausts without mismatches ➡️ Return `True`.

---

### ⚡ Clean Iterative BFS Code

```python
from collections import deque

def is_symmetric_bfs(root: TreeNode | None) -> bool:
    if not root:
        return True

    queue = deque([(root.left, root.right)])
    while queue:
        t1, t2 = queue.popleft()

        if not t1 and not t2:
            continue
        if not t1 or not t2 or t1.val != t2.val:
            return False

        queue.append((t1.left, t2.right))
        queue.append((t1.right, t2.left))

    return True
```

---

### 📊 Strategy Comparison

| Traversal Strategy | Time Complexity | Auxiliary Space | Call Stack Overflow Risk |
| :--- | :--- | :--- | :--- |
| **Recursive Mirror DFS** | O(N) | O(H) Call Stack | Yes (on skewed trees) |
| **Iterative Pair BFS** | **O(N)** | **O(W) Queue (Width)** | **Zero (Heap-allocated)** |
| **Iterative Pair Stack DFS** | **O(N)** | **O(H) Heap Stack** | **Zero (Heap-allocated)** |

---

### 🎯 Key Engineering Takeaways

• **Tuple Enqueueing**: Grouping interdependent nodes as tuples in FIFO queues simplifies state synchronization across multi-tree comparisons.
• **Breadth vs Depth Memory**: Iterative BFS checks the tree level-by-level, failing early at shallow depths if asymmetry occurs near the root.

Check out both implementations in the attached image! 📸

Do you prefer recursive invariants or iterative tuple queues for tree validation? Let's discuss in the comments! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CleanCode #Performance
