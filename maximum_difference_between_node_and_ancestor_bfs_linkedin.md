# Mastering Binary Trees: Tracking Path Extremes with Level-Order BFS  (Part 2) ⚡🌲

In **Part 1**, we broke down the core invariant for finding the maximum ancestor-descendant difference in a binary tree:

> Along any root-to-leaf path, the maximum difference between any ancestor and descendant is simply $\max(\text{path}) - \min(\text{path})$.

We used top-down Depth-First Search (DFS) to propagate path extremes down to leaves. But what if you want to explore the tree horizontally, level by level?

Good news: BFS can track path-specific state across independent branches!

---

### 💡 The Solution: Level-Order BFS with State Propagation

Instead of diving deep along one branch, **Breadth-First Search (BFS)** sweeps through the tree level by level using a `deque`:

1. **Queue State:** Store tuples of `(node, cur_min, cur_max)` in the queue. So a tuple has a current node and the ancestral min and max values relative to that node.
2. **Update Bounds:** As each node is dequeued, update the running path extremes:
   `cur_min = min(cur_min, node.val)`
   `cur_max = max(cur_max, node.val)`
3. **Leaf Evaluation:** If the node is a leaf (`not left and not right`), evaluate `max_diff = max(max_diff, cur_max - cur_min)` and proceed to the next iteration.
4. **Enqueue Children:** Enqueue non-empty children along with the updated `(cur_min, cur_max)`.

Because each tuple is immutable, every branch maintains its own independent path history with zero cross-talk between siblings!

---

### 📊 Architectural & Memory Trade-Offs

| Approach | Time | Auxiliary Space | Memory Bound | Best Suited For |
| :--- | :--- | :--- | :--- | :--- |
| 🔄 **Recursive DFS** | $\mathcal{O}(N)$ | $\mathcal{O}(H)$ | Tree Height (Call Stack) | Clean code, balanced trees |
| 📦 **Iterative DFS** | $\mathcal{O}(N)$ | $\mathcal{O}(H)$ | Tree Height (Heap Stack) | Deep/skewed trees, stack-safety |
| ⚡ **Level-Order BFS** | $\mathcal{O}(N)$ | $\mathcal{O}(W)$ | Tree Width (Queue on Heap) | Streaming nodes, shallow wide trees |

---

### 🧠 Key Engineering Takeaways

1. **Height vs. Width Memory Trade-Off:**
   - DFS space is bounded by tree height ($H$). On balanced trees: $\mathcal{O}(\log N)$.
   - BFS space is bounded by tree maximum width ($W$). On balanced trees: $\mathcal{O}(N/2) = \mathcal{O}(N)$.
   - For deeply nested trees, BFS can use less peak memory; for wide balanced trees, DFS is often more memory-efficient.

2. **Immutable State Propagation:** Passing state down tuples in BFS queues eliminates shared mutable state bugs—a crucial pattern in concurrent and streaming systems.

Do you prefer DFS or BFS when dealing with path properties?

#LearningInPublic #Python #Algorithms #DataStructures #LeetCode #SoftwareEngineering #CodingInterview #CleanCode #BFS #SystemDesign
