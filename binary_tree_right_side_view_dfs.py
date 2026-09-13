'''
Given the root of a binary tree, imagine yourself standing on the right side of it, 
return the values of the nodes you can see ordered from top to bottom.
'''

from typing import Optional, List
from tree_node import TreeNode


def right_side_view_dfs(root: Optional[TreeNode]) -> List[int]:
    """Return the right-side view of a binary tree using right-to-left recursive DFS."""
    result = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if not node:
            return

        if depth == len(result):
            result.append(node.val)

        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)

    dfs(root, 0)
    return result
