'''
Given the root of a binary search tree and a target value, return the value in the BST 
that is closest to the target. If there are multiple answers, return the smallest.
'''

from typing import Optional
from tree_node import TreeNode


def closest_value(root: Optional[TreeNode], target: float) -> int:
    """Return the value in the BST closest to target using an iterative O(1) space search.
    
    If there are multiple answers with identical distance, returns the smaller value.
    """
    if not root:
        return 0

    closest = root.val
    current: Optional[TreeNode] = root

    while current:
        curr_diff = abs(current.val - target)
        closest_diff = abs(closest - target)

        # Update if closer, or if equidistant and current value is smaller (tie-breaking rule)
        if curr_diff < closest_diff or (curr_diff == closest_diff and current.val < closest):
            closest = current.val

        if target < current.val:
            current = current.left
        elif target > current.val:
            current = current.right
        else:
            # Exact match found: distance is 0, cannot do better
            return current.val

    return closest
