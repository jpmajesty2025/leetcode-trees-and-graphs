# Zero-Allocation Distance K: Navigating Ancestor Offsets with Pure Tree DFS 🌲🧙‍♂️

In Part 1, we converted the unidirectional binary tree into a bidirectional structure by recording parent pointers and radiating BFS outward.

*Can we find all nodes at distance $k$ using pure recursive DFS with ZERO extra graph dictionaries, parent maps, or BFS queues?*

Yes! By tracking the distance to the target as the recursive call stack unwinds from bottom to top.

---

### 💡 The Mathematical Insight: Ancestor Offsets

When searching for `target` recursively:
1️⃣ **Downwards from Target**:
• When `node is target`, simply collect all nodes at distance $k$ in `target`'s own subtree.

2️⃣ **Upwards through Ancestors**:
• Suppose `target` is found in the **left subtree** at distance $d$.
• Then the current ancestor node is at distance $d + 1$ from `target`!
  - If $d + 1 == k$, this ancestor is one of the answers!
  - What about the ancestor's **right subtree**? Any node in the right subtree at distance $k - (d + 1) - 1 = \mathbf{k - d - 2}$ is also at distance $k$ from `target`!

3️⃣ **Symmetric Case for Right Subtree**:
• If `target` is in the right subtree at distance $d$, explore the left subtree at distance $k - d - 2$.

---

### 📊 Comprehensive Architectural Summary

| Strategy | Time Complexity | Extra Data Structures | Auxiliary Memory |
| :--- | :--- | :--- | :--- |
| **Adjacency List Graph + BFS** | $\mathcal{O}(N)$ | Graph Dict + Queue + Visited Set | $\mathcal{O}(N)$ |
| **Parent Map + Wavefront BFS** | $\mathcal{O}(N)$ | Parent Dict + Queue + Visited Set | $\mathcal{O}(N)$ |
| **Pure Subtree DFS (Zero Allocation)** | $\mathbf{O(N)}$ | **None (Pure Recursion)** | **$\mathcal{O}(H)$ Call Stack Only** |

---

### 🎯 Key Engineering Takeaways

• **Parent Pointer BFS** is usually the most intuitive and easiest to explain in technical interviews.
• **Pure Subtree DFS** is the most memory-efficient approach, utilizing recursive backtracking to traverse opposing subtrees with remaining distance offsets.

Check out the Pure Subtree DFS implementation in the attached image! 📸

Do you prefer Graph/BFS transformations or pure recursive backtracking for multi-directional tree searches? Let's discuss in the comments! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CleanCode #ComputerScience
