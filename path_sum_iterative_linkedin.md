**Mastering Binary Trees: Iterative Depth First Search (DFS) with Target Subtraction 🌲**

When solving DFS tree problems in production systems, deep or untrusted inputs can easily blow past Python's default recursion stack limit. 

How do we retain the mathematical elegance of the **target subtraction** approach without risking a `RecursionError`? By moving recursion to an **explicit heap stack**.

---

### The Strategy: Explicit Stack + Remaining Target

We simulate the recursive call stack on the heap by storing tuples of `(node, remaining_sum_needed)`:
- Initialize the stack with `(root, targetSum - root.val)`.
- When popping a leaf node (`not node.left and not node.right`), check if `remaining == 0`.
- Push valid children to the stack with their updated `remaining - child.val`.

```python
def has_path_sum_iterative(root: Optional[TreeNode], targetSum: int) -> bool:
    if not root:
        return False

    stack = [(root, targetSum - root.val)]
    while stack:
        node, remaining = stack.pop()
        
        # Leaf node check
        if not node.left and not node.right and remaining == 0:
            return True

        if node.right:
            stack.append((node.right, remaining - node.right.val))
        if node.left:
            stack.append((node.left, remaining - node.left.val))

    return False
```

---

### Complexity & Architectural Advantages

- ⏱️ **Time Complexity:** **O(N)** — visits each node at most once, terminating immediately upon reaching the first matching leaf.
- 💾 **Space Complexity:** **O(H)** — stack depth is bounded by tree height (`O(log N)` balanced, `O(N)` skewed).
- 🛡️ **Stack Overflow Immune:** Unlike the system call stack (typically ~1,000 frames in Python), heap memory can easily accommodate millions of nodes.

---

### Key Takeaway

By pairing an explicit DFS stack with the top-down subtraction pattern, we get the best of both worlds: clean remaining-budget logic and bulletproof runtime safety for deep or skewed binary trees.

Do you prefer explicit stacks over recursion in production code? Let’s hear your thoughts! 👇

#LearningInPublic #SoftwareEngineering #Python #LeetCode #DataStructures #Algorithms #Stack #Tree #Graph #DFS #SystemDesign #CleanCode #TechInterview
