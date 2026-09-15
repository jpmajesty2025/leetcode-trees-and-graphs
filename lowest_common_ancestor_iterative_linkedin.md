# Mastering Binary Trees (Part 2): Recursion-Proof LCA with Parent Pointers 🛡️🌲

In **Part 1**, we looked at the elegant recursive solution for finding the **Lowest Common Ancestor (LCA)**.

To be sure, it's clean. However, some languages - Python C, C++, Java - do not implement Tail Call Recursion (TCO) and impose rigid call stack limits. In these cases, recursive DFS has a potential dark side that you need to consider: deep skewed trees can exceed the recursion limit and crash with `RecursionError`. Note that some languages are less vulnerable and some are designed for recursion and support native TCO.

But if you need to make an LCA implementation **stack-safe** and **production-ready**, how do you do it? We've seen the underlying idea before: use an iterative algorithm with an explicit stack.

---

### 💡 The Solution: Iterative Parent Mapping + Path Intersection

Instead of holding state in function stack frames, we can simulate the search using an explicit stack on the heap and map parent references:

1. **Map Parents with Early Stopping:** Traverse the tree with an explicit stack, recording `parent_map[child] = parent` until *both* target nodes `p` and `q` are found.
2. **Trace Ancestors of `p`:** Walk upwards from `p` to the root, adding each ancestor into a hash set.
3. **Find the Intersection with `q`:** Walk upwards from `q` to the root. The very first node encountered that is already in `p`'s ancestor set is their **LCA**!

```python
from typing import Optional, Dict, Set, List
from tree_node import TreeNode


def lowest_common_ancestor_iterative(
    root: Optional[TreeNode], p: Optional[TreeNode], q: Optional[TreeNode]
) -> Optional[TreeNode]:
    """Find LCA using iterative parent mapping and ancestor path intersection."""
    if not root or not p or not q:
        return None

    parent_map: Dict[TreeNode, Optional[TreeNode]] = {root: None}
    stack: List[TreeNode] = [root]

    # Early stopping: Traverse only until both p and q are discovered
    while stack and (p not in parent_map or q not in parent_map):
        node = stack.pop()
        if node.left:
            parent_map[node.left] = node
            stack.append(node.left)
        if node.right:
            parent_map[node.right] = node
            stack.append(node.right)

    if p not in parent_map or q not in parent_map:
        return None

    # Step 1: Collect ancestors of p
    ancestors_of_p: Set[TreeNode] = set()
    curr: Optional[TreeNode] = p
    while curr:
        ancestors_of_p.add(curr)
        curr = parent_map[curr]

    # Step 2: First common ancestor for q is the LCA
    curr = q
    while curr not in ancestors_of_p:
        curr = parent_map[curr]

    return curr
```

### 🚀 Engineering Highlights
- **Stack-Overflow Immune:** Your state lives on the heap, safely handling trees of any height, bounded only by your RAM. Recursion may crumble with only 1000 or so nodes; a heap stack handles several orders of magnitude more.
- **Early Exit:** Stops traversal the instant both $p$ and $q$ are discovered, without exploring the rest of the tree.

Which approach do you default to in interviews vs. production code?

#LearningInPublic #Python #DataStructures #Algorithms #LeetCode #SoftwareEngineering #SystemDesign #CleanCode
