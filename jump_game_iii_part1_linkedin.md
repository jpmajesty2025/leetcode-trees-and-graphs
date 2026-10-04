# Graph Reachability in 1D Arrays: Beware the O(N^2) Deque Trap 🏃‍♂️🕹️

We start at index `start` in an array of non-negative integers.

From index `i`, we can jump left or right:
• `next_left = i - arr[i]`
• `next_right = i + arr[i]`

Can we reach any index with value `0` without jumping out of bounds?

---

### 💡 Array as an Implicit Directed Graph

While presented as an array jumping problem, this is fundamentally a **graph reachability problem**:
• **Nodes**: Array indices `0, 1, ..., n - 1`.
• **Edges**: At most 2 directed outgoing edges per index (`i + arr[i]` and `i - arr[i]`).
• **Target**: Any node `u` where `arr[u] == 0`.

Since edge weights are uniform (1 jump step), standard **Breadth-First Search (BFS)** explores reachable states in linear time.

---

### 🚨 The Silent O(N^2) Python List Trap

A frequent performance pitfall in Python BFS implementations is using a standard list as a queue:

```python
# ❌ DANGEROUS: pop(0) takes O(K) time for list length K!
queue = [start]
while queue:
    curr = queue.pop(0)  # Shifts every remaining element in memory!
```

Repeatedly calling `list.pop(0)` degrades an otherwise optimal `O(N)` algorithm into a slow `O(N^2)` bottleneck.

**The Fix**: Always use `collections.deque` with `popleft()`, which guarantees true `O(1)` amortized pop operations via double-ended chunked blocks!

---

### ⚡ The Early-Visited Invariant

Another subtle bug is marking nodes visited *after* popping from the queue instead of *when enqueueing*:
• If multiple paths reach index `j` in the same BFS layer, `j` gets pushed to the queue multiple times!
• **Best Practice**: Add to `visited` immediately upon push:
  ```python
  if 0 <= next_idx < n and next_idx not in visited:
      visited.add(next_idx)
      queue.append(next_idx)
  ```

---

### ⚖️ Algorithm Complexity

| Metric | BFS with collections.deque | Naive list.pop(0) BFS |
| :--- | :--- | :--- |
| **Time Complexity** | **O(N)** (Each index visited once) | **O(N^2)** (List shifting penalty) |
| **Auxiliary Space**| **O(N)** (Queue + Visited Set) | **O(N)** |
| **Traversal Guarantee** | **Shortest Jump Path** | Shortest Jump Path |

---

In Part 2 tomorrow, we’ll explore **In-Place Sign-Flipping DFS to achieve O(1) extra allocation space!**

How do you prevent subtle container performance traps in your day-to-day code? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #GraphTheory #Performance
