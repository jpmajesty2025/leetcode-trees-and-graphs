'''
Given the roots of two binary trees p and q, write a function to check if they are the same or not.

Iterative DFS (Stack) approach.
'''

from typing import Optional
from tree_node import TreeNode


def is_same_tree_iterative(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    stack = [(p, q)]
    
    while stack:
        node_p, node_q = stack.pop()
        
        if node_p is None and node_q is None:
            continue
        if node_p is None or node_q is None:
            return False
        if node_p.val != node_q.val:
            return False
            
        stack.append((node_p.right, node_q.right))
        stack.append((node_p.left, node_q.left))
        
    return True
