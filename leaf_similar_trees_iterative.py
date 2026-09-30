'''
Consider all the leaves of a binary tree, from left to right order, the values of those leaves form a 
leaf value sequence.

Two binary trees are considered leaf-similar if their leaf value sequence is the same.

This module implements an explicit stack-safe iterative DFS approach.
'''

from tree_node import TreeNode


def leaf_similar_iterative(root1: TreeNode | None, root2: TreeNode | None) -> bool:
    """Compare leaf sequences using iterative stack DFS for complete stack safety."""
    def get_leaves_iterative(root: TreeNode | None) -> list[int]:
        if not root:
            return []
        leaves: list[int] = []
        stack: list[TreeNode] = [root]

        while stack:
            node = stack.pop()
            if not node.left and not node.right:
                leaves.append(node.val)
            # Push right before left so left is popped first (L-to-R)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return leaves

    return get_leaves_iterative(root1) == get_leaves_iterative(root2)


# Aliases
leaf_similar = leaf_similar_iterative
leafSimilar = leaf_similar_iterative
