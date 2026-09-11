'''
Given the roots of two binary trees p and q, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.
'''


from typing import Optional
from tree_node import TreeNode

def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    if p is None and q is None:
        return True
    
    if p is None or q is None:
        return False
    
    if p.val != q.val:
        return False
    
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)