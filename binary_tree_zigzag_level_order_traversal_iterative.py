'''
Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. 
(i.e., from left to right, then right to left for the next level and alternate between).
'''

from collections import deque
from typing import Optional, List, Tuple
from tree_node import TreeNode


def zigzag_level_order_iterative(root: Optional[TreeNode]) -> List[List[int]]:
    """Return zigzag level order traversal using iterative DFS with an explicit stack."""
    if not root:
        return []

    result: List[deque[int]] = []
    stack: List[Tuple[TreeNode, int]] = [(root, 0)]

    while stack:
        node, depth = stack.pop()

        if depth == len(result):
            result.append(deque())

        if depth % 2 == 0:
            result[depth].append(node.val)
        else:
            result[depth].appendleft(node.val)

        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))

    return [list(level) for level in result]
