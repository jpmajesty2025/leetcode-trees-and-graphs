# Directed Graphs & Degree Scoring: Finding the Town Judge (Part 1 of 2) 🌐⚖️

Graph theory problems often look like social relationship puzzles on the surface. "Find the Town Judge" is a great example of translating human trust rules into directed graph degrees.

Let's break down the mathematical invariants and the optimal single-array net degree score!

---

### 💡 The Problem & Graph Modeling

In a town of `n` people labeled 1 to `n`, there is a rumor that one person is secretly the town judge.
If the judge exists:
1. The judge trusts nobody (`out-degree = 0`).
2. Everybody else trusts the judge (`in-degree = n - 1`).
3. There is exactly one such person.

We can model this town as a **directed graph**:
- Each person is a vertex `V`.
- Each trust relationship `[a, b]` is a directed edge `a → b` (where `a` trusts `b`).

---

### ⚙️ The Net Score Optimization: Merging In-Degree & Out-Degree

A standard approach uses two arrays: `in_degree` and `out_degree`. Can we do it with a single array?

Yes! Notice the algebraic property:
- Every time person `a` trusts someone, their likelihood of being the judge drops to zero (`out-degree > 0`).
- Every time person `b` is trusted, their candidacy increases (`in-degree + 1`).

By maintaining a single array `net_scores` where `net_scores[i] = in_degree[i] - out_degree[i]`:
- The town judge will have a net score of exactly `(n - 1) - 0 = n - 1`.
- Any non-judge who trusts the judge has `out-degree >= 1` and `in-degree <= n - 2`, meaning their net score is at most `(n - 2) - 1 = n - 3`.
- Thus, the score `n - 1` is mathematically unique to the judge!

---

### ⚡ Early-Exit Optimization: Edge Pruning

If `len(trust) < n - 1`, a valid judge is impossible because there are not enough trust edges in the entire town for any candidate to receive `n - 1` endorsements. We can return `-1` in O(1) time before even creating arrays.

---

### 📊 Complexity Profile

- **Time Complexity: O(E + N)** — Where E is the number of trust relationships and N is the population. We iterate through the trust array once and scan the scores once.
- **Auxiliary Space: O(N)** — A single integer array of size N + 1.

---

### 🧠 Key Engineering Takeaway

Translating relationship rules into algebraic invariants (`in_degree - out_degree = n - 1`) compresses two state arrays into one, halving heap allocation and improving CPU cache locality.

👉 **In Part 2**, we'll explore **Universal Graph Sinks, PageRank connections, and distributed trust networks**!

How do you model unidirectional trust relationships in your graph services?

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #GraphTheory #DirectedGraphs #PerformanceOptimization
