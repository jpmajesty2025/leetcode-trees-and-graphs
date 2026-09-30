'''
Consider all the leaves of a binary tree, from left to right order, the values of those leaves form a 
leaf value sequence.

Two binary trees are considered leaf-similar if their leaf value sequence is the same.

This module implements the classic recursive leaf collection approach.
'''

from tree_node import TreeNode


def leaf_similar_recursive(root1: TreeNode | None, root2: TreeNode | None) -> bool:
    """Compare leaf sequences by collecting leaves into lists using recursive DFS."""
    def get_leaves(node: TreeNode | None, leaves: list[int]) -> None:
        if not node:
            return
        if not node.left and not node.right:
            leaves.append(node.val)
            return
        get_leaves(node.left, leaves)
        get_leaves(node.right, leaves)

    leaves1: list[int] = []
    leaves2: list[int] = []
    get_leaves(root1, leaves1)
    get_leaves(root2, leaves2)
    return leaves1 == leaves2


# Aliases
leaf_similar = leaf_similar_recursive
leafSimilar = leaf_similar_recursive
