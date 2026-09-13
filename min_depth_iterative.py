'''
Given a binary tree, find its minimum depth.

Iterative Depth-First Search (Stack) approach.
'''

from typing import Optional, List, Tuple
from tree_node import TreeNode


def min_depth_iterative(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    stack: List[Tuple[TreeNode, int]] = [(root, 1)]
    min_d = float('inf')

    while stack:
        node, depth = stack.pop()

        if not node.left and not node.right:
            min_d = min(min_d, depth)
            continue

        # Prune branches that are already deeper than the current minimum found
        if depth >= min_d:
            continue

        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))

    return int(min_d)
