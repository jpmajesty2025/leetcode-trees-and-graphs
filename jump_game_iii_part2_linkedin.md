# In-Place Sign-Flipping vs Queue BFS: Memory-Optimal Traversals 🏃‍♂️🧙‍♂️

In Part 1, we formulated Jump Game III as a graph reachability problem and fixed the O(N^2) list pop bottleneck with `collections.deque`.

*Can we eliminate auxiliary visited sets entirely and achieve ZERO extra heap allocations?*

Let's compare **Iterative Deque BFS** with **In-Place Sign-Flipping DFS**.

---

### 💡 The Sign-Flipping Insight

The problem statement guarantees that all initial array elements are **non-negative** (`arr[i] >= 0`).

We can exploit this domain constraint to store the visited state **directly inside the input array**:
1. When visiting index `i`, negate its value: `arr[i] = -arr[i]`.
2. A negative value (`arr[i] < 0`) signals that the index has already been visited!
3. To jump, recover the jump magnitude via `-arr[i]` (or negate after reading).

---

### ⚡ Clean Recursive In-Place DFS

```python
def can_reach_inplace(arr: list[int], start: int) -> bool:
    if not (0 <= start < len(arr)) or arr[start] < 0:
        return False
    if arr[start] == 0:
        return True

    jump = arr[start]
    arr[start] = -arr[start]  # Mark visited in-place

    return (can_reach_inplace(arr, start + jump) or 
            can_reach_inplace(arr, start - jump))
```

---

### 📊 Architectural Comparison

| Dimension | Deque Level BFS | In-Place Sign DFS |
| :--- | :--- | :--- |
| **Time Complexity** | O(N) Linear | O(N) Linear |
| **Auxiliary Heap Allocations** | O(N) (Queue + Visited Set) | **O(1) Strict Zero Heap** |
| **Call Stack Memory** | O(1) (Iterative loop) | O(N) Recursion stack |
| **Input Mutability** | Non-destructive (Pure) | Destructive (Modifies input) |
| **Early Termination** | Breadth-first (Shortest path) | Depth-first |

---

### 🎯 Engineering Trade-Offs

• **Pure Functions vs In-Place Mutations**: In concurrent systems or re-entrant pipelines, mutating input arguments introduces side-effects. Creating a shallow copy preserves purity at the cost of O(N) memory.
• **Domain-Specific Encoding**: Using sign bits or sentinel values for state tracking is a classic systems engineering technique for embedded software and cache-constrained pipelines.

Check out both implementations in the attached image! 📸

Do you prefer pure immutable data structures or in-place memory optimizations in your production workflows? Let's discuss in the comments! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CleanCode #Performance
