'''
Given a binary tree, find its minimum depth.

Breadth-First Search (Queue / Level-Order) approach.
Optimally finds the shortest root-to-leaf path by stopping at the first leaf encountered.
'''

from collections import deque
from typing import Optional
from tree_node import TreeNode


def min_depth_bfs(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    queue = deque([(root, 1)])

    while queue:
        node, depth = queue.popleft()

        # First leaf encountered gives the minimum depth immediately
        if not node.left and not node.right:
            return depth

        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))

    return 0
