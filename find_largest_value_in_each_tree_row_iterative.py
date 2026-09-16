'''
Given the root of a binary tree, return an array of the largest value in each row of the tree (0-indexed).
'''

from typing import Optional, List
from tree_node import TreeNode


def largest_values_iterative(root: Optional[TreeNode]) -> List[int]:
    """Return the largest value in each row of a binary tree using iterative DFS with an explicit stack."""
    if not root:
        return []

    result: List[int] = []
    stack = [(root, 0)]

    while stack:
        node, depth = stack.pop()

        if depth == len(result):
            result.append(node.val)
        else:
            result[depth] = max(result[depth], node.val)

        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))

    return result
