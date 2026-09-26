# Mastering Binary Trees: Level-by-Level Zigzag Traversal with BFS  (Part 1 of 2) 🌲⚡

When traversing a tree where data flows in alternating directions across horizontal rows (left-to-right on tier 0, right-to-left on tier 1, and so on), Breadth-First Search (BFS) is an intuitive starting point. Let's dive in!

---

### 💡 The Problem & Mental Model

Given the root of a binary tree, return its node values in zigzag level order:
- **Even depths (0, 2, 4...)**: Left $\to$ Right
- **Odd depths (1, 3, 5...)**: Right $\to$ Left

Because the problem defines output by horizontal tiers, **Breadth-First Search (BFS)** provides the cleanest direct mapping between the data structure and the algorithm.

---

### ⚙️ How the BFS Architecture Works

1. **Queue-Based Level Batching**: Using a standard `deque`, capture the size of the current tier (`len(queue)`).
2. **Direction Flag**: Maintain a boolean `left_to_right = True` that flips at the end of every processed tier.
3. **In-Place Row Inversion**: Collect nodes left-to-right as they are dequeued, and conditionally reverse the tier list if `not left_to_right` before appending to the final result.

---

### 📊 Complexity & Performance Profile

- **Time Complexity: $\mathcal{O}(N)$**
  Every node is visited and queued exactly once. Reversing a row of $k$ nodes takes $\mathcal{O}(k)$ operations; across all rows, $\sum k = N$.
- **Auxiliary Space: $\mathcal{O}(W)$**
  The queue only holds at most the maximum width ($W$) of the tree at any given moment. In a balanced binary tree, the bottom tier holds $\approx N/2$ nodes.

---

### 🧠 Key Engineering Takeaways

1. **Natural State Scoping**: Level-order BFS finishes each tier completely before advancing, making row-level transformations (reversing, summing, filtering) trivial to scope and isolate.
2. **Predictable Memory Footprint**: In tall, skewed trees (chains), the queue size is strictly $\mathcal{O}(1)$, consuming virtually no heap space.
3. **Clean Decoupling**: Child discovery remains strictly left-to-right, keeping queue ingestion simple while deferring directional logic to the extracted level batch.

---

👉 **In Part 2**, we’ll explore how to solve this exact problem **Depth-First (DFS)** using depth indexing and double-ended queues — and why DFS might be your best bet for memory optimization on wide, balanced trees!

Do you prefer handling alternating direction via row reversal or directional deque insertions?

#LearningInPublic #Python #DataStructures #Algorithms #LeetCode #SoftwareEngineering #CleanCode #BFS #TreeTraversal
