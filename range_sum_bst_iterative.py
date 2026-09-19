'''
Given the root node of a binary search tree and two integers low and high, 
return the sum of values of all nodes with a value in the inclusive range [low, high].
'''

from typing import Optional, List
from tree_node import TreeNode


def range_sum_bst_iterative(root: Optional[TreeNode], low: int, high: int) -> int:
    """Return the sum of node values in [low, high] using iterative DFS with an explicit stack."""
    if not root:
        return 0

    stack: List[TreeNode] = [root]
    ans = 0

    while stack:
        node = stack.pop()
        if low <= node.val <= high:
            ans += node.val
        if node.left and low < node.val:
            stack.append(node.left)
        if node.right and node.val < high:
            stack.append(node.right)

    return ans
