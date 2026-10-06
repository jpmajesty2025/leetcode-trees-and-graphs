# Average of Levels: Streaming BFS & Clean Tier Reductions (Part 1 of 2) 🌲📈

Calculating layer-by-layer metrics—like the average node value at each tree depth (LeetCode 637)—is a standard task in tree analytics. While Breadth-First Search (BFS) is the go-to tool, keeping execution strictly linear requires intentional container choices.

Let's break down the optimal queue-based architecture!

---

### 💡 The Problem & Mental Model

Given the root of a binary tree, return the average value of the nodes on each level as a list of floating-point numbers.

Because the output is grouped strictly by horizontal depth, BFS is the natural match:
- Start at the root (level 0).
- For each level, aggregate all node values, divide by the number of nodes on that tier, and advance to the next level.

---

### ⚙️ How Streaming BFS Works

1. **Queue Setup**: Initialize a `collections.deque` with the root node.
2. **Level Snapshot**: At the start of each while loop iteration, capture `level_size = len(queue)`. Because all nodes currently in the queue belong to the active tier, this snapshot establishes the exact denominator.
3. **Inner Loop**: Iterate `level_size` times using `popleft()`. Add each node's value to `current_sum` and enqueue its non-null left and right children.
4. **Row Average**: Append `current_sum / level_size` to the result list.

---

### ⚠️ The O(N²) Trap: List vs. Deque

Avoid using a standard Python list with `pop(0)`. 

Calling `pop(0)` on a dynamic array forces a left-shift of all remaining elements in memory—costing O(K) per pop. In a balanced tree where the bottom tier contains ~50% of all nodes, these repeated pointer shifts turn an O(N) traversal into an O(N²) bottleneck. Always use `collections.deque` for O(1) removals.

---

### 📊 Complexity Profile

- **Time: O(N)** — Every node is visited, summed, and enqueued exactly once.
- **Space: O(W)** — Auxiliary queue memory is proportional to maximum tree width (up to N/2 in a balanced tree).

---

👉 **In Part 2**, we'll explore **DFS with parallel accumulators** and how DFS slashes memory usage on wide trees!

Do you default to BFS for level-based tree reductions?

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #TreeTraversal #BFS #PerformanceOptimization
