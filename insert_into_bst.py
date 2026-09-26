'''
You are given the root node of a binary search tree (BST) and a value to insert into the tree. 
Return the root node of the BST after the insertion. It is guaranteed that the new value does not exist 
in the original BST.

Notice that there may exist multiple valid ways for the insertion, as long as the tree remains a BST 
after insertion. You can return any of them.
'''

from typing import Optional
from tree_node import TreeNode

def insert_into_bst(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """Insert a value into a Binary Search Tree (BST) and return the root of the modified tree."""
    if not root:
        return TreeNode(val)

    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    else:
        root.right = insert_into_bst(root.right, val)

    return root