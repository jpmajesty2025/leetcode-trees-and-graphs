# Algebraic Consistency: Multiplicative Weighted Disjoint Set Union 🌐⚖️

We are given a stream of algebraic equations:
• `A / B = 2.0`
• `B / C = 3.0`
• `A / C = 5.0` 🚨 (Contradiction! Since 2.0 * 3.0 = 6.0 != 5.0)

How do we validate consistency across dynamic equations in near-constant time?

---

### 🚨 Why Standard DSU Falls Short

Standard Disjoint Set Union (DSU / Union-Find) only tracks whether two variables belong to the same connected component.

To detect numerical contradictions, we must also track the **relative scaling ratio** between every node and its component representative.

---

### 💡 Multiplicative Path Compression

We augment DSU with a `weight` table:
`weight[x] = x / parent[x]`

During `find(x)`, we apply path compression to attach `x` directly to `root(x)` and multiply ratios along the path:
`weight[x] = (x / parent[x]) * (parent[x] / root) = x / root(x)`

---

### ⚡ The Consistency Invariant

When processing a new equation `A / B = value`:

1. Find roots and weights:
   • `root_a, weight_a = find(A)` (where `weight_a = A / root_a`)
   • `root_b, weight_b = find(B)` (where `weight_b = B / root_b`)

2. **If Already Connected (`root_a == root_b`)**:
   Both variables share the same root! The implied ratio is:
   `A / B = (A / root) / (B / root) = weight_a / weight_b`
   If `|weight_a / weight_b - value| >= 1e-5` ➡️ **Contradiction Detected!**

3. **If Disconnected (`root_a != root_b`)**:
   Merge `root_a` into `root_b` by setting:
   `parent[root_a] = root_b`
   `weight[root_a] = (value * weight_b) / weight_a`

---

### ⚖️ Algorithm Complexity

| Metric | Weighted DSU | Incremental BFS |
| :--- | :--- | :--- |
| **Time per Equation** | **O(α(V))** (Nearly O(1)) | **O(V + E)** (Graph search) |
| **Total Time** | **O(E * α(V))** | **O(E * (V + E))** |
| **Space** | **O(V)** | **O(V + E)** |

---

In Part 2, we explore **Online Stream Processing: Weighted DSU vs Graph BFS!**

Check out the implementation in the attached image! 📸

How do you handle transitive ratio constraints in your systems? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #GraphTheory #SystemDesign #CleanCode #Performance
