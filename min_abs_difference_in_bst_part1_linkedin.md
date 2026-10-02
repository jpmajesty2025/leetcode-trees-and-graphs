# Minimum Absolute Difference in BST: The Full-Array Anti-Pattern & In-Order Streaming 🌲⚡

In a Binary Search Tree (BST), values are naturally sorted in-order:
$\text{Left Subtree} \le \text{Node} \le \text{Right Subtree}$

Here we must find the minimum absolute difference between any two nodes. The good news: the minimum difference is **guaranteed to occur between adjacent elements in an in-order sequence**!

You might be tempted to do the following:
1. In-order traverse the tree and append every value to `values = []`.
2. Loop through `values` and compute `min(values[i] - values[i - 1])`.

However, this is an anti-pattern. Let's see why!

---

### 🚨 The Memory Overhead of Eager Array Collection

On a BST with $N = 100,000$ nodes:
• Building a full list allocates contiguous memory for all $100,000$ integers.
• If you only need to compare **adjacent consecutive pairs**, buffering the entire dataset in RAM is pure waste!

---

### 💡 The Fix: In-Order Streaming with a `prev` Pointer

Instead of collecting an array, maintain a single scalar variable `prev: Optional[int]`:

1️⃣ **Left Subtree First**: Recurse down `node.left`.
2️⃣ **Compare with `prev`**:
• If `prev is not None`, update: `min_diff = min(min_diff, node.val - prev)`.
• Advance the stream pointer: `prev = node.val`.
3️⃣ **Right Subtree**: Recurse down `node.right`.

By computing differences on the fly:
• **Zero intermediate array allocations**.
• Memory drops from $\mathcal{O}(N)$ down to $\mathbf{O(H)}$ call-stack space.

---

### ⚖️ Performance Comparison

| Metric | Full Array Collection | In-Order Streaming (`prev` pointer) |
| :--- | :--- | :--- |
| **Time Complexity** | $\mathcal{O}(N)$ | $\mathbf{O(N)}$ |
| **Array Allocations** | $\mathcal{O}(N)$ list allocation | **Zero array allocations** |
| **Auxiliary Memory** | $\mathcal{O}(N + H)$ | $\mathbf{O(H)}$ **call stack only** |
| **Data Processing** | Batch (Post-processed) | **Streaming (On-the-fly)** |

---

Check out the clean streaming implementation in the attached snippet! 📸

In Part 2 tomorrow, we’ll explore how to break the $\mathcal{O}(H)$ stack barrier and achieve **strictly $\mathcal{O}(1)$ extra memory using Morris Traversal!**

Do you stream or buffer data when traversing sequential structures? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #SystemDesign #ComputerScience
