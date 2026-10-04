# Bitset Transitive Closure: Ultra-Fast Reachability on Dense Graphs 💣🧙‍♂️

In Part 1, we formulated bomb chain reactions as an all-pairs reachability problem on a directed graph using multi-source BFS.

*When N <= 100, can we compute transitive reachability faster and more compactly than running 100 independent BFS traversals?*

Enter **Bitset Transitive Closure (Bitwise Floyd-Warshall)**.

---

### 💡 The Bitmask Representation

Instead of allocating graph adjacency lists, queues, and visited sets in heap memory:
• Represent all reachable bombs from node `i` as a single **integer bitmask**: `reach[i]`.
• If bomb `i` can detonate bomb `j`, the `j`-th bit of `reach[i]` is set to `1` (`reach[i] |= (1 << j)`).

---

### ⚡ Bitwise Floyd-Warshall in 6 Lines

We can propagate transitive reachability across all nodes using bitwise OR operations:

```python
# Propagate reachability through intermediate node k
for k in range(n):
    k_mask = 1 << k
    for i in range(n):
        if reach[i] & k_mask:
            reach[i] |= reach[k]  # 64-bit parallel union!

return max(mask.bit_count() for mask in reach)
```

Why is this so fast?
• In Python, integers have arbitrary precision, acting as native 64-bit/128-bit bitsets.
• The bitwise OR (`|=`) merges reachability for up to 64 nodes in a single CPU instruction!

---

### 📊 Strategy Comparison

| Traversal Strategy | Time Complexity | Auxiliary Space | CPU Cache Efficiency |
| :--- | :--- | :--- | :--- |
| **Multi-Source BFS** | O(N^3) in dense graph | O(N^2) lists & queues | Moderate (pointer chasing) |
| **Multi-Source DFS** | O(N^3) in dense graph | O(N) call stack | Moderate (stack frames) |
| **Bitset Transitive Closure** | **O(N^3 / 64)** | **O(N) integer array** | **Ultra-high (Flat array)** |

---

### 🎯 Key Engineering Takeaways

• **Bit-Level Parallelism**: When graphs are dense and vertex count N is moderate, bitwise operations eliminate pointer dereferencing and queue allocation overhead.
• **Popcount Optimization**: Python 3.10+'s built-in `int.bit_count()` compiles directly to hardware `POPCNT` instructions on modern x86/ARM CPUs.

Check out both implementations in the attached image! 📸

Have you leveraged bitwise matrix operations or transitive closures in your graph algorithms? Let's discuss in the comments! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CleanCode #Performance
