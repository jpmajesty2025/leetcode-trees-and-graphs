'''
Given the root of a Binary Search Tree (BST), return the minimum absolute difference between the 
values of any two different nodes in the tree.
'''

from typing import Optional
from tree_node import TreeNode


def get_minimum_difference(root: Optional[TreeNode]) -> int:
    """Return the minimum absolute difference between any two nodes using in-order streaming."""
    prev: Optional[int] = None
    min_diff = float("inf")

    def inorder(node: Optional[TreeNode]) -> None:
        nonlocal prev, min_diff
        if not node:
            return

        inorder(node.left)

        if prev is not None:
            min_diff = min(min_diff, node.val - prev)
        prev = node.val

        inorder(node.right)

    inorder(root)
    return int(min_diff) if min_diff != float("inf") else 0


# LeetCode backward compatibility aliases
getMinimumDifference = get_minimum_difference
min_diff_in_bst = get_minimum_difference
