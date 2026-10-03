# Shortest Paths in Non-Deterministic Games: Modeling State Transitions with BFS 🎲🎯

In Part 1, we optimized board navigation by pre-flattening the 2D Boustrophedon grid into a 1D lookup array.

*How do you formulate optimal turn-based game strategies when players can roll random dice and jump across snakes or ladders?*

By modeling the game as a **Directed Unweighted Shortest Path Graph**!

---

### 💡 The Graph Abstraction

Every square on the board represents a vertex in a directed state graph:
• **Vertices ($V$)**: Squares $1, 2, \dots, n^2$. Total $V = n^2$.
• **Directed Edges ($E$)**: From square `curr`, a player can roll $1 \dots 6$, generating up to 6 directed edges to `dest = flat_board[curr + roll]`.
• **Edge Weights**: Every dice roll represents **$1$ uniform step**, making the graph completely **unweighted**.

Since edge weights are uniformly $1$, **Breadth-First Search (BFS)** guarantees finding the shortest path in strictly $\mathbf{O(V + E)} = \mathbf{O(N^2)}$ time without needing priority queues or Dijkstra's algorithm!

---

### 🚨 The Visited State Nuance: Destination vs. Roll Square

A critical implementation detail in Snakes and Ladders is how to manage the `visited` set:

1️⃣ If a roll takes you to square `next_sq` which contains a ladder to `dest`:
• You do **NOT** stop at `next_sq` — you are immediately transported to `dest`.
• Therefore, we record **`dest`** in the `visited / dist` array!

2️⃣ Marking `dest` as visited ensures:
• If another dice roll path reaches `dest` with equal or greater turns, it is immediately pruned.
• Infinite cycles between opposing snakes and ladders are naturally avoided without extra cycle detection code.

---

### 📊 Comprehensive Game Traversal Comparison

| Search Strategy | Time Complexity | Extra Data Structures | Guarantees Shortest Path? |
| :--- | :--- | :--- | :--- |
| **Depth-First Search (DFS)** | $\mathcal{O}(6^{N^2})$ (Exponential) | Recursion stack | ❌ No (Can get trapped in cycles) |
| **Dijkstra’s Algorithm** | $\mathcal{O}(N^2 \log N)$ | Priority Queue (Min-Heap) | ✅ Yes (Overkill for unit weights) |
| **Unweighted BFS** | $\mathbf{O(N^2)}$ **(Optimal)** | **Standard `collections.deque`** | ✅ **Yes (Guaranteed minimum moves)** |

---

### 🎯 Key Engineering Takeaways

• **Uniform Cost = BFS**: Never use Dijkstra or A* when all state transition edge costs are $1$; BFS gives optimal $\mathcal{O}(V + E)$ linear time.
• **State Collapsing**: Collapsing instant teleportation mechanics into single graph transitions eliminates multi-hop recursion overhead.

Check out the full BFS graph implementation in the attached image! 📸

How do you approach modeling state transitions in game simulations and pathfinding engines? Let's discuss in the comments! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CleanCode #ComputerScience
