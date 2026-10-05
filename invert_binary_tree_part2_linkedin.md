# Call-Stack Safety: Recursion vs Level-Order BFS in Tree Transformations 🌲🛡️

In Part 1, we examined the recursive symmetry of inverting binary trees.

*While recursion is concise, what happens when a binary tree degenerates into a linked list with 10,000 nodes?*

In Python, the default recursion limit is 1,000 frames. Deep recursion triggers a `RecursionError: maximum recursion depth exceeded`.

How can we invert trees safely in production without risking call-stack overflow?

---

### 💡 Pattern 1: Iterative Level-Order BFS

Instead of exploring depth-first, we can process nodes layer-by-layer using a FIFO queue (`collections.deque`):

```python
from collections import deque

def invert_tree_bfs(root: TreeNode | None) -> TreeNode | None:
    if not root:
        return None

    queue = deque([root])
    while queue:
        curr = queue.popleft()
        curr.left, curr.right = curr.right, curr.left

        if curr.left:
            queue.append(curr.left)
        if curr.right:
            queue.append(curr.right)

    return root
```

**Why it shines**:
• Memory is bounded by the maximum **width** `W` of the tree (`W <= N / 2` for full binary trees, `W = 1` for skewed trees).
• Skewed degenerate trees consume only `O(1)` queue memory!

---

### 💡 Pattern 2: Iterative Stack DFS

If we prefer depth-first traversal without call-stack risks:
• Allocate an explicit list on the heap: `stack = [root]`.
• While stack is non-empty, pop node, swap children, and push non-null children.

**Why it shines**:
• Operates in `O(H)` space on the heap, bypassing OS/Python call-stack limits entirely.

---

### 📊 Strategy Comparison

| Dimension | Recursive DFS | Iterative Level BFS | Iterative Stack DFS |
| :--- | :--- | :--- | :--- |
| **Code Simplicity** | Highest (4 lines) | Clean (12 lines) | Clean (12 lines) |
| **Space Complexity**| O(H) Call Stack | O(W) Queue (Width) | O(H) Heap Stack |
| **Worst-Case for Skewed Tree** | **O(N) (Stack Crash Risk!)** | **O(1) Memory (Safe!)** | **O(N) Heap (Safe!)** |
| **Worst-Case for Full Tree** | O(log N) | O(N / 2) | O(log N) |

---

### 🎯 Key Engineering Takeaways

• **Stack Safety**: When processing user-generated trees (e.g. ASTs, XML/DOM trees, filesystem hierarchies), prefer iterative BFS or heap-allocated stacks to guard against deep nesting crashes.
• **Memory Layout Awareness**: BFS memory scales with width, DFS memory scales with height. Choose based on anticipated tree topologies!

Check out all three patterns in the attached image! 📸

How do you protect your production parsers and tree visitors from recursion limits? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CleanCode #Performance
