# Cutting Search Spaces in Half: Bidirectional BFS 🧬🧙‍♂️

In Part 1, we modeled genetic mutation as an unweighted shortest path problem using standard BFS.

*When search depth d grows, standard BFS expands an exponential search tree of size O(b^d). How can we dramatically shrink this search volume?*

Enter **Bidirectional Breadth-First Search (Bidirectional BFS)**.

---

### 💡 Why Search from Both Ends?

Consider a search space with branching factor `b = 10` and shortest path depth `d = 6`:
• **Standard BFS**: Explores up to `10^6 = 1,000,000` states.
• **Bidirectional BFS**: Two searches meet in the middle at `d / 2 = 3`:
  `2 * (10^3) = 2 * 1,000 = 2,000 states!`

That is a **500x reduction in visited states**! 🚀

---

### ⚡ The Frontier Swapping Trick

Implementing bidirectional BFS cleanly without managing two separate queues is enabled by **Frontier Swapping**:

1. Maintain two sets: `front_frontier = {startGene}` and `back_frontier = {endGene}`.
2. In each iteration, **always expand the smaller frontier**:
   ```python
   if len(front_frontier) > len(back_frontier):
       front_frontier, back_frontier = back_frontier, front_frontier
   ```
3. For each gene in `front_frontier`, generate all single-character mutations:
   • If a mutated string is in `back_frontier` ➡️ **Collision found! Return total steps.**
   • If in `bank_set` and unvisited ➡️ Add to `next_frontier`.
4. Replace `front_frontier = next_frontier` and repeat until frontiers meet or exhaust.

---

### 📊 Strategy Comparison

| Traversal Strategy | Search Volume | Memory Footprint | Dynamic Balancing |
| :--- | :--- | :--- | :--- |
| **Standard Queue BFS** | O(b^d) | O(b^d) Queue | None (One-way) |
| **Bidirectional BFS (Dual Queue)** | O(b^(d/2)) | O(b^(d/2)) | Fixed alternating |
| **Bidirectional BFS (Frontier Swapping)** | **O(b^(d/2))** | **O(b^(d/2))** | **Self-balancing (Optimal)** |

---

### 🎯 Key Engineering Takeaways

• **Symmetric Graph Search**: Whenever both start and target states are known in advance, bidirectional search cuts exponential exponents in half.
• **Frontier Swapping Elegance**: Swapping sets based on cardinality minimizes loop iterations and prevents uneven tree expansion.
• **Real-World Impact**: This pattern powers production pathfinders in Word Ladders, Rubik's cube solvers, and road network routing engines (OSRM, Google Maps).

Check out the Bidirectional BFS implementation in the attached image! 📸

Have you utilized bidirectional search in your production routing or game AI systems? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #GraphTheory #CleanCode
