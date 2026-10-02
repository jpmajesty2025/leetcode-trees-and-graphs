# 01 Matrix: The Single-Source BFS Trap & The Multi-Source Wavefront 🌊⚡

You need to find the shortest distance to the nearest `0` for every cell in a binary matrix. So, how do you orchestrate your search?

Maybe your intuition says **Single-Source BFS from every `1`**:
1. Iterate over every cell $(r, c)$ where `mat[r][c] == 1`.
2. Launch a brand-new BFS to find the closest `0`.

You fallen in a trap! Let's see why is this an architectural disaster at scale.

---

### 🚨 The Hidden $\mathcal{O}((M \times N)^2)$ Bottleneck

If your grid is $100 \times 100$ ($10,000$ cells):
• Starting a fresh BFS from every `1` repeatedly re-traverses the entire grid.
• Runtime explodes to $\mathcal{O}(M^2 \times N^2) \approx 10^8$ operations, causing immediate Time Limit Exceeded (TLE) timeouts.

---

### 💡 The Fix: Multi-Source Wavefront BFS

Instead of searching from `1`s towards `0`s, **reverse the perspective**:
Start the search from **ALL `0`s simultaneously**!

1️⃣ **Multi-Source Initialization**:
• Collect all `(r, c)` where `mat[r][c] == 0` into a single `collections.deque`.
• Initialize a `dist` matrix with `0` for zeros and `-1` for unvisited ones.

2️⃣ **Concentric Wavefront Expansion**:
• Dequeue cells level-by-level.
• When expanding to unvisited neighbor $(nr, nc)$ where `dist[nr][nc] == -1`:
  `dist[nr][nc] = current_dist + 1`
• Push $(nr, nc)$ into the queue.

3️⃣ **Eliminate `seen: set()` Overhead**:
• The `dist[nr][nc] == -1` check replaces expensive Python `set()` allocations of coordinate tuples, slashing garbage collection churn!

Every cell is enqueued and processed **exactly once**, dropping runtime down to strictly $\mathbf{O(M \times N)}$!

---

### ⚖️ Performance Comparison

| Metric | Single-Source BFS Churn | Multi-Source Wavefront BFS |
| :--- | :--- | :--- |
| **Time Complexity** | $\mathcal{O}((M \times N)^2)$ (Slow) | $\mathbf{O(M \times N)}$ **Linear (Strict)** |
| **Visited Tracking** | Reset set per query | **Direct `-1` matrix lookup** |
| **Traversal Perspective** | $1 \to 0$ (Many-to-Many) | **$0 \to 1$ (Simultaneous Broadcast)** |
| **Auxiliary Space** | $\mathcal{O}(MN)$ | $\mathcal{O}(MN)$ |

---

Check out the clean Multi-Source BFS implementation in the attached snippet! 📸

In Part 2 tomorrow, we’ll see how to eliminate queues and heap allocations entirely using **Two-Pass Dynamic Programming!**

Do you default to BFS or DP for grid distance calculations? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #BFS #LeetCode #CleanCode #SystemDesign #ComputerScience
