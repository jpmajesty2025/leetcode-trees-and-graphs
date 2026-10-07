# Bottom-Up Path Compression & Broadcast Trees (Part 2 of 2) 📡⚡

In Part 1, we calculated maximum broadcast delay using top-down iterative BFS over an adjacency list.

Can we solve this **without building an adjacency list at all**?

Let's explore bottom-up path memoization and real-world distributed broadcast systems!

---

### 💡 The Zero-Adjacency Optimization: Bottom-Up Memoization

Because each employee has exactly one manager in `manager[i]`, we already have parent pointers!

Instead of building child lists:
1. Initialize an array `memo = [-1] * n` where `memo[headID] = 0`.
2. For each employee `i`, climb upward toward `headID` until hitting an already-resolved ancestor.
3. Propagate the accumulated delay back down along the traversed path (path compression).

**Why this shines**:
- Eliminates the allocation overhead of dynamic adjacency lists.
- Each node's upward path is evaluated at most once, maintaining strict **O(N)** time!

---

### 🚀 Real-World Distributed Systems Applications

Hierarchical delay modeling directly maps to core distributed infrastructure:

1. **P2P Gossip & Blockchain Broadcasts**:
   - In Bitcoin and Ethereum networks, estimating block/transaction propagation latency across peer topologies determines stale block (uncle) rates.
2. **Push Notification & Alert Cascades**:
   - In enterprise incident management (PagerDuty, Opsgenie), on-call escalation trees use path latency calculations to model SLA breach thresholds.
3. **Workflow Engines & Critical Path Method (CPM)**:
   - Systems like Apache Airflow and Temporal evaluate weighted task DAGs to compute the critical path (makespan bottleneck) for pipeline completion.

---

### 📊 Complexity Profile

- **Time Complexity: O(N)** — Amortized linear pass via path compression.
- **Space Complexity: O(N)** — Memo array without adjacency list overhead.

---

Have you leveraged bottom-up parent pointer traversal to avoid adjacency allocations in your services?

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #TreeAlgorithms #SystemDesign #DistributedSystems
