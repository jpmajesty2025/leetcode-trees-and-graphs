# Merging Two BSTs: The Power of Concurrent Stack Traversals (Part 1 of 2) 🌲⚡

When combining data from multiple sorted structures—like merging two Binary Search Trees into a single sorted list—the in-order traversal property is our greatest asset.

Tempted to dump both trees into arrays and sort them? Don't! We can streamingly merge both BSTs in a single pass with minimal memory!

---

### 💡 The Problem & Mental Model

Given the roots of two BSTs (`root1` and `root2`), return a list containing all integers from both trees in sorted ascending order.

A fundamental property of BSTs is that an **in-order traversal (Left $\to$ Root $\to$ Right)** produces elements in strictly non-decreasing order.

Instead of extracting all elements first and then sorting, we can run two in-order traversals **concurrently**, comparing the next smallest element from each tree just like the merge step in Merge Sort!

---

### ⚙️ How Concurrent 2-Stack In-Order Merging Works

1. **Dual Stacks**: Maintain `stack1` and `stack2` alongside active pointers `curr1` and `curr2`.
2. **Left-Subtree Descent**:
   - Push all left descendants of `curr1` onto `stack1`.
   - Push all left descendants of `curr2` onto `stack2`.
3. **Top-of-Stack Comparison**:
   - Peek at the tops of both stacks. The smaller value is the next global minimum across both trees.
   - If `stack1` holds the smaller value (or if `stack2` is empty), pop from `stack1`, append its value to the result, and advance `curr1 = node.right`.
   - Otherwise, pop from `stack2`, append its value, and advance `curr2 = node.right`.
4. **Repeat**: Continue until both stacks and pointers are exhausted.

---

### 📊 Complexity Profile

- **Time Complexity: O(N + M)** — Every node in both trees is pushed and popped exactly once.
- **Auxiliary Space: O(H₁ + H₂)** — The stacks store only the current root-to-leaf paths, requiring zero intermediate arrays!

---

### 🧠 Key Engineering Takeaways

1. **True Streaming**: We produce the globally sorted sequence on the fly without materializing intermediate lists.
2. **Optimal Memory**: Auxiliary space drops from O(N + M) down to logarithmic tree heights O(H₁ + H₂).

👉 **In Part 2**, we'll compare **Two-Pass Array Extraction vs. Streaming Stacks** and examine real-world applications in database index merging!

How do you approach merging sorted tree structures in production?

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #BinarySearchTree #BST #MergeSort #PerformanceOptimization
