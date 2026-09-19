# The Power of Pruning: Optimizing Range Queries in Binary Search Trees 🌲🎯

When querying a Binary Search Tree (BST) for values within a specific range $[low, high]$, a standard tree traversal visits every single node in $\mathcal{O}(N)$ time. 

Can we do significantly better?

By leveraging the **BST ordering invariant**, we can prune entire subtrees that fall outside our range boundaries, slashing the query runtime to $\mathcal{O}(K + H)$ (where $K$ is the number of matching nodes and $H$ is the tree height).

Let's dissect **LeetCode 938: Range Sum of BST** and compare **Recursive DFS** with **Iterative Stack DFS**.

---

### 💡 The Core Problem & Intuition

Given the root of a BST and an inclusive range $[low, high]$, return the sum of all node values within $[low, high]$.

Because a BST guarantees that for every node:
$$\text{left\_subtree} < \text{node.val} < \text{right\_subtree}$$

We never need to blindly explore both children:
1. **Left Branch Pruning**: Only visit `node.left` if `node.val > low`. If `node.val <= low`, everything in the left subtree is strictly $< low$—completely safe to ignore!
2. **Right Branch Pruning**: Only visit `node.right` if `node.val < high`. If `node.val >= high`, everything in the right subtree is strictly $> high$—pruned immediately!
3. **In-Range Accumulation**: Only add `node.val` to our total when $low \le \text{node.val} \le high$.

---

### 1️⃣ Solution 1: Recursive DFS (Declarative & Concise)

Recursive DFS expresses the pruning logic naturally through divide-and-conquer:
- Recursively sum the matching nodes from the qualified left and right subtrees.
- Takes $\mathcal{O}(H)$ call stack space ($\mathcal{O}(\log N)$ on balanced BSTs).

*(See attached ray.so image for the clean Python implementation! 📸)*

---

### 2️⃣ Solution 2: Iterative DFS with Explicit Stack (Production & Stack-Safe)

In environments where trees might be deep or skewed ($H > 1,000$ levels), recursion risks hitting Python's call frame limit.

We can simulate the depth traversal using an explicit stack on the heap:
- Push the root node onto a stack.
- Pop nodes one by one, conditionally pushing only the non-pruned children (`node.left` if `low < node.val`, `node.right` if `node.val < high`).
- Guarantees $100\%$ immunity against `RecursionError`.

*(See attached ray.so image for the iterative Python implementation! 📸)*

---

### ⚖️ Architectural Trade-off Summary

| Metric | Full Tree Traversal | Recursive BST Pruning | Iterative BST Pruning |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | $\mathcal{O}(N)$ | **$\mathcal{O}(K + H)$** | **$\mathcal{O}(K + H)$** |
| **Auxiliary Space (Balanced BST)** | $\mathcal{O}(\log N)$ | $\mathcal{O}(\log N)$ call stack | $\mathcal{O}(\log N)$ heap stack |
| **Auxiliary Space (Skewed BST)** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ call stack | $\mathcal{O}(N)$ heap stack |
| **Search Space** | 100% of tree | Only nodes near/within range | Only nodes near/within range |
| **Stack Overflow Risk** | Possible if recursive | Possible if $H > 1,000$ | **None** |

---

### 🧪 Property-Based Verification with Hypothesis
Both implementations were validated using **Hypothesis** with a custom BST generator tested against a brute-force $\mathcal{O}(N)$ oracle across randomized tree topologies, negative numbers, and extreme range intervals with 100% agreement.

---

When designing range queries or indexing in database engines and search trees, branch pruning is one of the most fundamental optimizations. 

How often do you rely on early search-space pruning in your backend systems? Let's discuss below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #BinarySearchTree #SystemDesign
