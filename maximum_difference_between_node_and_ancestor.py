'''
Given the root of a binary tree, find the maximum value v for which there exist different nodes a and b where 
v = |a.val - b.val| and a is an ancestor of b.

A node a is an ancestor of b if either: any child of a is equal to b or any child of a is an ancestor of b.
'''

from typing import Optional
from tree_node import TreeNode


def max_ancestor_diff(root: Optional[TreeNode]) -> int:
    """Find the maximum difference |a.val - b.val| between ancestor a and descendant b using recursive DFS."""
    if not root:
        return 0

    def dfs(node: Optional[TreeNode], cur_min: int, cur_max: int) -> int:
        if not node:
            return cur_max - cur_min

        cur_min = min(cur_min, node.val)
        cur_max = max(cur_max, node.val)

        left_diff = dfs(node.left, cur_min, cur_max)
        right_diff = dfs(node.right, cur_min, cur_max)

        return max(left_diff, right_diff)

    return dfs(root, root.val, root.val)
