# Morris Traversal: True O(1) Space BST Recovery 🌲🧙‍♂️

In Part 1, we identified swapped BST nodes by tracking in-order inversions using standard recursive DFS.

*Standard recursion or explicit stacks cost O(H) auxiliary memory (up to O(N) for skewed trees). Can we traverse and recover a BST in TRUE O(1) space without recursion or stacks?*

Yes! Using **Morris In-Order Traversal** with temporary threaded pointers.

---

### 💡 The Core Idea: Threaded Binary Trees

Why do standard traversals require a stack?
To remember the path back to the parent node after exploring a left subtree.

**J. H. Morris’s Breakthrough (1979)**:
Instead of allocating memory on the call stack, use the **unused `right` pointer of the in-order predecessor** to create a temporary bridge back up to the current node!

---

### ⚡ Step-by-Step Morris Traversal

For each node `curr`:

1️⃣ **No Left Child**:
• Process `curr` directly and check for inversions.
• Move `curr = curr.right`.

2️⃣ **Has Left Child**:
• Find `pred` (the rightmost node in `curr.left` subtree).
• **If `pred.right is None`**:
  - Create the thread: `pred.right = curr`
  - Move left: `curr = curr.left`
• **If `pred.right is curr` (Bridge already crossed)**:
  - Break the thread: `pred.right = None` (Restoring tree structure!)
  - Process `curr` and check for inversions.
  - Move right: `curr = curr.right`

---

### 📊 Traversal Strategy Comparison

| Traversal Strategy | Time Complexity | Auxiliary Space | Modifies Structure? |
| :--- | :--- | :--- | :--- |
| **Recursive In-Order DFS** | O(N) | O(H) Call Stack | ❌ No |
| **Iterative Stack BFS/DFS**| O(N) | O(H) Explicit Stack | ❌ No |
| **Morris In-Order Traversal** | **O(N)** | **O(1) Strict Constant** | **Temporary (Restored to original)** |

---

### 🎯 Key Engineering Takeaways

• **Zero Stack Overhead**: Morris traversal eliminates recursion limits and memory allocations entirely, making it ideal for memory-constrained embedded environments.
• **Time-Space Tradeoff**: Each edge is traversed at most 3 times, preserving O(N) linear time while dropping space to O(1).
• **Reversibility**: Breaking threads during the second pass guarantees the tree's original topology remains 100% untouched.

Check out the Morris Traversal implementation in the attached image! 📸

Have you encountered threaded trees or Morris traversal in production systems? Let's discuss in the comments! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CleanCode #ComputerScience
