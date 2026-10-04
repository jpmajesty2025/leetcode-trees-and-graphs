# Maximize Currency Conversions: Two-Stage Graph Arbitrage 💱🚀

We start with 1.0 of `initialCurrency`. We are given two independent sets of currency conversion pairs:
• Day 1 pairs & rates (`pairs1`, `rates1`)
• Day 2 pairs & rates (`pairs2`,`rates2`)

We can make any sequence of conversions on Day 1, hold any currency overnight, and convert back to `initialCurrency` on Day 2.

How do we find the optimal sequence of conversions to maximize our final balance?

---

### 🚨 The Single-Currency Trap

A common mistake is trying to pick a single "best" currency on Day 1:
1. Run Day 1 traversal to maximize one target currency.
2. Start Day 2 with that currency.

How this fails:
• A currency with a modest Day 1 conversion rate might have an extraordinary return rate on Day 2!
• The optimal strategy requires checking **every reachable intermediate currency bridge C**:
  `final_amount(C) = Day1_Rate(initial -> C) * Day2_Rate(C -> initial)`

---

### 💡 Two-Stage BFS Graph Composition

Since exchange rates are reversible (A -> B at rate r implies B -> A at rate 1/r), each day forms a connected graph.

1️⃣ **Day 1 Exploration**:
• Run BFS from `initialCurrency` with amount 1.0.
• Record the maximum reachable balance for every currency: `day1_balances[C]`.

2️⃣ **Day 2 Return Path**:
• For every currency C held overnight, find the maximum conversion rate back to `initialCurrency` on Day 2.
• Calculate total final return:
  `total = day1_balances[C] * Day2_Rate(C -> initialCurrency)`

3️⃣ **Max Frontier Selection**:
• Take `max(1.0, max(total for all C))`. If no conversion beats holding our initial 1.0 balance, we simply make zero conversions!

---

### ⚖️ Graph Composition Overview

| Step | Operation | Time Complexity |
| :--- | :--- | :--- |
| **Day 1 Traversal** | BFS from initialCurrency | O(V1 + E1) |
| **Day 2 Traversal** | BFS from initialCurrency | O(V2 + E2) |
| **Frontier Merging** | Intersect Day 1 & Day 2 maps | O(min(V1, V2)) |
| **Total System** | Linear two-pass graph search | **O(V + E) Optimal** |

---

In Part 2 tomorrow, we’ll contrast **Dual-Frontier Bridging vs. Multi-Source BFS!**

How do you model multi-period financial transitions in graph systems? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #GraphTheory #SystemDesign #CleanCode
