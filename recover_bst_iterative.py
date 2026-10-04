'''
You are given the root of a binary search tree (BST), where the values of exactly two nodes of the 
tree were swapped by mistake.

This module implements the iterative stack in-order traversal approach.
'''

from tree_node import TreeNode


def recover_tree_iterative(root: TreeNode | None) -> None:
    """Recover swapped BST using iterative stack-based in-order traversal."""
    stack: list[TreeNode] = []
    curr = root
    first: TreeNode | None = None
    second: TreeNode | None = None
    prev: TreeNode | None = None

    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left

        curr = stack.pop()
        if prev and prev.val > curr.val:
            if first is None:
                first = prev
            second = curr
        prev = curr
        curr = curr.right

    if first and second:
        first.val, second.val = second.val, first.val


# Aliases
recover_tree = recover_tree_iterative
recoverTree = recover_tree_iterative
