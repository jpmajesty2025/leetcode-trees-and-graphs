'''
Given the root of a binary tree, return the length of the diameter of the tree.

The diameter of a binary tree is the length of the longest path between any two nodes in a tree. 
This path may or may not pass through the root.

The length of a path between two nodes is represented by the number of edges between them.
'''

from typing import Optional, Tuple
from tree_node import TreeNode


def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    """Find the diameter of a binary tree using pure functional recursion."""
    def dfs(node: Optional[TreeNode]) -> Tuple[int, int]:
        if not node:
            return 0, 0  # (depth, diameter)

        left_depth, left_diam = dfs(node.left)
        right_depth, right_diam = dfs(node.right)

        current_depth = max(left_depth, right_depth) + 1
        current_diam = max(left_diam, right_diam, left_depth + right_depth)

        return current_depth, current_diam

    return dfs(root)[1]
