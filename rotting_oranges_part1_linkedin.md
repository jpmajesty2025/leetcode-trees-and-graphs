# Multi-Source BFS & Synchronous Wavefronts: Rotting Oranges (Part 1 of 2) 🍊⏱️

How do you model events spreading concurrently from multiple origins across a grid?

In "Rotting Oranges", we have a grid of empty cells (`0`), fresh oranges (`1`), and rotten oranges (`2`). Every minute, fresh oranges adjacent to rotten ones rot. We must find the minimum minutes until no fresh orange remains, or return `-1`.

One approach: multi-source BFS and concurrent wavefront expansion!

---

### 💡 The Multi-Source Invariant: Simultaneous Propagation

A common pitfall is running BFS from one rotten orange at a time. But rotting happens **simultaneously across all sources in parallel**!

If orange A and orange B are both rotten at `minute = 0`:
- They expand outward concurrently.
- A fresh orange between them rots as soon as the **closer** wavefront arrives.
- Running separate sequential searches inflates time complexity.

Instead, **Multi-Source BFS** seeds the queue with every initial rotten orange before the timer starts!

---

### ⚙️ The Level-by-Level Queue Architecture

1. **Initialization**:
   - Count fresh oranges (`fresh_count`).
   - Push all coordinates with value `2` into a `deque`.
   - **Edge Case**: If `fresh_count == 0`, return `0` immediately.

2. **Wavefront Expansion**:
   - Snapshot the queue size for the minute: `for _ in range(len(queue))`.
   - Pop each wavefront cell, check 4 orthogonal neighbors, and infect fresh oranges (`1 → 2`).
   - Decrement `fresh_count` and push newly infected coordinates into the queue.

3. **Termination**:
   - Stop when the queue is empty or `fresh_count == 0`.
   - If `fresh_count == 0`, return elapsed minutes; if isolated oranges remain, return `-1`.

---

### 📊 Complexity Profile

- **Time: O(M * N)** — Every cell is enqueued and dequeued at most once.
- **Space: O(M * N)** — For the BFS queue in the worst case.

---

👉 **In Part 2**, we will explore **Epidemic SEIR Modeling, Failure Blast Radius in Distributed Systems, and Image Dilation**!

How do you model multi-source concurrency in your graph engines?

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #GraphTheory #BFS #CleanCode #PerformanceOptimization
