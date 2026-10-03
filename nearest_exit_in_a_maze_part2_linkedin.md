# Shrinking Search Space: Bidirectional BFS by Meeting in the Middle 🧭🎯

In Part 1, we optimized single-source BFS by checking exit criteria at push-time and marking visited cells in-place.

When searching expansive mazes with multiple possible exits, standard BFS radiates outward in an expanding radial circle.

*Can we drastically shrink the number of explored cells by searching from both ends simultaneously?*

Yes! Using **Bidirectional Breadth-First Search (Bidirectional BFS)**.

---

### 💡 The Mathematical Geometry of Search Space

Suppose the shortest distance between start and exit is $d$:
• **Standard BFS** explores an expanding circle of radius $d$, covering an area proportional to:
  $$\text{Area}_{\text{standard}} \approx \pi d^2$$
• **Bidirectional BFS** grows two circles of radius $d / 2$ (one from the entrance, one from the exits):
  $$\text{Area}_{\text{bidirectional}} \approx 2 \times \pi \left(\frac{d}{2}\right)^2 = \frac{\pi d^2}{2} = \mathbf{50\% \text{ of the search space!}}$$

In higher branching factor graphs, this reduces complexity from $\mathcal{O}(b^d)$ down to $\mathbf{O(b^{d/2})}$.

---

### ⚡ Mechanics of Bidirectional Grid Search

1️⃣ **Dual Frontiers**:
• Forward queue initialized at `start = entrance`.
• Backward queue initialized with all candidate border `exits`.

2️⃣ **Wavefront Balancing**:
• At each step, always expand the **smaller queue** to keep the search balanced and minimize branching.

3️⃣ **Collision Detection**:
• The instant an expanding step hits a cell already visited by the opposing search:
  $$\text{total\_distance} = \text{forward\_dist} + \text{backward\_dist} + 1$$
• Return the total distance immediately!

---

### 📊 Comprehensive Strategy Comparison

| Strategy | Search Direction | Search Geometry | Peak Visited Cells | Mutates Input? |
| :--- | :--- | :--- | :--- | :--- |
| **Standard Pop-Time BFS** | Forward only | Full circle ($\pi d^2$) | High | No |
| **Push-Time In-Place BFS** | Forward only | Full circle ($\pi d^2$) | Medium | **Yes (Zero Memory)** |
| **Bidirectional BFS** | **Forward + Backward** | **Two half-circles ($\frac{\pi d^2}{2}$)** | **Minimal** | No |

---

### 🎯 Key Engineering Takeaways

• **Meeting in the Middle**: When the target state (or set of candidate targets) is known in advance, bidirectional search dramatically cuts exponential exploration.
• **Wavefront Balancing**: Alternating expansions based on queue size prevents one side from exploding into dead ends.

Check out the Bidirectional BFS implementation in the attached image! 📸

Have you applied bidirectional search or A* heuristics to large routing problems? Let's discuss in the comments! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CleanCode #ComputerScience
