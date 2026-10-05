# State-Machine Traversal: Alternating Paths in Binary Trees 🌲⚡

We are given the root of a binary tree.

A **ZigZag path** is an alternating sequence of directional steps:
• Move Right ➡️ Move Left ➡️ Move Right ➡️ Move Left...
• Or: Move Left ➡️ Move Right ➡️ Move Left ➡️ Move Right...

The path can start at ANY node, and its length is the number of edges traversed.

```
          1
           \
            1
           / \
          1   1
             / \
            1   1
                 \
                  1

Longest ZigZag Path = 3 (Right ➡️ Left ➡️ Right)
```

How do we track alternating states across all subtrees in a single linear pass?

---

### 🚨 The Branching Decision Problem

During an active zigzag path, we face two choices at each child:

1. **Alternating Continuation**: Moving in the opposite direction continues the active streak (`length + 1`).
2. **Same-Direction Restart**: Moving in the same direction breaks the zigzag, but starts a new zigzag of length `1`!

Exploring every starting node independently leads to quadratic O(N²) time on skewed trees.

---

### 💡 The Top-Down Directional State Machine

We model this as a 2-state automaton passed down the call stack:
`dfs(node, expected_direction, current_length)`

At each node:
• **Update Global Max**: `max_length = max(max_length, current_length)`
• **If Expected is Left**:
  • Moving Left continues streak: pass `Right` and `length + 1`.
  • Moving Right breaks streak: pass `Left` and restart `1`.
• **If Expected is Right**:
  • Moving Right continues streak: pass `Left` and `length + 1`.
  • Moving Left breaks streak: pass `Right` and restart `1`.

Every node is visited once in strictly O(N) linear time.

---

### ⚖️ Complexity

| Metric | State Machine DFS | Subtree Restarts |
| :--- | :--- | :--- |
| **Time** | **O(N)** (Single pass) | **O(N²)** worst-case |
| **Call Stack** | **O(H)** | **O(N)** |
| **State** | **Single boolean** | Multiple traversals |

---

In Part 2, we contrast **Top-Down DFS vs Bottom-Up Tree DP!**

Check out the implementation in the attached image! 📸

How do you model directional state in tree traversals? Let's discuss! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #TreeTraversals #CleanCode #Performance
