# Breaking the O(H) Memory Barrier: Morris In-Order Traversal in O(1) Space 🌲🧙‍♂️

In Part 1, we used a `prev` pointer to stream BST nodes, reducing memory from $\mathcal{O}(N)$ to the $\mathcal{O}(H)$ call stack.

*Can we traverse a BST in sorted in-order sequence and calculate minimum differences with ZERO recursion frames and ZERO heap-allocated stacks?*

Yes! Using **Morris In-Order Traversal** ($\mathcal{O}(1)$ auxiliary space).

---

### 💡 The Core Mechanism: Threaded Binary Trees

How can we backtrack to a parent node without storing an ancestor stack?
By temporarily modifying null `right` child pointers to point back to the current node!

1️⃣ **Find In-Order Predecessor**:
• If `curr.left` exists, find its rightmost descendant (`pred = curr.left`).

2️⃣ **Thread Creation (Going Down)**:
• If `pred.right is None`:
  - Set `pred.right = curr` (create temporary thread back to `curr`).
  - Move left: `curr = curr.left`.

3️⃣ **Thread Destruction & Node Processing (Backtracking)**:
• If `pred.right is curr`:
  - Reset `pred.right = None` (restore tree structure).
  - Process `curr.val`: update `min_diff` using `prev`.
  - Update `prev = curr.val`.
  - Move right: `curr = curr.right`.

4️⃣ **Left is None**:
• Process `curr.val` directly and move right.

---

### 📊 Comprehensive Architectural Comparison

| Traversal Strategy | Time Complexity | Extra Memory | Modifies Tree Structure? |
| :--- | :--- | :--- | :--- |
| **Array Collection** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ list | No |
| **Recursive Streaming** | $\mathcal{O}(N)$ | $\mathcal{O}(H)$ call stack | No |
| **Iterative Stack** | $\mathcal{O}(N)$ | $\mathcal{O}(H)$ heap memory | No |
| **Morris Traversal** | $\mathbf{O(N)}$ | $\mathbf{O(1)}$ **Constant Space** | Temporarily (restored on exit) |

---

### 🎯 Key Engineering Takeaways

• **Tree Restoration Invariant**: Morris traversal temporarily creates threads but guarantees $100\%$ restoration of original tree pointers before returning.
• **Constant Memory Bound**: Essential in resource-constrained environments (microcontrollers, kernel drivers) where call-stack space is strictly budgeted.

Check out the Morris Traversal implementation in the attached image! 📸

Have you ever used threaded binary trees or Morris traversal in production? Let's discuss in the comments! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CleanCode #ComputerScience
