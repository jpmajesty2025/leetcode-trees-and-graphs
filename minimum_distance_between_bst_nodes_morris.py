'''
Given the root of a Binary Search Tree (BST), return the minimum difference between the values of any two 
different nodes in the tree.

This module implements Morris Inorder Traversal in O(1) auxiliary space using threaded binary trees.
'''

from tree_node import TreeNode


def min_diff_in_bst_morris(root: TreeNode | None) -> int:
    """Find minimum distance between BST nodes in O(1) auxiliary space using Morris Traversal."""
    if not root:
        return 0

    curr = root
    prev: int | None = None
    min_diff = float('inf')

    while curr:
        if not curr.left:
            if prev is not None:
                min_diff = min(min_diff, curr.val - prev)
            prev = curr.val
            curr = curr.right
        else:
            predecessor = curr.left
            while predecessor.right and predecessor.right is not curr:
                predecessor = predecessor.right

            if not predecessor.right:
                predecessor.right = curr
                curr = curr.left
            else:
                predecessor.right = None
                if prev is not None:
                    min_diff = min(min_diff, curr.val - prev)
                prev = curr.val
                curr = curr.right

    return int(min_diff) if min_diff != float('inf') else 0


# Aliases
min_diff_in_bst = min_diff_in_bst_morris
minDiffInBST = min_diff_in_bst_morris
