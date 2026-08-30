**Mastering Binary Trees: The Power of Recursive Subtraction for Path Sum 🌲**

Finding whether a binary tree has a root-to-leaf path that sums to a target value (**LeetCode 112: Path Sum**) is a classic tree traversal problem. While many developers reach for an accumulator variable, there is a much cleaner, more functional way to solve it.

Here is an in-depth breakdown of the **Recursive Direct Subtraction** pattern:

---

### The Strategy: Subtract as You Descend

Instead of carrying a running sum downward (`0 -> 5 -> 9 -> 20`), subtract each node's value from the remaining target at every recursive call:
- At each node, ask: *"Does a child path sum to `remaining - node.val`?"*
- When you reach a **leaf node** (`not node.left and not node.right`), simply check:
  `root.val == targetSum`

```python
def has_path_sum(root: Optional[TreeNode], targetSum: int) -> bool:
    if not root:
        return False

    # Base case: Leaf node check
    if not root.left and not root.right:
        return root.val == targetSum

    remaining = targetSum - root.val
    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)
```

---

### Complexity & Trade-Offs

- ⏱️ **Time Complexity:** **O(N)** — in the worst case, every node is visited once. The boolean `or` provides automatic short-circuiting as soon as the first valid path is found.
- 💾 **Space Complexity:** **O(H)** — where `H` is the height of the tree (`O(log N)` for balanced trees, `O(N)` for skewed trees) due to the call stack frames.

---

### Key Engineering Insights

1. **Strict Leaf Validation:** A common bug is returning `True` when an intermediate node reaches the target sum. Checking `not root.left and not root.right` guarantees that only full root-to-leaf paths are accepted.
2. **Elimination of State Overhead:** Decrementing the target directly removes the need for inner closure functions or mutable state tracking.
3. **The Recursion Risk:** While elegant, deep skewed trees can risk `RecursionError` in Python if the call stack exceeds system limits (~1,000 frames).

What’s your favorite recursion pattern for tree problems? Let’s connect and discuss below! 👇

#SoftwareEngineering #Python #LeetCode #DataStructures #Algorithms #Recursion #CleanCode #TechInterview
