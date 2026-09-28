# Breaking the O(H) Memory Barrier: Morris Inorder Traversal in O(1) Space 🌲🧙‍♂️

In Part 1, we examined how replacing recursive DFS with an explicit stack eliminates recursion stack overflow on deep binary trees.

Yet both approaches still consume $\mathcal{O}(H)$ auxiliary space (where $H$ is the tree height).

*Can you traverse a binary tree in $\mathcal{O}(1)$ auxiliary space without any stack or recursion?*

Enter **Morris Traversal** (invented by J. H. Morris in 1979).

---

### 💡 The Core Mechanism: Threaded Binary Trees

Morris Traversal utilizes the unused `None` right-child pointers of leaf nodes to build temporary "threads" back to ancestor nodes:

1️⃣ **Find In-Order Predecessor**:
For any node `curr` with a left child, find the rightmost node in its left subtree:
`predecessor = curr.left` (then march right until `None` or `curr`).

2️⃣ **Thread Creation (1st Visit)**:
If `predecessor.right is None`:
• Create a temporary pointer: `predecessor.right = curr`
• Move to `curr = curr.left`

3️⃣ **Pointer Restoration (2nd Visit)**:
If `predecessor.right is curr`:
• Thread already exists! Dismantle it: `predecessor.right = None`
• Process the node value: `result.append(curr.val)`
• Move to `curr = curr.right`

When traversal finishes, **every single pointer is restored to its exact original state**.

---

### 📊 Strategy Comparison

| Strategy | Time Complexity | Auxiliary Space | Mutates Tree Permanently? |
| :--- | :--- | :--- | :--- |
| **Recursive DFS** | $\mathcal{O}(N)$ | $\mathcal{O}(H)$ call stack | ❌ No |
| **Iterative Stack** | $\mathcal{O}(N)$ | $\mathcal{O}(H)$ heap stack | ❌ No |
| **Morris Traversal** | $\mathcal{O}(N)$ | **$\mathcal{O}(1)$ (Constant)** | ❌ **No (Self-Restoring)** |

---

### 🎯 Key Engineering Takeaways

• **Zero Memory Footprint**: Morris Traversal is ideal for embedded hardware, memory-constrained IoT systems, or massive datasets where $\mathcal{O}(H)$ stack space cannot be allocated.
• **Concurrency Trade-Off**: Because tree pointers are modified temporarily during traversal, Morris Traversal is **not thread-safe** for simultaneous readers without synchronization.

Check out the clean Morris Traversal implementation in the attached image! 📸

Have you ever used threaded binary trees in low-level or embedded software? Let's discuss in the comments! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #EmbeddedSystems #ComputerScience
