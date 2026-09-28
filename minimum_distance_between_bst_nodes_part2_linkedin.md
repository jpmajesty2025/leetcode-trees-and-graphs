# Zero-Allocation BST Difference Tracking: Morris Traversal in O(1) Space 🌲⚡

In Part 1, we eliminated the $\mathcal{O}(N^2)$ list concatenation bottleneck by streaming in-order values on-the-fly with a `prev` pointer.

Yet, both recursive DFS and iterative stack approaches consume $\mathcal{O}(H)$ auxiliary memory (where $H$ is the tree height).

*Can we find the minimum difference between any two BST nodes in strictly $\mathcal{O}(1)$ auxiliary space without any stack or recursion?*

**Morris Inorder Traversal** achieves zero auxiliary allocation by threading unused leaf pointers!

---

### 💡 The Core Mechanism: In-Order Predecessor Threading

Instead of using a call stack or heap stack to remember parent nodes:
1️⃣ For each node `curr` with a left child, find its **in-order predecessor** (the rightmost node of its left subtree).
2️⃣ **Create Thread (1st Visit)**: Set `predecessor.right = curr` and descend left: `curr = curr.left`.
3️⃣ **Compute & Restore (2nd Visit)**: When `predecessor.right is curr`, the left subtree is fully processed!
   • Dismantle the thread: `predecessor.right = None`
   • Calculate running difference: `min_diff = min(min_diff, curr.val - prev)`
   • Update `prev = curr.val`
   • Descend right: `curr = curr.right`

When Morris Traversal finishes, **all original pointers in the BST are completely restored**.

---

### 📊 Strategy Comparison

| Strategy | Time Complexity | Auxiliary Space | Permanent Mutation? |
| :--- | :--- | :--- | :--- |
| **Naive Concatenation (`+`)** | $\mathcal{O}(N^2)$ | $\mathcal{O}(N)$ list | ❌ No |
| **Streaming DFS with `prev`** | $\mathcal{O}(N)$ | $\mathcal{O}(H)$ call stack | ❌ No |
| **Morris Inorder Traversal** | $\mathcal{O}(N)$ | **$\mathcal{O}(1)$ (Zero Heap/Stack)** | ❌ **No (Self-Restoring)** |

---

### 🎯 Key Engineering Takeaways

• **Memory-Constrained Environments**: In embedded software, kernel programming, or large-scale in-memory databases, saving $\mathcal{O}(H)$ stack space avoids stack overflow and eliminates memory allocation pressure.
• **Concurrency Consideration**: Because pointer threads are temporarily modified during traversal, Morris Traversal requires read-locks in multithreaded systems.

Check out the clean Morris Traversal implementation in the attached image! 📸

How often do you prioritize $\mathcal{O}(1)$ memory optimization over algorithmic simplicity? Let's discuss in the comments! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #EmbeddedSystems #ComputerScience
