# From O(N²) to O(N): Generalizing 1D Prefix Sums to Binary Trees 🌲⚡

Here, as before, we are given the root of a binary tree and an integer `targetSum`.

However, unlike Path Sum I and II (which require paths to start strictly at the root and terminate at leaves), Path Sum III allows paths to:
• Start at ANY ancestor node.
• End at ANY descendant node.
• Must travel strictly downwards (parent ➡️ child).

```
          10
         /  \
        5   -3
       / \    \
      3   2   11
     / \   \
    3  -2   1

Target Sum = 8
Valid Paths:
👉 [5, 3]
👉 [5, 2, 1]
👉 [-3, 11]
Total Count = 3
```

How do we optimize this from a quadratic O(N²) double-recursion into a single-pass O(N) linear algorithm?

---

### 🚨 The O(N²) Double-DFS Bottleneck

The intuitive baseline approach uses two nested recursions:
1. An outer DFS that visits every node in the tree.
2. For each visited node, an inner DFS that treats that node as a fresh root and counts all downward paths summing to the remaining target.

While simple, this re-computes sub-path sums repeatedly across overlapping branches:
• **Time Complexity**: O(N log N) on balanced trees, but degrades to **O(N²)** on skewed/degenerate trees.

---

### 💡 The 1D Subarray Prefix Sum Analogy

Recall the classic "Subarray Sum Equals K" problem on 1D arrays:
• Any subarray sum from index `i` to `j` is:
  `SubarraySum(i..j) = PrefixSum[j] - PrefixSum[i - 1] = Target`
• Rearranging gives the target lookup equation:
  `PrefixSum[i - 1] = CurrentRunningSum - Target`

A root-to-leaf path in a binary tree is simply a **1D sequence of node values**!

By maintaining a hash map of prefix sum frequencies during our DFS traversal, at any node with `CurrentRunningSum`, we can query the count of valid ancestor starting nodes in **O(1) instant lookup time**:
`MatchingPathsEndingHere = PrefixCounts[CurrentRunningSum - TargetSum]`

---

### ⚖️ Algorithm Complexity

| Metric | Double DFS (Brute Force) | Prefix Sum Hash Map DFS |
| :--- | :--- | :--- |
| **Time Complexity** | **O(N²)** worst-case | **O(N)** strictly linear |
| **Pass Count** | Multi-pass re-traversal | **Single Pass** |
| **Auxiliary Memory** | **O(H)** Call Stack | **O(H)** Call Stack + Hash Map |

---

In Part 2 tomorrow, we’ll explore **Why Tree Prefix Hash Maps Require Backtracking to Prevent Cross-Branch Memory Pollution!**

Check out the full implementation in the attached code snippet! 📸

Have you applied 1D array prefix sums to hierarchical tree structures before? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #TreeTraversals #CleanCode #Recursion #Performance
