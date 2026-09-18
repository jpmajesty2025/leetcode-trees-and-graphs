# Mastering Binary Trees (Part 1): Maximum Ancestor Difference via Top-Down DFS 🌲

Given a binary tree, how do you find the maximum value $V = |a.\text{val} - b.\text{val}|$ where node $a$ is an ancestor of node $b$?

There is always the $\mathcal{O}(N^2)$ brute-force problem: for every node, compare it against every single ancestor above it. You'd be right to suspect this as sub-optimal. You might instead try complex bottom-up aggregation returning sub-trees of values.

However, there's a much more elegant mental model.

---

### 💡 The Core "Aha!" Insight

Instead of comparing pairs, look at the root-to-leaf paths:

> **Along any root-to-leaf path, the maximum difference between any ancestor-descendant pair is simply:**
> $$\max(\text{path}) - \min(\text{path})$$

Why? Because both the minimum and maximum values lie along the same simple path from the root down to a leaf, **one is guaranteed to be an ancestor of the other!**

This flips the problem from quadratic pair comparisons to a simple top-down state propagation: track `(cur_min, cur_max)` as you traverse downwards. Much cleaner and easier to reason about!

---

### 1️⃣ Approach 1: Recursive DFS (Clean & Expressive)
- Pass `(cur_min, cur_max)` down the call stack.
- At each node, update the running extremes with `min(cur_min, node.val)` and `max(cur_max, node.val)`.
- At null children (past a leaf), return `cur_max - cur_min`.
- Bubble up `max(left_diff, right_diff)`.

**Complexity:** $\mathcal{O}(N)$ Time | $\mathcal{O}(H)$ Call Stack Space ($H = \log N$ balanced, $H = N$ skewed).

---

### 2️⃣ Approach 2: Explicit Stack Iterative DFS (Recursion-Proof) 🛡️
As we've seen in prior posts, Python and languages without tail-call optimization have call-stack limits (~1,000 frames). A sufficiently large, heavily skewed tree will crash the program with a `RecursionError`.

**The fix:** Move state to the heap using an explicit LIFO stack holding `(node, cur_min, cur_max)`.
- Pop node, update path bounds.
- When reaching a true leaf (`not left and not right`), record `max_diff = max(max_diff, cur_max - cur_min)`.
- Push children with updated bounds.

**Complexity:** $\mathcal{O}(N)$ Time | $\mathcal{O}(H)$ Heap Space.

---

👉 **In Part 2**, we'll explore how to track path state horizontally with **Level-Order BFS**, and compare the $\mathcal{O}(H)$ vs $\mathcal{O}(W)$ architectural space trade-offs!

What's your default when traversing trees: recursive DFS or explicit heap stacks?

#LearningInPublic #Python #Algorithms #DataStructures #LeetCode #SoftwareEngineering #CodingInterview #CleanCode #Recursion
