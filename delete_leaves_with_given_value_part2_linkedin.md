# Iterative Tree Mutation: Pruning Skewed Trees Safely 🌲🛡️

In Part 1, we established that Post-Order DFS is the only traversal order that guarantees single-pass cascading leaf deletions in O(H) call-stack space.

*What happens in production when a binary tree is degenerate (skewed with depth 50,000) and recursive DFS triggers a call-stack overflow?*

Let's dissect how to execute **Iterative Post-Order Tree Mutation** using an explicit heap stack.

---

### 🚨 The Challenge with Iterative Tree Pruning

Iterative post-order traversal is notoriously tricky because a parent node must be processed only *after* its right subtree has been fully traversed.

Furthermore, pruning requires modifying the **parent's child pointer** (`parent.left = None` or `parent.right = None`). If the root itself gets deleted, we also need a safe way to return the updated root.

---

### 💡 The Dummy Parent + Last-Visited Stack Pattern

We can solve both challenges using two classical engineering techniques:

1. **The Sentinel Dummy Node**:
   Create a dummy node (`dummy.left = root`). This ensures that the original `root` node always has a concrete parent, making root deletion identical to any internal node deletion.

2. **Explicit Stack with `last_visited` Pointer**:
   • Push left children down the branch to the bottom.
   • Peek at the top node (`peek_node = stack[-1]`).
   • If `peek_node.right` exists and was not just visited (`last_visited != peek_node.right`), traverse down the right branch.
   • Otherwise, both children are processed! Inspect `peek_node.left` and `peek_node.right`. If either is a leaf matching `target`, prune it by setting `peek_node.left = None` or `peek_node.right = None`.
   • Pop the node and record it as `last_visited`.

---

### 📊 Strategy Comparison

| Dimension | Recursive Post-Order DFS | Iterative Stack Post-Order |
| :--- | :--- | :--- |
| **Time Complexity** | **O(N)** | **O(N)** |
| **Auxiliary Memory** | **O(H) Call Stack** | **O(H) Heap Stack** |
| **Stack Overflow Risk** | **High** (Python default limit: 1,000) | **Zero** (Heap-allocated) |
| **Implementation Complexity** | Minimal (3 lines) | Moderate (Explicit state machine) |

---

### 🎯 Key Engineering Takeaways

• **Sentinel Nodes for Tree Mutation**: Dummy roots eliminate edge cases where the root itself must be replaced or severed.
• **Post-Order State Machine**: Maintaining a `last_visited` pointer enables clean two-way traversal without modifying node schemas with visited flags.

Check out the complete iterative implementation in the attached code image! 📸

Do you default to recursive tree traversals in production or implement iterative stack fallbacks? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CleanCode #Performance
