# Mastering Binary Trees: Depth-Indexed Zigzag Traversal with DFS (Part 2 of 2)🌲🔄

In **Part 1**, we explored the intuitive Breadth-First Search (BFS) approach for zigzag level-order traversal. But what happens when memory is a constraint on massive, balanced trees where the bottom tier holds up to 50% of all nodes ($\approx N/2$)?

**Depth-First Search (DFS)** to the rescue!

---

### 💡 The DFS Insight: Depth-Indexed Buckets

DFS dives deep along a branch but we can still construct horizontal zigzag rows by passing the current `depth` to our traversal:

1. **Dynamic Level Allocation**: When visiting a node at `depth == len(result)`, create a new double-ended queue (`deque`) for that tier.
2. **Directional Placement with $\mathcal{O}(1)$ Insertion**:
   - **Even Depths (0, 2, 4...)**: Append to the right $\to$ `result[depth].append(node.val)`
   - **Odd Depths (1, 3, 5...)**: Append to the left $\to$ `result[depth].appendleft(node.val)`
3. **Preserving Left-to-Right Precedence**: Always traverse `node.left` before `node.right`.

By utilizing `deque.appendleft()`, we avoid the $\mathcal{O}(k)$ array shifting cost of `list.insert(0, val)`.

---

### 🛡️ Recursive vs. Iterative DFS (Stack Safety)

- **Recursive DFS**: Clean, declarative, and concise. It relies on Python's call stack, taking $\mathcal{O}(H)$ memory ($H = \text{tree height}$).
- **Iterative DFS**: For deep or skewed trees where $H > 1,000$, recursive calls risk a `RecursionError`. By managing an explicit stack of `(node, depth)` tuples on the heap and pushing right-child before left-child, we achieve identical traversal order with complete stack-overflow immunity.

---

### ⚖️ BFS vs. DFS Architectural Comparison

| Metric | Level-Order BFS | Recursive DFS | Iterative DFS (Stack) |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| **Auxiliary Space (Balanced Tree)** | $\mathcal{O}(N)$ queue ($\approx N/2$ nodes) | $\mathcal{O}(\log N)$ call stack | $\mathcal{O}(\log N)$ heap stack |
| **Auxiliary Space (Skewed Tree)** | $\mathcal{O}(1)$ queue | $\mathcal{O}(N)$ call stack | $\mathcal{O}(N)$ heap stack |
| **State Finalization** | Finalized per tier | Finalized at end of traversal | Finalized at end of traversal |
| **Stack Overflow Risk** | None | Possible on deep trees ($H > 1000$) | None |

---

When building tree pipelines in production, do you prefer BFS for natural level boundaries or DFS for $\mathcal{O}(\log N)$ memory efficiency on balanced trees?

#LearningInPublic #Python #DataStructures #Algorithms #LeetCode #SoftwareEngineering #CleanCode #DFS #TreeTraversal #SystemDesign
