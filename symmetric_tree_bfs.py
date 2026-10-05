'''
Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric 
around its center).

This module implements the iterative queue BFS pair verification approach.
'''

from collections import deque
from tree_node import TreeNode


def is_symmetric_bfs(root: TreeNode | None) -> bool:
    """Check if a binary tree is symmetric using iterative BFS pair verification."""
    if not root:
        return True

    queue: deque[tuple[TreeNode | None, TreeNode | None]] = deque(
        [(root.left, root.right)]
    )

    while queue:
        t1, t2 = queue.popleft()

        if not t1 and not t2:
            continue
        if not t1 or not t2 or t1.val != t2.val:
            return False

        queue.append((t1.left, t2.right))
        queue.append((t1.right, t2.left))

    return True


# Aliases
is_symmetric = is_symmetric_bfs
isSymmetric = is_symmetric_bfs
