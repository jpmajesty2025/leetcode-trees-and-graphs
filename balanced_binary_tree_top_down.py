'''
Given a binary tree, determine if it is height-balanced.

This module implements the naive top-down O(N^2) baseline approach.
'''

from tree_node import TreeNode


def is_balanced_top_down(root: TreeNode | None) -> bool:
    """Determine if a binary tree is height-balanced using top-down traversal (O(N^2) baseline)."""
    if not root:
        return True

    def get_height(node: TreeNode | None) -> int:
        if not node:
            return 0
        return max(get_height(node.left), get_height(node.right)) + 1

    left_h = get_height(root.left)
    right_h = get_height(root.right)

    return (
        abs(left_h - right_h) <= 1
        and is_balanced_top_down(root.left)
        and is_balanced_top_down(root.right)
    )


# Aliases
is_balanced = is_balanced_top_down
isBalanced = is_balanced_top_down
