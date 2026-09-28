'''
Given the root of a Binary Search Tree (BST), return the minimum difference between the values of any two 
different nodes in the tree.

This module implements an explicit stack-safe iterative approach.
'''

from tree_node import TreeNode


def min_diff_in_bst_iterative(root: TreeNode | None) -> int:
    """Find minimum distance between BST nodes using an explicit iterative stack."""
    if not root:
        return 0

    stack: list[TreeNode] = []
    curr = root
    prev: int | None = None
    min_diff = float('inf')

    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left

        curr = stack.pop()
        if prev is not None:
            min_diff = min(min_diff, curr.val - prev)
        prev = curr.val
        curr = curr.right

    return int(min_diff) if min_diff != float('inf') else 0


# Aliases
min_diff_in_bst = min_diff_in_bst_iterative
minDiffInBST = min_diff_in_bst_iterative
