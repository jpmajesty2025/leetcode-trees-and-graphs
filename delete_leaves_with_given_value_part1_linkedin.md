# Cascading Tree Pruning: Why Traversal Order Dictates Correctness 🌲✂️

Given: a binary tree root and an integer `target`.

The task:
1. Delete all leaf nodes whose value equals `target`.
2. **The Cascading Rule**: If deleting a leaf causes its parent to become a leaf with value `target`, that parent must also be deleted immediately! This pruning must cascade upward until no target leaves remain.

```
       1 (target = 2)                1
      / \                           / \
     2   3           ===>        None  3
    /   / \                             \
   2   2   4                             4
```

Why does the choice of tree traversal order make or break this problem?

---

### 🚨 Why Pre-Order and In-Order Traversal Fail

• **Pre-Order (Top-Down)**: Inspects the parent node before visiting its children. If a parent node currently has two children that are target leaves, pre-order sees a non-leaf node, skips deletion, and recurses downward. After deleting the children, the parent becomes a target leaf that never gets re-evaluated, leaving an invalid tree state!

• **In-Order**: Processes the left child, evaluates the parent, and only then visits the right child. If the right child gets deleted later, the parent's new leaf status is missed.

---

### 💡 The Post-Order Bottom-Up Invariant

To prune cascading leaves correctly in a single pass, we must guarantee that **all descendants are fully resolved and pruned before a parent node evaluates itself**.

This is the exact mathematical definition of **Post-Order Traversal (Left ➡️ Right ➡️ Root)**:

1. Prune the left subtree: reassign the left child to the pruned result.
2. Prune the right subtree: reassign the right child to the pruned result.
3. **Evaluate the Current Node**: Now that both children have been pruned, check if the current node is a leaf (`not left and not right`) and equals `target`. If so, return `None` to sever the link from its parent!

---

### ⚖️ Algorithm Complexity

| Metric | Post-Order Recursive DFS |
| :--- | :--- |
| **Time Complexity** | **O(N)** (Every node visited exactly once) |
| **Call Stack Memory** | **O(H)** (O(log N) for balanced trees, O(N) for skewed trees) |
| **Pass Count** | **Single Pass** (Zero multi-pass recalculations) |

---

In Part 2 tomorrow, we’ll explore **Iterative Post-Order Pruning with an Explicit Stack & Dummy Parent for 100% Call-Stack Safety!**

Check out the full implementation in the attached code snippet! 📸

How do you reason about bottom-up state propagation when mutating hierarchical data structures? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #TreeTraversals #CleanCode #Recursion #Performance
