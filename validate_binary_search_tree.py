'''
Given the root of a binary tree, determine if it is a valid BST.
'''

from typing import Optional, Union
from tree_node import TreeNode

def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """Determine if a binary tree is a valid Binary Search Tree (BST) using recursive DFS with range validation."""
    def dfs(node: Optional[TreeNode], small: Union[int, float], large: Union[int, float]) -> bool:
        if not node:
            return True

        if not (small < node.val < large):
            return False

        # Short-circuit: if left subtree is invalid, avoid evaluating right subtree
        return dfs(node.left, small, node.val) and dfs(node.right, node.val, large)

    return dfs(root, float("-inf"), float("inf"))