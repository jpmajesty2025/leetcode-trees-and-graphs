# Beyond Plain BFS: Bidirectional Search & A* with Chebyshev Distance 🚀🤖

In Part 1, we optimized single-source BFS on an 8-directional binary grid.

However, standard BFS expands uniformly in all directions like a growing circle. On large or obstacle-heavy grids, exploring backwards from the goal is just as wasteful as exploring away from it.

How can we prune the search space by $50\%\text{--}80\%$?

---

### 💡 Technique 1: Bidirectional BFS (Halving Search Volume)

Instead of expanding a single radius-$R$ search circle (area $\propto \pi R^2$), expand **two simultaneous frontiers** of radius $R/2$ from `(0, 0)` and `(N-1, N-1)`:
$$\text{Area} = 2 \times \pi \left(\frac{R}{2}\right)^2 = \frac{1}{2} \pi R^2$$

• Always expand the smaller queue to balance work.
• When the two frontiers collide at a common cell, the global shortest path is found.

---

### 💡 Technique 2: A* Search with Chebyshev Distance

In 8-directional grids, moving diagonally has the same cost ($1$) as moving horizontally or vertically.

Therefore, **Manhattan distance is inadmissible** (it overestimates cost and breaks optimality).

The mathematically correct admissible heuristic is **Chebyshev Distance**:
$$h(r, c) = \max(|(N - 1) - r|, |(N - 1) - c|)$$

Using a min-heap priority queue sorted by $f(n) = g(n) + h(n)$, A\* pulls exploration directly along the diagonal toward the goal, bypassing dead ends and massive open areas.

---

### 📊 Strategy Comparison

| Metric | Unidirectional BFS | Bidirectional BFS | A* Search (Chebyshev) |
| :--- | :--- | :--- | :--- |
| **Exploration Shape** | Expanding circle | Two colliding circles | Targeted ellipse toward goal |
| **Data Structure** | `deque` | Two `deque`s | `heapq` (Min-Heap) |
| **Best Scenario** | Small/toy grids | High branch-factor grids | Large maps with open corridors |

---

### 🎯 Key Engineering Takeaways

• In robotics, game development, and GPS navigation, **A\*** and **Bidirectional Search** are industry standards for path planning.
• Matching the heuristic ($h$) to grid geometry (Manhattan for 4-way, Chebyshev for 8-way, Euclidean for continuous space) is critical for correctness.

Check out the Bidirectional and A* implementations in the attached image! 📸

Which pathfinding algorithm do you use most in your production systems? Let's discuss in the comments! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #GameDev #ArtificialIntelligence
