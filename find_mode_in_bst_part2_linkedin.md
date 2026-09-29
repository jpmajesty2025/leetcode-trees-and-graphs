# Zero-Auxiliary Memory BST Mode Finding: The Morris Traversal Follow-Up 🌲🧙‍♂️

In Part 1, we eliminated hash map allocations by streaming in-order values on-the-fly, reducing auxiliary memory to $\mathcal{O}(H)$ stack space.

Now let's tackle the famous LeetCode follow-up challenge:
*Could you do that without allocating any extra space, where the implicit stack memory does not count?*

Can we find all modes in strictly **$\mathcal{O}(1)$ auxiliary space** without any recursion or stack?

**Morris Inorder Traversal** makes it possible by threading unused leaf pointers!

---

### 💡 The Core Mechanism: Threaded Predecessors

Instead of maintaining a call stack or heap stack to traverse back up the tree:
1️⃣ For each node `curr` with a left child, find its **in-order predecessor** (the rightmost node of its left subtree).
2️⃣ **Create Thread (1st Visit)**: Set `predecessor.right = curr` and move left: `curr = curr.left`.
3️⃣ **Process & Restore (2nd Visit)**: When `predecessor.right is curr`, the left subtree is fully processed:
   • Dismantle the thread: `predecessor.right = None`
   • Update frequency streaks and mode candidates
   • Move right: `curr = curr.right`

When Morris Traversal finishes, **all modified pointers are restored to their exact original structure**.

---

### ⚡ Mode Updating on the Fly

As Morris Traversal visits each node in sorted order, we maintain the streak logic:
```python
def update_mode(val: int) -> None:
    nonlocal prev, count, max_count, modes
    count = (count + 1) if (prev is not None and val == prev) else 1
    if count > max_count:
        max_count = count
        modes = [val]
    elif count == max_count:
        modes.append(val)
    prev = val
```

---

### 📊 Strategy Comparison

| Feature | Hash Map (`Counter`) | Streaming In-Order DFS | Morris Inorder Traversal |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| **Auxiliary Memory** | $\mathcal{O}(N)$ dictionary | $\mathcal{O}(H)$ call stack | **$\mathcal{O}(1)$ (Zero Stack/Heap)** |
| **Passes Over Tree** | 2 passes | 1 pass | **1 pass** |
| **Pointer Mutation** | None | None | **Self-Restoring Threads** |

---

### 🎯 Key Engineering Takeaways

• **Follow-Up Mastery**: Achieving true $\mathcal{O}(1)$ auxiliary space on tree traversals is a premier demonstration of low-level pointer manipulation and data structure mastery.
• **Concurrency Trade-Off**: Because pointers are temporarily modified during exploration, Morris Traversal is not thread-safe without synchronization.

Check out the clean Morris Traversal implementation in the attached image! 📸

How often do you reach for threaded binary trees in performance-critical code? Let's discuss in the comments! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #EmbeddedSystems #ComputerScience
