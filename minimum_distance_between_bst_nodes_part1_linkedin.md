# BST Min Distance: The Hidden O(N²) List Concatenation Trap 🌲🔍

When finding the minimum distance between any two nodes in a Binary Search Tree (LeetCode 783 / 530), we know the BST invariant guarantees that an **in-order traversal** visits nodes in strictly ascending order.

To collect values, a common recursive pattern is written:
```python
# ❌ HIDDEN BOTTLENECK: List concatenation at each node
def inorder(node):
    if not node: return []
    return inorder(node.left) + [node.val] + inorder(node.right)
```

It looks harmless in a one-liner, but examine what happens under the hood:

---

### 🚨 The Hidden $\mathcal{O}(N^2)$ Time & Memory Churn

1️⃣ **Repeated Sub-Array Copying**: Concatenating lists with `+` allocates a brand new list and copies all elements from subtrees at every recursive step. On skewed trees, list copying takes $1 + 2 + \dots + N = \mathbf{O(N^2)}$ **time**!
2️⃣ **Two-Pass Overhead**: Storing all $N$ values into an array requires an entire second loop (`for i in range(1, len(values))`) to find the minimum difference, consuming $\mathcal{O}(N)$ heap memory.

---

### 💡 The Fix: Single-Pass Streaming with a `prev` Pointer

Instead of collecting elements into an array, track only the immediately preceding in-order value with a single `prev` variable:

```python
def min_diff_in_bst(root: TreeNode | None) -> int:
    prev = None
    min_diff = float('inf')

    def inorder(node):
        nonlocal prev, min_diff
        if not node: return

        inorder(node.left)

        # On-the-fly streaming difference
        if prev is not None:
            min_diff = min(min_diff, node.val - prev)
        prev = node.val

        inorder(node.right)

    inorder(root)
    return min_diff
```

• **Single Pass**: Zero list allocations, strictly $\mathcal{O}(N)$ runtime.
• **Iterative Alternative**: Uses an explicit `stack = []` for $100\%$ stack safety on deep trees.

---

### ⚖️ Traversal Trade-Offs

| Approach | Time Complexity | Auxiliary Space | Passes Over Data |
| :--- | :--- | :--- | :--- |
| **List Concatenation (`+`)** | $\mathcal{O}(N^2)$ worst-case | $\mathcal{O}(N)$ array allocation | 2 passes |
| **Streaming DFS with `prev`** | $\mathcal{O}(N)$ (Optimal) | $\mathcal{O}(H)$ call stack | **1 single pass** |
| **Iterative Stack with `prev`**| $\mathcal{O}(N)$ (Optimal) | $\mathcal{O}(H)$ heap stack | **1 single pass (Stack-Safe)** |

---

Check out the clean implementations in the attached snippet! 📸

In Part 2 tomorrow, we’ll explore how **Morris Traversal** calculates BST node distances in **$\mathcal{O}(1)$ auxiliary space without any stack or recursion!**

Do you stream state during in-order traversal or collect into an array first? Let's discuss below! 👇

#Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #CleanCode #ComputerScience
