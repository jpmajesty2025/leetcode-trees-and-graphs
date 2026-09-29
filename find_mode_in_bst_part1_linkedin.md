# Finding Modes in a BST: Why Hash Maps Are an Anti-Pattern 🌲📊

When asked to find the mode(s) (most frequent elements) in a Binary Search Tree with duplicates (LeetCode 501), what is the first instinct?

Many engineers traverse the tree and dump node values into a hash map:
`counts = Counter()`

Why is this an architectural anti-pattern for a BST?

---

### 🚨 Why Hash Maps Waste the BST Invariant

1️⃣ **Ignores Sorted Ordering**: A general binary tree requires a hash map because duplicates can appear anywhere. But in a BST, **an in-order traversal yields elements in sorted, non-decreasing order**!
2️⃣ **Unnecessary $\mathcal{O}(N)$ Memory**: Allocating a dictionary with up to $N$ entries creates heap allocations and hash table overhead when duplicate values are already grouped contiguously.

---

### 💡 The Clean Insight: Single-Pass Streak Tracking

Because in-order traversal produces sorted sequences like `[1, 2, 2, 3, 3, 3, 4]`, all duplicate instances appear back-to-back.

We only need a single `prev` pointer to track the current frequency streak:
• **Streak Update**: `count = (count + 1) if (prev == curr) else 1`
• **Mode Maintenance**:
  - If `count > max_count`: reset `modes = [curr.val]` and update `max_count = count`.
  - If `count == max_count`: append `modes.append(curr.val)`.

• **Single Pass**: Identifies all tied modes in one traversal without prior knowledge of `max_count`.
• **Iterative Stack Alternative**: Employs an explicit heap stack for $100\%$ stack safety on skewed trees.

---

### ⚖️ Strategy Comparison

| Metric | Hash Map Counter | Streaming In-Order DFS | Iterative Stack DFS |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| **Auxiliary Memory** | $\mathcal{O}(N)$ (Dictionary) | $\mathcal{O}(H)$ (Call stack) | $\mathcal{O}(H)$ (Heap stack) |
| **Passes Over Tree** | 2 passes | **1 single pass** | **1 single pass** |
| **Stack Safety** | Risky on deep trees | Risky if $H > 1,000$ | ✅ **100% Stack-Safe** |

---

Check out the clean implementations in the attached snippet! 📸

In Part 2 tomorrow, we’ll explore how **Morris Traversal** finds BST modes in **$\mathcal{O}(1)$ auxiliary space without any stack or recursion!**

Do you leverage BST ordering properties or reach for a `Counter()` first? Let's discuss below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #ComputerScience
