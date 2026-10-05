# Recovering a Swapped BST: The In-Order Inversion Theorem 🌲🔍

I tell you that two nodes in a binary search tree have been accidentally swapped and ask you to restore the tree in-place without changing its structure. How do you identify which two nodes were swapped during a single pass?

---

### 💡 The BST In-Order Property

An in-order traversal (Left -> Node -> Right) of any valid BST yields a **strictly monotonically increasing array**:
`[1, 2, 3, 4, 5]`

When exactly two nodes are swapped, this sorted order breaks, creating **inversion anomalies** where `prev.val > curr.val`.

---

### 🔍 The Two Inversion Scenarios

When scanning the in-order sequence, swapped nodes manifest in one of two distinct patterns:

1️⃣ **Case A: Adjacent Nodes Swapped**
• Original: `[1, 2, 3, 4, 5]`
• Swapped 2 & 3: `[1, 3, 2, 4, 5]`
• Inversion: Exactly **ONE** drop (`3 > 2`).
• Resolution: `first = prev` (3) and `second = curr` (2).

2️⃣ **Case B: Non-Adjacent Nodes Swapped**
• Original: `[1, 2, 3, 4, 5, 6]`
• Swapped 2 & 5: `[1, 5, 3, 4, 2, 6]`
• Inversions: Exactly **TWO** drops:
  - Drop 1 (`5 > 3`): `first = prev` (5), `second = curr` (3).
  - Drop 2 (`4 > 2`): `second = curr` (2) — overwriting our temporary candidate!
• Resolution: `first` (5) and `second` (2).

---

### ⚡ The Unified Detection Rule

We can handle both cases with a single, elegant conditional check during in-order traversal:

```python
if prev and prev.val > curr.val:
    if first is None:
        first = prev  # First drop: take the larger element
    second = curr     # Always update second to the smaller element
```

Once traversal completes, simply swap values:
`first.val, second.val = second.val, first.val`

---

### ⚖️ Algorithm Complexity

| Metric | In-Order DFS Traversal |
| :--- | :--- |
| **Time Complexity** | **O(N)** (Single pass through tree) |
| **Call Stack Memory** | **O(H)** (where H is tree height, up to O(N)) |
| **Node Value Swaps** | **1 swap** at termination |

---

Check out the clean in-order traversal implementation in the attached snippet! 📸

In Part 2 tomorrow, we’ll explore how **Morris Traversal achieves TRUE O(1) auxiliary space using Threaded Binary Trees!**

How do you approach anomaly detection in sorted streams and search trees? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #ComputerScience #Trees
