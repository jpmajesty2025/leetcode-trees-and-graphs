'''
You are given the root of a binary search tree (BST), where the values of exactly two nodes of the 
tree were swapped by mistake.

This module implements the clean recursive in-order traversal approach.
'''

from tree_node import TreeNode


def recover_tree_recursive(root: TreeNode | None) -> None:
    """Recover swapped BST using clean recursive in-order DFS."""
    first: TreeNode | None = None
    second: TreeNode | None = None
    prev: TreeNode | None = None

    def inorder(node: TreeNode | None) -> None:
        nonlocal first, second, prev
        if not node:
            return
        inorder(node.left)
        if prev and prev.val > node.val:
            if first is None:
                first = prev
            second = node
        prev = node
        inorder(node.right)

    inorder(root)
    if first and second:
        first.val, second.val = second.val, first.val


# Aliases
recover_tree = recover_tree_recursive
recoverTree = recover_tree_recursive
