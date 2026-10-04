# Dual-Frontier Bridging vs Multi-Source BFS: Two-Period Graph Search 💱🧙‍♂️

In Part 1, we saw how maximizing two-period currency conversions requires evaluating every reachable intermediate bridge currency C.

*What are the cleanest architectural patterns to compose multi-stage graph transitions in Python?*

Let's compare two elegant approaches: **Dual-Frontier Ratio Bridging** vs. **Multi-Source BFS**.

---

### 💡 Pattern 1: Dual-Frontier Ratio Bridging

Since exchange rates are reversible (A -> B at rate r means B -> A at rate 1/r):
• Converting C -> initialCurrency on Day 2 is the exact reciprocal of initialCurrency -> C on Day 2:
  `Day2_Rate(C -> initialCurrency) = 1 / Day2_Rate(initialCurrency -> C)`

This enables running **the exact same BFS helper twice**:
1. `day1_rates = get_rates(initialCurrency, pairs1, rates1)`
2. `day2_rates = get_rates(initialCurrency, pairs2, rates2)`
3. For each currency C in both days:
   `final_amount = day1_rates[C] / day2_rates[C]`

**Why it shines**: Reuses a single pure traversal function with zero code duplication!

---

### 💡 Pattern 2: Multi-Source Day 2 BFS

Instead of running two independent searches:
1. Run Day 1 BFS from `initialCurrency` to produce overnight balances: `day1_balances`.
2. **Directly seed the Day 2 BFS queue** with all `(currency, balance)` pairs from Day 1!
3. Propagate balances across Day 2 edges.
4. Read `day2_balances[initialCurrency]`.

**Why it shines**: Directly models the physical flow of capital across temporal stages.

---

### 📊 Architectural Comparison

| Dimension | Dual-Frontier Ratio Bridging | Multi-Source BFS Seeding |
| :--- | :--- | :--- |
| **Code Reusability** | High (Single 1-to-All helper) | Medium (Sequential pipeline) |
| **Edge Requirement** | Requires bidirectional Day 2 edges | Works even on directed Day 2 edges |
| **Time Complexity** | O(V1 + E1 + V2 + E2) | O(V1 + E1 + V2 + E2) |
| **Auxiliary Memory** | 2 dictionary maps | 2 dictionary maps |

---

### 🎯 Key Engineering Takeaways

• **Decouple Multi-Period States**: Splitting multi-stage optimization into independent per-period traversals prevents state explosion.
• **Exploit Invertibility**: When graph transitions are reversible, computing paths to a common origin simplifies cross-stage reconciliation.

How do you handle multi-stage transitions in your algorithmic pipelines? Let's discuss below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #SystemDesign #CleanCode
