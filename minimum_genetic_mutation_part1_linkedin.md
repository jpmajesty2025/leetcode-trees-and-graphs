# Modeling Genetic Mutations as Implicit Graphs 🧬⚡

Given:
• A starting 8-character DNA sequence: `startGene`
• A target sequence: `endGene`
• A dictionary of valid intermediate mutations: `bank`

Each mutation changes exactly one nucleotide (`'A'`, `'C'`, `'G'`, `'T'`).

How do we find the shortest valid mutation sequence from start to end?

---

### 💡 The Implicit State Graph

This problem is a classic **unweighted shortest path problem** over an implicit state space:
• **Nodes**: 8-character gene strings.
• **Edges**: Transitions between two strings that differ by exactly 1 character (Hamming distance = 1), where the target exists in `bank`.
• **Objective**: Find the minimum edge path from `startGene` to `endGene`.

Whenever we need the shortest path on an unweighted graph, **Breadth-First Search (BFS)** is the gold standard!

---

### 🔍 Generating Next States: Word Scan vs Mutation Probe

How should we discover adjacent neighbors during BFS?

❌ **Option A: Full Bank Scan**
• Compare the current gene against every string in `bank`.
• Cost per node: `O(B * L)` (where B is bank size and L = 8).

✅ **Option B: Alphabet Mutation Probe (Optimal)**
• For each of the 8 positions, substitute the 3 other nucleotide choices (`'A'`, `'C'`, `'G'`, `'T'`).
• Generate exactly `8 * 3 = 24` candidate strings and check membership in a `bank_set` in `O(1)` time.
• Cost per node: `O(L * |Sigma|)` — constant and completely independent of bank size!

---

### ⚡ Level-Order BFS Workflow

1. Initialize `queue = deque([(startGene, 0)])` and `visited = {startGene}`.
2. If `endGene not in bank`, return -1 immediately.
3. Pop `(curr_gene, steps)`. If `curr_gene == endGene`, return `steps`.
4. Generate all 24 single-character mutations. For each valid, unvisited string in `bank`, mark visited and push to the queue with `steps + 1`.
5. If queue exhausts without reaching `endGene`, return -1.

---

### ⚖️ Complexity Analysis

| Metric | Level-Order BFS |
| :--- | :--- |
| **Time Complexity** | **O(B * L * |Sigma|)** where L = 8, |Sigma| = 4 |
| **Auxiliary Space** | **O(B * L)** for the visited set and queue |
| **Optimality** | **Guaranteed shortest path** |

---

In Part 2 tomorrow, we’ll explore how **Bidirectional BFS slashes the search tree exponentially from b^d to 2 * b^(d/2)!**

How do you optimize state transitions in implicit graph problems? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #GraphTheory #Bioinformatics #CleanCode
