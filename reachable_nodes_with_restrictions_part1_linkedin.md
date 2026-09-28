# Tree Traversal with Restrictions: Eliminating the Dual-Set Anti-Pattern 🌲🚫

When exploring an undirected tree while avoiding a set of restricted nodes (LeetCode 2368: $N \le 100,000$), how do you track state?

A very common pattern is maintaining two separate hash sets:
```python
# ⚠️ Common Pattern: Dual hash sets
restricted_set = set(restricted)
visited = set()

# Inside traversal:
for neighbor in graph[curr]:
    if neighbor not in visited and neighbor not in restricted_set:
        visited.add(neighbor)
        queue.append(neighbor)
```

It works, but examine the subtle overhead at scale:

---

### 🚨 Why Dual-Set Lookups Hurt Performance

1️⃣ **Double Hashing Overhead**: Every single edge inspection triggers two separate hash table lookups (`neighbor not in visited` AND `neighbor not in restricted_set`).
2️⃣ **Memory Fragmentation**: Allocating `defaultdict(list)` + two dynamic hash sets on $100,000$ integers introduces significant cache misses and memory churn.

---

### 💡 The Clean Optimization: Unified Pre-Marked Boolean Array

Why maintain two sets when a single contiguous boolean array can track both restrictions and traversal state?

```python
# 1. Fixed-size list adjacency
graph = [[] for _ in range(n)]
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)

# 2. Unified boolean array
visited = [False] * n
for node in restricted:
    visited[node] = True  # Pre-mark restricted nodes as visited!

# 3. Traversal simplifies to a single condition
for neighbor in graph[curr]:
    if not visited[neighbor]:
        visited[neighbor] = True
        queue.append(neighbor)
```

---

### ⚖️ Traversal Trade-Offs

| Approach | Neighbor Condition | Memory Footprint | Edge Check Speed |
| :--- | :--- | :--- | :--- |
| **Dual Hash Sets** | `not in visited and not in restricted` | $2 \times \text{Set}$ + Dict Graph | Slower (2 hash lookups) |
| **Unified BFS / DFS** | `not visited[neighbor]` | Flat `[False] * n` array | **Instant ($O(1)$ direct index)** |

---

Check out the clean implementations in the attached snippet! 📸

In Part 2 tomorrow, we’ll explore how to solve restricted reachability with **Disjoint Set Union (Union-Find) without building an adjacency tree**!

How do you handle node filtering in your graph algorithms? Let's discuss below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #ComputerScience
