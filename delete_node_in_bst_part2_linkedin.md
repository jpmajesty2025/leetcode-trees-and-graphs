# BST Deletion: Iterative O(1) Splicing & Tree Degradation (Part 2 of 2) 🌲🧠

In Part 1, we broke down the three structural cases of BST node deletion (LeetCode 450). While the recursive approach with in-order successor swapping is elegant, examining iterative pointer splicing and long-term tree health reveals deep systems insights.

Let's dive deeper into BST surgery!

---

### 🔄 Successor vs. Predecessor Symmetry

In Case 3 (deleting a node with 2 children), we replaced the node with its **In-Order Successor** (minimum node in the right subtree).

However, the operation is completely symmetric:
- **In-Order Predecessor**: The maximum node in the left subtree (the rightmost leaf of `root.left`).
- It is strictly larger than all other nodes in the left subtree and smaller than all nodes in the right subtree.
- Replacing the target with either node is mathematically valid and preserves the BST property.

---

### ⚡ Iterative Deletion: Strictly O(1) Memory

To eliminate call-stack frames on deep trees, we can perform deletion iteratively using parent tracking:

1. **Descent**: Walk down the tree while tracking a `parent` pointer.
2. **Direct Splicing (0 or 1 Child)**: If the target has at most one child, reassign `parent.left` or `parent.right` to bypass the deleted node.
3. **Successor Splicing (2 Children)**:
   - Walk right once, then left to find the successor and its parent (`succ_parent`).
   - Overwrite the target's value with `succ.val`.
   - Unlink the successor by setting `succ_parent.left = succ.right` (or `succ_parent.right = succ.right`).

This reduces auxiliary memory from O(H) recursion stack frames down to strictly **O(1) constant space**.

---

### ⚠️ The Hibbard Deletion Problem: Long-Term Tree Skew

Here is a classic theoretical pitfall discovered by Thomas Hibbard in 1962:
- If a BST undergoes continuous random insertions and deletions where two-child deletions **always** replace with the right-subtree successor, tree balance systematically degrades.
- Right subtrees shrink faster than left subtrees, skewing the tree to the left and increasing average query height from O(log N) toward O(√N).
- *Solution*: Alternating between successor and predecessor replacements (or utilizing self-balancing trees like AVL or Red-Black Trees).

---

### 📊 Complexity Summary

- **Time: O(H)** (O(log N) balanced, O(N) skewed).
- **Auxiliary Space**:
  - **Recursive**: O(H) stack space.
  - **Iterative**: O(1) constant memory.

---

Do you prefer recursive or iterative pointer manipulation when modifying tree topologies?

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #BinarySearchTree #BST #PerformanceOptimization
