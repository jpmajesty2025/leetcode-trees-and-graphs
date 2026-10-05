'''
Given the root of a binary tree, invert the tree, and return its root.

This module implements the explicit stack DFS approach.
'''

from tree_node import TreeNode


def invert_tree_dfs_iterative(root: TreeNode | None) -> TreeNode | None:
    """Invert a binary tree iteratively using an explicit stack."""
    if not root:
        return None

    stack: list[TreeNode] = [root]
    while stack:
        curr = stack.pop()
        curr.left, curr.right = curr.right, curr.left

        if curr.left:
            stack.append(curr.left)
        if curr.right:
            stack.append(curr.right)

    return root


# Aliases
invert_tree = invert_tree_dfs_iterative
invertTree = invert_tree_dfs_iterative
