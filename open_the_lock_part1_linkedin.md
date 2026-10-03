# Open the Lock: The 2,000x Speedup of Bidirectional Set BFS 🔒⚡

We are given a 4-wheel combination lock with slots $0 \dots 9$ that wrap around ($0 \leftrightarrow 9$). 

Starting from `'0000'`, we must find the minimum turns to reach a `target` combination while avoiding a list of `deadends`.

At each step, any of the 4 wheels can rotate forward or backward:
$$\text{Branching Factor } b = 4 \times 2 = 8$$

But, the standard unidirectional Breadth-First Search (BFS) suffer under deep targets.

---

### 🚨 The Exponential Search Explosion ($\mathcal{O}(b^d)$)

In standard single-source BFS radiating outward from `'0000'`:
• At depth $d$, the number of explored combinations scales exponentially as $\mathcal{O}(8^d)$.
• If the shortest path is $d = 8$ turns away:
  $$\text{States Explored} \approx 8^8 = \mathbf{16,777,216 \text{ nodes!}}$$

Even in a bounded $10,000$-state space, standard BFS explores nearly the entire state graph before reaching deep targets.

---

### 💡 The High-Performance Fix: Bidirectional BFS ($\mathcal{O}(b^{d/2})$)

Since both the starting state (`'0000'`) and the goal state (`target`) are known in advance, we can search from **both ends simultaneously**!

1️⃣ **Halving the Search Depth**:
• Forward search explores radius $d/2$; backward search explores radius $d/2$.
• Total explored states drops to:
  $$\text{States} \approx 2 \times 8^{d/2} = 2 \times 8^4 = \mathbf{8,192 \text{ nodes!}}$$
• That is a **$2,000\times$ reduction in explored search volume**!

2️⃣ **Set BFS Representation**:
• Instead of slow FIFO queues, represent frontiers as Python `set` objects: `forward = {'0000'}` and `backward = {target}`.
• Set lookups provide instant $\mathcal{O}(1)$ collision detection the instant frontiers meet!

---

### ⚖️ Complexity Comparison

| Metric | Unidirectional Queue BFS | Bidirectional Set BFS |
| :--- | :--- | :--- |
| **Search Complexity** | $\mathcal{O}(b^d)$ (Exponential) | $\mathbf{O(b^{d/2})}$ **(Halved Exponent)** |
| **Peak States ($d=8$)** | $\approx 1.67 \times 10^7$ | **$\approx 8,192$ (2,000x fewer states)** |
| **Collision Detection** | N/A (One-way scan) | **Instant $\mathcal{O}(1)$ Set Intersection** |
| **Frontier Balancing** | Fixed direction | **Dynamic (Always expands smaller set)** |

---

In Part 2 tomorrow, we’ll dive deep into **Frontier Swapping and Level Synchronization!**

Have you used bidirectional search to tame combinatorial explosion in state-space search? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #SystemDesign #ComputerScience
