'''
You are given the root node of a binary search tree (BST) and a value to insert into the tree. 
Return the root node of the BST after the insertion. It is guaranteed that the new value does not exist 
in the original BST.

Notice that there may exist multiple valid ways for the insertion, as long as the tree remains a BST 
after insertion. You can return any of them.
'''

from typing import Optional
from tree_node import TreeNode


def insert_into_bst_iterative(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """Insert a value into a BST using an iterative pointer walk in O(1) auxiliary space."""
    if not root:
        return TreeNode(val)

    curr = root
    while True:
        if val < curr.val:
            if not curr.left:
                curr.left = TreeNode(val)
                break
            curr = curr.left
        else:
            if not curr.right:
                curr.right = TreeNode(val)
                break
            curr = curr.right

    return root