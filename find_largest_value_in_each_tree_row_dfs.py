'''
Given the root of a binary tree, return an array of the largest value in each row of the tree (0-indexed).
'''

from typing import Optional, List
from tree_node import TreeNode


def largest_values_dfs(root: Optional[TreeNode]) -> List[int]:
    """Return the largest value in each row of a binary tree using recursive DFS."""
    result: List[int] = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if not node:
            return

        if depth == len(result):
            result.append(node.val)
        else:
            result[depth] = max(result[depth], node.val)

        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return result
