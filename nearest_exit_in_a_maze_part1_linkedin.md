# Maze Navigation: Push-Time Early Exit & In-Place Memory Optimization 🧭⚡

When searching for the shortest path from an entrance to the nearest border exit in a grid maze, Breadth-First Search (BFS) is the standard algorithm of choice.

However, two subtle implementation details often double both the runtime and memory footprint of standard BFS:

---

### 🚨 Pitfall 1: Pop-Time vs. Push-Time Exit Checking

In typical textbook BFS, developers check the goal condition when a node is **popped**:
`curr = queue.popleft()`
`if is_exit(curr): return steps`

Why is this suboptimal?
• By the time a node is popped, all of its sibling nodes on the current level have already explored and enqueued **an entire extra layer of redundant neighbors**!
• Checking for the exit condition **immediately at neighbor generation (push-time)** terminates the search the exact instant an exit is spotted, skipping thousands of useless allocations.

---

### 🚨 Pitfall 2: The `visited: set()` Tuple Allocation Trap

Many implementations track visited cells using a Python `set()` of coordinate tuples:
`visited.add((nr, nc))`

In a large grid:
1. Every visited cell allocates a `(row, col)` tuple on the heap.
2. Hashing and rehashing the set causes CPU and memory churn.

---

### 💡 The High-Performance Fix: In-Place Wall Marking

1️⃣ **Push-Time Termination**:
• As soon as `nr == 0 or nr == rows - 1 or nc == 0 or nc == cols - 1`, return `steps + 1` instantly!

2️⃣ **In-Place Wall Transformation**:
• Instead of storing visited coordinates in an external set, mutate the grid directly: `maze[nr][nc] = '+'`.
• The wall symbol `'+'` naturally acts as the visited marker, completely preventing cycles and duplicate visits.

• **Auxiliary Space**: Drops from $\mathcal{O}(M \times N)$ down to just the peak queue perimeter $\mathbf{O(M + N)}$!

---

### ⚖️ Performance Comparison

| Metric | Pop-Time BFS + Set | Push-Time BFS + In-Place Marking |
| :--- | :--- | :--- |
| **Exit Detection** | On `queue.popleft()` (Late) | **On Neighbor Generation (Instant)** |
| **Visited Tracking** | Heap-allocated `set()` of tuples | **Direct `maze[r][c] = '+'` in-place** |
| **Auxiliary Memory** | $\mathcal{O}(M \times N)$ | **$\mathbf{O(M + N)}$ peak queue only** |
| **Garbage Collection** | High tuple allocation churn | **Zero GC pressure** |

---

Check out the clean In-Place BFS implementation in the attached snippet! 📸

In Part 2 tomorrow, we’ll explore how **Bidirectional BFS cuts the exploration search space in half by meeting in the middle!**

Do you check target conditions at push-time or pop-time in your search pipelines? Let's discuss below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #SystemDesign #ComputerScience
