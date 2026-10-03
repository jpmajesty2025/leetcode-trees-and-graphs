# Bidirectional Search Mastery: Dynamic Frontier Swapping in Python 🔒🧙‍♂️

In Part 1, we saw how searching from both `'0000'` and `target` reduces search complexity from $8^d$ down to $8^{d/2}$.

*How do you implement Bidirectional BFS without managing two queues and lockstep counters?*

### 💡 The Frontier Swapping BFS Idiom

Managing two standard `deques` requires awkward bookkeeping to prevent one frontier from outpacing the other.

Sets achieve optimal frontier balancing in just **two lines of code**:

```python
# Always expand the smaller frontier
if len(forward) > len(backward):
    forward, backward = backward, forward
```

Why is this simple swap so powerful?
1. **Minimizes Branching**: Expanding the smaller set generates fewer child nodes in the next iteration.
2. **Naturally Symmetric**: We only write the expansion logic once! The algorithm automatically alternates between expanding from start and expanding from target.

---

### ⚡ Mechanics of Set-Based Level Expansion

1️⃣ **Level Generation**:
• For each 4-digit code in `forward`, generate all 8 adjacent single-wheel turns.

2️⃣ **Instant Collision Check**:
• If `new_state in backward`, a valid path connects start and target! Return `turns` immediately.

3️⃣ **Pruning & Advancing**:
• If `new_state` is unvisited and not in `dead_set`:
  - Mark `visited.add(new_state)` and add to `next_level`.
• Set `forward = next_level` and increment `turns`.

---

### 📊 Strategy Comparison

| Strategy | Data Structure | Frontier Balancing | Peak Memory Overhead |
| :--- | :--- | :--- | :--- |
| **Unidirectional BFS** | `deque` of `(state, dist)` | None (Single direction) | High ($10,000$ states) |
| **Dual-Queue BFS** | 2 $\times$ `deque` + 2 $\times$ `visited` | Manual size tracking | Medium |
| **Frontier Swapping Set BFS** | **2 $\times$ `set` + 1 $\times$ `visited`** | **Automatic (`len` swap)** | **Minimal (Active level only)** |

---

### 🎯 Key Engineering Takeaways

• **Deterministic Targets = Bidirectional BFS**: When start and end states are known and edges are reversible, bidirectional search cuts exponential search space.
• **Set BFS over Queues**: In discrete level-order graph searches, `set` replacements for `deque` eliminate duplicate expansions and make collision checks $\mathcal{O}(1)$.

What graph traversal patterns do you rely on for large state-space puzzles? Let's discuss below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CleanCode
