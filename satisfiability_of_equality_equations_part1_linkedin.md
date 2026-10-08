# Equivalence Relations & 2-Pass Union-Find: Equations (Part 1 of 2) ⚖️🔗

Can a set of equality and inequality constraints be satisfied simultaneously?

In "Satisfiability of Equality Equations", we are given equations like `"a==b"` and `"b!=a"`. We must determine whether an integer assignment exists that satisfies all equations.

Let's explore algebraic equivalence classes and the 2-pass Union-Find approach!

---

### 💡 The Mathematical Foundation: Equivalence Relations

In mathematics, equality (`==`) satisfies three axioms:
1. **Reflexivity**: `a == a`
2. **Symmetry**: `a == b ⇔ b == a`
3. **Transitivity**: `a == b ∧ b == c ⇒ a == c`

Relations satisfying these axioms partition variables into **disjoint equivalence classes**. 

This maps directly to **Disjoint Set Union (DSU / Union-Find)**:
- Connected components represent variables that must share the same value.
- Inequalities (`!=`) act as constraints prohibiting two variables from sharing a component.

---

### ⚙️ The 2-Pass Union-Find Strategy

Because equality constraints are constructive while inequalities validate, we solve the problem in two passes:

1. **Pass 1: Construct Components (`==`)**
   - Iterate over all `"=="` equations.
   - For every `a == b`, call `union(a, b)`.
   - Transitive chains automatically merge into the same component.

2. **Pass 2: Validate Invariants (`!=`)**
   - Iterate over all `"!="` equations.
   - For every `a != b`, check `if find(a) == find(b)`.
   - If they share the same root, they belong to the same component — a contradiction! Return `False`.

If all checks pass, return `True`.

---

### 🚀 Optimization: Fixed Array vs. Hash Map

Because variables are restricted to 26 lowercase English letters (`'a'` to `'z'`), a flat array `parent = list(range(26))` eliminates hash table lookups, resizing, and allocations.

---

### 📊 Complexity Profile

- **Time: O(N * α(26)) = O(N)** — Linear time, where α is Inverse Ackermann.
- **Space: O(1)** — A fixed 26-element array.

---

👉 **In Part 2**, we will explore **SMT Solvers, Type Inference, and Pointer Alias Analysis**!

How do you model constraint satisfaction in your validation engines?

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #UnionFind #CleanCode #PerformanceOptimization
