# Deleting Nodes in a BST: The Three Structural Cases (Part 1 of 2) 🌲✂️

Inserting and searching in a Binary Search Tree (BST) are straightforward, but **node deletion** requires structural tree manipulation.

How do you remove a node without violating the BST invariant? Let's break down the three fundamental deletion cases!

---

### 💡 The Problem & Two-Stage Mental Model

Deleting a node consists of two distinct phases:
1. **Search Phase**: Route down the tree using BST comparisons until locating the target node with `key`.
2. **Deletion Phase**: Remove the target node while preserving BST ordering across all remaining nodes.

Once the target node is found, the surgery depends entirely on the node's number of children.

---

### ⚙️ The Three Structural Deletion Cases

#### Case 1: Node is a Leaf (0 Children)
The easiest case. The node has no subtrees to maintain. We simply return `None` (or unlink the parent's pointer) to snip the leaf off the tree.

#### Case 2: Node has Exactly 1 Child
If the node has only a left or right child, we bypass the deleted node completely. We promote the existing child to take the target's place by returning `root.left` or `root.right` directly to the parent pointer.

#### Case 3: Node has 2 Children (The Successor Replacement)
When a node has two subtrees, we cannot simply delete it without breaking the tree. 
- We must find a replacement value that is strictly greater than all nodes in the left subtree and strictly smaller than all other nodes in the right subtree.
- **The In-Order Successor**: The smallest node in the right subtree (the leftmost leaf of `root.right`).
- **The Swap**: Copy the successor's value into the target node, then recursively delete the successor from the right subtree. Because the successor is guaranteed to have at most one child, its deletion falls trivially into Case 1 or Case 2!

---

### 📊 Complexity Profile

- **Time Complexity: O(H)** — Where H is tree height (O(log N) for balanced trees, O(N) for skewed trees). Finding the node and finding its successor both follow a single branch descent.
- **Auxiliary Space: O(H)** — Call stack overhead during recursive descent.

---

### 🧠 Key Engineering Takeaway

Breaking complex graph/tree mutations into clear structural cases (0, 1, or 2 children) simplifies edge-case handling and prevents broken pointers.

👉 **In Part 2**, we'll explore **Iterative O(1) space deletion, in-order predecessor alternatives, and tree balance degradation**!

Do you prefer using in-order successors or predecessors when deleting nodes?

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #BinarySearchTree #BST #TreeAlgorithms #PerformanceOptimization
