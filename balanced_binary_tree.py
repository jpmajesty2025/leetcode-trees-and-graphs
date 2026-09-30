'''
Given a binary tree, determine if it is height-balanced.

A height-balanced binary tree is defined as a binary tree in which the depth of the two subtrees 
of every node never differs by more than one.
'''

from tree_node import TreeNode


def is_balanced(root: TreeNode | None) -> bool:
    """Determine if a binary tree is height-balanced using bottom-up DFS with short-circuiting."""
    def check_height(node: TreeNode | None) -> int:
        if not node:
            return 0

        left = check_height(node.left)
        if left == -1:
            return -1  # Early exit: left subtree is already unbalanced

        right = check_height(node.right)
        if right == -1 or abs(left - right) > 1:
            return -1

        return max(left, right) + 1

    return check_height(root) != -1


# LeetCode backward compatibility aliases
is_balanced_dfs = is_balanced
isBalanced = is_balanced
