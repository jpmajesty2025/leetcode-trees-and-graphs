'''
Given the root of a binary search tree (BST) with duplicates, return all the mode(s) (i.e., 
the most frequently occurred element) in it.

This module implements an explicit stack-safe iterative approach.
'''

from tree_node import TreeNode


def find_mode_iterative(root: TreeNode | None) -> list[int]:
    """Find mode(s) in a BST using an explicit iterative stack."""
    if not root:
        return []

    stack: list[TreeNode] = []
    curr = root
    prev: int | None = None
    count = 0
    max_count = 0
    modes: list[int] = []

    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left

        curr = stack.pop()
        count = (count + 1) if (prev is not None and curr.val == prev) else 1

        if count > max_count:
            max_count = count
            modes = [curr.val]
        elif count == max_count:
            modes.append(curr.val)

        prev = curr.val
        curr = curr.right

    return modes


# Aliases
find_mode = find_mode_iterative
findMode = find_mode_iterative
