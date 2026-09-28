'''
Given the root of a binary tree, return the inorder traversal of its nodes' values.
'''

from tree_node import TreeNode


def inorder_traversal(root: TreeNode | None) -> list[int]:
    """Perform an inorder traversal of a binary tree using an iterative approach with a stack."""
    result: list[int] = []
    stack: list[TreeNode] = []
    current = root

    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.val)
        current = current.right

    return result


# LeetCode backward compatibility aliases
inorder_traversal_iterative = inorder_traversal
inorderTraversal = inorder_traversal
