'''
Given the root of a Binary Search Tree (BST), return the minimum absolute difference between the 
values of any two different nodes in the tree.

This module implements Morris In-Order Traversal achieving strictly O(1) auxiliary memory.
'''

from typing import Optional
from tree_node import TreeNode


def get_minimum_difference_morris(root: Optional[TreeNode]) -> int:
    """Find minimum difference in BST in O(1) extra space using Morris Traversal."""
    curr = root
    prev: Optional[int] = None
    min_diff = float("inf")

    while curr:
        if not curr.left:
            if prev is not None:
                min_diff = min(min_diff, curr.val - prev)
            prev = curr.val
            curr = curr.right
        else:
            # Find in-order predecessor
            pred = curr.left
            while pred.right and pred.right is not curr:
                pred = pred.right

            if not pred.right:
                # Create temporary thread back to curr
                pred.right = curr
                curr = curr.left
            else:
                # Thread already exists; break thread and visit curr
                pred.right = None
                if prev is not None:
                    min_diff = min(min_diff, curr.val - prev)
                prev = curr.val
                curr = curr.right

    return int(min_diff) if min_diff != float("inf") else 0


# Aliases
get_minimum_difference = get_minimum_difference_morris
getMinimumDifference = get_minimum_difference_morris
