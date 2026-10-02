# Zero-Allocation Grid Distances: Two-Pass Dynamic Programming in O(1) Memory 🚀🧠

In Part 1, we used Multi-Source BFS to broadcast distances outward from all `0`s in $\mathcal{O}(M \times N)$ linear time.

However, BFS still requires allocating an auxiliary `deque` and enqueuing thousands of coordinates.

*Can we calculate exact grid distances across all 4 directions with ZERO queues, ZERO graph objects, and ZERO recursion stacks?*

Yes! Using **Two-Pass Dynamic Programming**.

---

### 💡 The Directional Decomposition Insight

A cell $(r, c)$'s shortest path to a `0` must approach from one of four cardinal directions:
$$\text{dist}[r][c] = \min(\text{Top}, \text{Left}, \text{Bottom}, \text{Right}) + 1$$

We cannot check all 4 neighbors in a single pass without circular dependencies. But we CAN decompose the 4 directions into **two complementary linear scans**:

1️⃣ **Pass 1: Top-Left $\implies$ Bottom-Right**:
• Scan row-by-row from $(0, 0)$ down to $(m-1, n-1)$.
• For each cell $(r, c)$ with value `1`, calculate its minimum distance using only already-computed **Top** and **Left** neighbors:
  $$\text{dist}[r][c] = \min(\text{dist}[r-1][c] + 1, \text{dist}[r][c-1] + 1)$$

2️⃣ **Pass 2: Bottom-Right $\implies$ Top-Left**:
• Scan in reverse from $(m-1, n-1)$ back to $(0, 0)$.
• Check **Bottom** and **Right** neighbors and take the overall minimum:
  $$\text{dist}[r][c] = \min(\text{dist}[r][c], \text{dist}[r+1][c] + 1, \text{dist}[r][c+1] + 1)$$

---

### 📊 Comprehensive Architectural Comparison

| Strategy | Time Complexity | Queue / Heap Allocations | Cache Locality | Memory Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **Single-Source BFS** | $\mathcal{O}((MN)^2)$ (Slow) | $\mathcal{O}(MN)$ queue per cell | Poor | Low |
| **Multi-Source BFS** | $\mathcal{O}(MN)$ (Optimal) | $\mathcal{O}(MN)$ single deque | Medium | Standard |
| **Two-Pass DP** | $\mathbf{O(MN)}$ **(Fastest)**| **Zero (No Queues/Sets)** | **Optimal (Sequential scan)** | **$\mathcal{O}(1)$ Extra Space** |

---

### 🎯 Key Engineering Takeaways

• **Cache Efficiency**: Two sequential linear passes through contiguous memory arrays yield superior CPU cache line utilization over queue pointer indirection.
• **Zero Garbage Collection**: Eliminating queue node allocations prevents GC thrashing under high concurrency.

Check out the Two-Pass DP implementation in the attached image! 📸

Have you utilized multi-pass dynamic programming for grid distance fields? Let's discuss in the comments! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CleanCode #DynamicProgramming
