# Tree Prefix Hash Maps: Backtracking & State Isolation 🌲🛡️

In Part 1, we saw how 1D prefix sum hashing accelerates downward path counting in a binary tree from O(N²) to O(N) linear time.

*Why can't we just use a persistent global hash map like we do on an array?*

Let's look at the **Cross-Branch Contamination Problem** and why **Backtracking** is mandatory.

---

### 🚨 The Cross-Branch Contamination Trap

Arrays are linear: every preceding index is a true ancestor.

Trees, however, **branch into disjoint subtrees**:
• If node `A` in the left subtree records `PrefixSum = 15` in a shared hash map, and we subsequently traverse into the right subtree...
• A node `B` in the right subtree might encounter `CurrentSum - Target = 15` and falsely count node `A` as an ancestor!
• But there is **no downward path** connecting node `A` to node `B`.

Without branch isolation, prefix counts leak across subtrees and corrupt the output.

---

### 💡 The Backtracking Scope Invariant

To ensure the hash map *only* reflects the active root-to-node path, we apply **Hash Map Backtracking**:

1. **Enter Node**: Register the running sum (`PrefixCounts[CurrentSum] += 1`).
2. **Explore**: Recurse down `left` and `right` subtrees.
3. **Exit Node (Backtrack)**: Decrement the prefix count (`PrefixCounts[CurrentSum] -= 1`).

When the call stack unwinds to visit a sibling branch, the current node's prefix is completely purged from the map.

---

### 📊 Strategy & Space Comparison

| Strategy | Time Complexity | Hash Map Scope | Cross-Branch Leaks |
| :--- | :--- | :--- | :--- |
| **Double DFS Recursion** | O(N²) worst-case | None (Recomputed) | None |
| **Persistent Hash Map** | O(N) | Global Tree (All nodes) | **High (Corrupted Output)** |
| **Backtracking Hash Map DFS** | **O(N) Optimal** | **Active Branch Only** | **Zero (Strictly Isolated)** |

---

### 🎯 Key Engineering Takeaways

• **Lexical Path Scoping**: When sharing mutable lookup tables across recursive branches, always undo state changes upon return.
• **Bounded Memory Footprint**: Because the map only tracks the active branch, memory is bounded by tree height `O(H)` (O(log N) balanced) rather than `O(N)`!

Check out the implementation in the attached code image! 📸

How do you manage mutable state across branching recursions? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CleanCode #Performance
