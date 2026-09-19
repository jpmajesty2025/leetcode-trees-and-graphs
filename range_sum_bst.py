'''
Given the root node of a binary search tree and two integers low and high, 
return the sum of values of all nodes with a value in the inclusive range [low, high].
'''

from typing import Optional
from tree_node import TreeNode


def range_sum_bst(root: Optional[TreeNode], low: int, high: int) -> int:
    """Return the sum of node values in [low, high] using recursive BST pruning."""
    if not root:
        return 0

    ans = 0
    if low <= root.val <= high:
        ans += root.val
    if low < root.val:
        ans += range_sum_bst(root.left, low, high)
    if root.val < high:
        ans += range_sum_bst(root.right, low, high)

    return ans
