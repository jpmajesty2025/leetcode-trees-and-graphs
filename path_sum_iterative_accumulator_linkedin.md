**Mastering Binary Trees: Iterative DFS with Path Accumulator 🌲**

When traversing tree structures to find path sums (**LeetCode 112**), one of the most natural mental models is the **accumulator pattern**: tracking the running sum as you descend from the root.

Here is how to implement this cleanly and safely using an **Iterative DFS with an Accumulator**.

---

### The Strategy: Snapshotting Prefix Sums

In an iterative stack, managing path state can be tricky because multiple branches fork from common ancestors. The solution? Store immutable snapshots of the running sum along with the node in the stack tuple: `(node, current_sum)`.

- Start with `stack = [(root, root.val)]`.
- At each step, pop `(node, curr_sum)`.
- If the node is a leaf and `curr_sum == targetSum`, return `True`.
- For each child, push `(child, curr_sum + child.val)` to fork the accumulated path sum cleanly.

```python
def has_path_sum_accumulator(root: Optional[TreeNode], targetSum: int) -> bool:
    if not root:
        return False

    stack = [(root, root.val)]
    while stack:
        node, curr_sum = stack.pop()
        
        # Leaf node check
        if not node.left and not node.right and curr_sum == targetSum:
            return True

        if node.right:
            stack.append((node.right, curr_sum + node.right.val))
        if node.left:
            stack.append((node.left, curr_sum + node.left.val))

    return False
```

---

### Why Snapshotting Works Seamlessly

- **No Backtracking Overhead:** Because each tuple maintains an independent `curr_sum`, backtracking happens automatically when the stack unwinds to previous branches—no state mutation or rollbacks required.
- ⏱️ **Time Complexity:** **O(N)** — each node is processed once with immediate short-circuiting on success.
- 💾 **Space Complexity:** **O(H)** — bounded by tree height on the heap.

---

### Engineering Comparison: Accumulator vs. Subtraction

| Traversal Strategy | State Tracked | Leaf Condition |
| :--- | :--- | :--- |
| **Accumulator** | Prefix sum from root (`0 -> sum`) | `curr_sum == targetSum` |
| **Subtraction** | Remaining budget (`targetSum -> 0`) | `remaining == 0` |

Both paradigms achieve optimal performance, but the accumulator approach often aligns more directly with logging and path reconstruction.

How do you approach branch state management in non-recursive algorithms? Let's discuss below! 👇

#SoftwareEngineering #Python #LeetCode #DataStructures #Algorithms #DFS #CleanCode #TechInterview
