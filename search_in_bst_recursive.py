'''
You are given the root of a binary search tree (BST) and an integer val.

Find the node in the BST that the node's value equals val and return the subtree rooted with that 
node. If such a node does not exist, return null.

Recursive Approach.
'''

from typing import Optional
from tree_node import TreeNode


def search_bst_recursive(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """Search for a target value in a Binary Search Tree (BST) recursively.

    Time Complexity: O(H) where H is the height of the tree (O(log N) for balanced BST, O(N) for skewed).
    Space Complexity: O(H) call stack overhead.
    """
    if not root or root.val == val:
        return root

    if val < root.val:
        return search_bst_recursive(root.left, val)
    return search_bst_recursive(root.right, val)
