# The Classic Trap in BST Validation: Why Local Checks Fail 🌲🔍

When validating a Binary Search Tree (BST), what is your first instinct?

A common pitfall is checking only immediate parent-child relationships:
```python
# ❌ INCORRECT: Local check only
if node.left and node.left.val >= node.val: return False
if node.right and node.right.val <= node.val: return False
```

Why does this fail? Consider `[5, 4, 6, null, null, 3, 7]`:
- Locally, `3 < 6` and `7 > 6` look fine.
- Globally, `3` sits in the **right subtree of `5`**, violating the BST invariant ($3 < 5$)!

In a valid BST, **all left descendants** must be $< root$, and **all right descendants** must be $> root$.

Here is how dynamic interval propagation solves the problem in $\mathcal{O}(N)$ time.

---

### 💡 The Core Insight: Dynamic Open Intervals $(small, large)$

Pass down open intervals $(small, large)$ that tighten as we descend:
1. **Root**: Initialized to $(-\infty, +\infty)$.
2. **Left Branch**: Values must be $< parent \implies (small, node.val)$.
3. **Right Branch**: Values must be $> parent \implies (node.val, large)$.
4. **Validation**: If $node.val \le small$ or $node.val \ge large$, return `False`.

---

### 🚀 Two Complementary Implementations

1️⃣ **Recursive DFS (Declarative & Expressive)**
- Evaluates subtrees with boolean short-circuiting: `dfs(left) and dfs(right)`.
- Instantly terminates on the first violation.
- **Complexity:** $\mathcal{O}(N)$ time, $\mathcal{O}(H)$ call-stack space.

2️⃣ **Iterative DFS with Stack (Stack-Safe for Production)**
- Uses a heap-allocated stack of `(node, small, large)` tuples.
- Eliminates `RecursionError` on deep or skewed trees ($H > 1,000$).
- **Complexity:** $\mathcal{O}(N)$ time, $\mathcal{O}(H)$ auxiliary space.

---

### ⚖️ Trade-off Summary

| Metric | Local Checks | Recursive DFS | Iterative Stack DFS |
| :--- | :--- | :--- | :--- |
| **Correctness** | ❌ Fails ancestor traps | ✅ **100% Correct** | ✅ **100% Correct** |
| **Time** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| **Memory** | $\mathcal{O}(H)$ | $\mathcal{O}(H)$ call stack | $\mathcal{O}(H)$ heap stack |
| **Stack Safety** | Risky on deep trees | Possible if $H > 1,000$ | **None (Stack-Safe)** |

---

Have you ever caught a bug where local checks passed but global invariants failed? Let's discuss below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #BinarySearchTree #SystemDesign
