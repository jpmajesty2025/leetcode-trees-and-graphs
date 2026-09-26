'''
Given the root of a Binary Search Tree (BST), return the minimum absolute difference between the 
values of any two different nodes in the tree.
'''

from typing import Optional, List
from tree_node import TreeNode


def get_minimum_difference_iterative(root: Optional[TreeNode]) -> int:
    """Return the minimum absolute difference between any two nodes using iterative in-order traversal."""
    if not root:
        return 0

    stack: List[TreeNode] = []
    curr: Optional[TreeNode] = root
    prev: Optional[int] = None
    min_diff = float("inf")

    while stack or curr:
        if curr:
            stack.append(curr)
            curr = curr.left
        else:
            curr = stack.pop()
            if prev is not None:
                min_diff = min(min_diff, curr.val - prev)
            prev = curr.val
            curr = curr.right

    return int(min_diff) if min_diff != float("inf") else 0
