'''
Given the roots of two binary trees p and q, write a function to check if they are the same or not.

Breadth-First Search (Queue) approach.
'''

from collections import deque
from typing import Optional
from tree_node import TreeNode


def is_same_tree_bfs(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    queue = deque([(p, q)])
    
    while queue:
        node_p, node_q = queue.popleft()
        
        if node_p is None and node_q is None:
            continue
        if node_p is None or node_q is None:
            return False
        if node_p.val != node_q.val:
            return False
            
        queue.append((node_p.left, node_q.left))
        queue.append((node_p.right, node_q.right))
        
    return True
