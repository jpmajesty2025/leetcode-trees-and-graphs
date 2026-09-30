# Leaf-Similar Trees: The Eager Evaluation Bottleneck & Lazy Generators 🌲⚡

When determining if two binary trees have the exact same left-to-right leaf sequence, what data structure do you use to compare them?

The most common implementation eagerly collects all leaf values into two arrays:
1. `get_leaves(root1, list1)`
2. `get_leaves(root2, list2)`
3. `return list1 == list2`

It works, but examine the architectural inefficiency:

---

### 🚨 The Eager Evaluation Flaw

Suppose Tree 1 has $1,000,000$ nodes with leaves `[99, ...]` and Tree 2 has $1,000,000$ nodes with leaves `[42, ...]`.
• An eager approach traverses **both entire trees** ($2,000,000$ nodes) and allocates memory for all leaves before comparing a single value.
• This wastes massive CPU cycles and memory when the very first leaf reveals that the trees are not similar!

---

### 💡 The Solution: Lazy Streaming with Python Generators

Instead of collecting lists upfront, we can stream leaves **one by one on demand** using `yield from` and compare them with `itertools.zip_longest`:

1️⃣ **Generator Traversal**:
• When a leaf node is encountered, `yield node.val`.
• Execution pauses until the consumer requests the next leaf.

2️⃣ **Instant Short-Circuiting**:
• `zip_longest(get_leaves(root1), get_leaves(root2))` pulls one leaf from each tree in lockstep.
• On the very first mismatch, traversal terminates immediately!
• Best-case runtime drops from $\mathcal{O}(N_1 + N_2)$ down to $\mathcal{O}(H_1 + H_2)$!

---

### ⚖️ Performance Comparison

| Metric | Eager List Collection | Lazy Generator Stream |
| :--- | :--- | :--- |
| **Best-Case Time** | $\mathcal{O}(N_1 + N_2)$ (Always full traversal) | **$\mathcal{O}(H_1 + H_2)$ (Instant early exit)** |
| **Worst-Case Time** | $\mathcal{O}(N_1 + N_2)$ | $\mathcal{O}(N_1 + N_2)$ |
| **Auxiliary Memory** | $\mathcal{O}(L_1 + L_2)$ list allocations | **$\mathcal{O}(H_1 + H_2)$ call stack only** |
| **Evaluation Strategy** | Eager (Batch) | **Lazy (Streaming)** |

---

In Part 2 tomorrow, we’ll explore how to achieve **100% stack safety using Iterative Stack Leaf Traversals!**

Do you use generators for lazy tree comparisons in your systems? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #SystemDesign #ComputerScience
