'''
Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. 
(i.e., from left to right, then right to left for the next level and alternate between).
'''

from collections import deque
from typing import Optional, List, Tuple
from tree_node import TreeNode

# Recursive DFS implementation
def zigzag_level_order_dfs(root: Optional[TreeNode]) -> List[List[int]]:
    """Return zigzag level order traversal using recursive DFS."""
    result: List[deque[int]] = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if not node:
            return

        if depth == len(result):
            result.append(deque())

        if depth % 2 == 0:
            result[depth].append(node.val)
        else:
            result[depth].appendleft(node.val)

        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return [list(level) for level in result]


# Iterative DFS implementation
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