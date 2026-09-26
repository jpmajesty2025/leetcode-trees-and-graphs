'''
Given the root of a binary search tree and a target value, return the value in the BST 
that is closest to the target. If there are multiple answers, return the smallest.
'''

from typing import Optional
from tree_node import TreeNode


def closest_value_recursive(root: Optional[TreeNode], target: float) -> int:
    """Return the value in the BST closest to target using recursive search with tie-breaking."""
    if not root:
        return 0

    def helper(node: Optional[TreeNode], current_closest: int) -> int:
        if not node:
            return current_closest

        curr_diff = abs(node.val - target)
        closest_diff = abs(current_closest - target)

        if curr_diff < closest_diff or (curr_diff == closest_diff and node.val < current_closest):
            current_closest = node.val

        if target < node.val:
            return helper(node.left, current_closest)
        elif target > node.val:
            return helper(node.right, current_closest)
        else:
            return node.val

    return helper(root, root.val)


closest_value = closest_value_recursive
closestValue = closest_value_recursive
