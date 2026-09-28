'''
Given the root of a binary tree, return the inorder traversal of its nodes' values.

This module implements Recursive DFS Inorder Traversal.
'''

from tree_node import TreeNode


def inorder_traversal_recursive(root: TreeNode | None) -> list[int]:
    """Perform an inorder traversal using recursive DFS."""
    result: list[int] = []

    def dfs(node: TreeNode | None) -> None:
        if not node:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)

    dfs(root)
    return result


# Aliases
inorder_traversal = inorder_traversal_recursive
inorderTraversal = inorder_traversal_recursive
