'''
Given the root of a binary tree, return the inorder traversal of its nodes' values.

This module implements Morris Inorder Traversal in O(1) auxiliary space using threaded binary trees.
'''

from tree_node import TreeNode


def inorder_traversal_morris(root: TreeNode | None) -> list[int]:
    """Perform an inorder traversal in O(1) auxiliary space using Morris Traversal."""
    result: list[int] = []
    curr = root

    while curr:
        if not curr.left:
            result.append(curr.val)
            curr = curr.right
        else:
            # Find in-order predecessor
            predecessor = curr.left
            while predecessor.right and predecessor.right is not curr:
                predecessor = predecessor.right

            if not predecessor.right:
                # Create temporary thread back to curr
                predecessor.right = curr
                curr = curr.left
            else:
                # Thread already exists -> dismantle thread and visit curr
                predecessor.right = None
                result.append(curr.val)
                curr = curr.right

    return result


# Aliases
inorder_traversal = inorder_traversal_morris
inorderTraversal = inorder_traversal_morris
