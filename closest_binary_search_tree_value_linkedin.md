# The Hidden Tie-Breaking Trap in BST Search Queries 🌲🎯

**The Problem**:
Given the root of a binary search tree and a target value, return the value in the BST 
that is closest to the target. If there are multiple answers, return the smallest.

Note that binary search finds the answer in $\mathcal{O}(H)$ time.

However, there is subtle edge case that might silently breaks your solutions: **Equidistant Tie-Breaking**. Let's see why simple distance comparison falls short.

---

### ⚠️ The Bug: Strict Inequality Misses Ties

Problem constraint: *"If there are multiple answers, return the smallest."*

A common initial attempt:
```python
# ❌ BUGGY: Misses equal-distance updates
if abs(node.val - target) < abs(closest - target):
    closest = node.val
```

Why does this fail?
Consider `[2, 1, 3]` with `target = 1.5`:
- At root `2`: distance is $|2 - 1.5| = 0.5$. `closest` starts at `2`.
- Since $1.5 < 2$, we move left to node `1`.
- At node `1`: distance is $|1 - 1.5| = 0.5$.
- Because $0.5 < 0.5$ is `False`, `closest` **never updates to 1**, incorrectly returning `2`!

---

### 💡 The Fix: Tie-Aware Comparison

Update `closest` if the distance is strictly smaller, OR if distances are equal and the current value is smaller:

```python
curr_diff = abs(curr.val - target)
closest_diff = abs(closest - target)

if curr_diff < closest_diff or (curr_diff == closest_diff and curr.val < closest):
    closest = curr.val
```

---

### 🚀 Two Implementations

1️⃣ **Iterative Search ($\mathcal{O}(1)$ Auxiliary Space & Stack-Safe)**
- Follows the target branch with a single pointer.
- Includes early exit on exact match (`curr.val == target`).
- **Complexity:** $\mathcal{O}(H)$ time, **$\mathcal{O}(1)$** auxiliary space.

2️⃣ **Recursive Search (Declarative Divide-and-Conquer)**
- Passes running closest value down the call stack.
- **Complexity:** $\mathcal{O}(H)$ time, $\mathcal{O}(H)$ call-stack space.

---

### ⚖️ Trade-off Summary

| Metric | Iterative BST Search | Recursive BST Search |
| :--- | :--- | :--- |
| **Time** | $\mathcal{O}(H)$ ($\mathcal{O}(\log N)$ balanced) | $\mathcal{O}(H)$ ($\mathcal{O}(\log N)$ balanced) |
| **Auxiliary Memory** | **$\mathcal{O}(1)$** (constant) | $\mathcal{O}(H)$ call stack |
| **Branching** | Single path only | Single path only |
| **Stack Safety** | **100% Stack-Safe** | Call stack risk if deep |

---

How do you handle secondary sorting keys and tie-breaking in search indexes? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #BinarySearchTree #SystemDesign
