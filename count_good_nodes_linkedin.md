**Mastering Binary Trees: Tracking Path Maximums with Recursive DFS 🌲**

**Problem statement:**
Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with a value greater than X. Return the number of good nodes in the binary tree.

This is **top-down state propagation** and we can solve it with clean, recursive Depth-First Search:

---

### The Strategy: Propagate the Monotonic Upper Bound

As we traverse downward from the root, we don't need the entire ancestor history—we only need the **maximum value seen so far on the current path**.

- Seed the traversal with the root value: `max_val = root.val`.
- If `node.val >= max_val`, this node is "good" (`is_good = 1`).
- Update the maximum for child calls: `new_max = max(max_val, node.val)`.
- Recursively aggregate counts: `is_good + dfs(left) + dfs(right)`.

```python
def good_nodes(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    def dfs(node: Optional[TreeNode], max_val: int) -> int:
        if not node:
            return 0

        is_good = 1 if node.val >= max_val else 0
        new_max = max(max_val, node.val)

        return is_good + dfs(node.left, new_max) + dfs(node.right, new_max)

    return dfs(root, root.val)
```

---

### Complexity Analysis

- ⏱️ **Time Complexity:** **O(N)** — every node in the tree is visited exactly once.
- 💾 **Space Complexity:** **O(H)** — call stack depth proportional to tree height H -> `O(log N)` balanced, `O(N)` skewed (worst case).

---

### Key Takeaway

Top-down recursive DFS is the most intuitive fit when a node's validity depends solely on a monotonic summary (like `max_so_far` or `path_sum`) flowing down from ancestors.

#LearningInPublic #SoftwareEngineering #Python #LeetCode #DataStructures #Algorithms #Recursion #CleanCode #TechInterview
