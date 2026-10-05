# Collecting All Valid Paths: Backtracking Invariants in Binary Trees 🌲🛤️

We are given the root of a binary tree and an integer `targetSum`.

Unlike Path Sum I (a boolean reachability query), here we must return **all root-to-leaf paths** whose node values sum exactly to `targetSum`:

```
          5
         / \
        4   8
       /   / \
      11  13  4
     /  \    / \
    7    2  5   1

Target Sum = 22
Valid Paths: [5, 4, 11, 2], [5, 8, 4, 5]
```

How do we collect qualifying paths without massive memory allocation overhead?

---

### 🚨 The Naive List Copying Trap

A common pattern is creating a new list on every recursive call:
```python
# ❌ Allocates a fresh list copy at every single node!
dfs(node.left, path + [node.val])
dfs(node.right, path + [node.val])
```

For a tree with `N` nodes and height `H`, copying `path + [node.val]` allocates `O(N * H)` heap objects, triggering heavy Garbage Collection (GC) pressure.

---

### 💡 The Shared Backtracking Stack

Instead of cloning lists on every branch, maintain a **single shared mutable list** (`current_path`) and backtrack:

1. **Enter Node**: Append `node.val` and subtract from `remaining`.
2. **Leaf Match**: If `not node.left and not node.right and remaining == 0`, snapshot a copy: `result.append(list(current_path))`.
3. **Explore Children**: Recurse down `left` and `right`.
4. **Exit Node (Backtrack)**: `current_path.pop()` to restore state for sibling subtrees!

---

### ⚡ Clean Pythonic Backtracking

```python
def path_sum(root: TreeNode | None, target_sum: int) -> list[list[int]]:
    result: list[list[int]] = []
    current_path: list[int] = []

    def dfs(node: TreeNode | None, remaining: int) -> None:
        if not node:
            return

        current_path.append(node.val)
        remaining -= node.val

        if not node.left and not node.right and remaining == 0:
            result.append(list(current_path))  # Snapshot only valid paths!
        else:
            dfs(node.left, remaining)
            dfs(node.right, remaining)

        current_path.pop()  # Backtrack

    dfs(root, target_sum)
    return result
```

---

### ⚖️ Algorithm Complexity

| Metric | Shared Stack Backtracking DFS | Naive List Copying DFS |
| :--- | :--- | :--- |
| **Time Complexity** | **O(N + K * H)** | **O(N * H)** |
| **Active Auxiliary Space** | **O(H)** (One list of size H) | **O(N * H)** (Copied at every node) |
| **Output Space** | **O(K * H)** (K = valid paths) | **O(K * H)** |

---

In Part 2 tomorrow, we’ll explore **Memory Allocation Profiles: Backtracking DFS vs Queue BFS!**

How do you optimize state snapshots in your recursive backtracking algorithms? Let's discuss below! 👇

#LearningInPublic #Python #SoftwareEngineering #DataStructures #Algorithms #LeetCode #TreeTraversals #CleanCode #Recursion #Performance
