'''
Given the root of a binary tree, imagine yourself standing on the right side of it, 
return the values of the nodes you can see ordered from top to bottom.
'''

from collections import deque
from typing import Optional, List
from tree_node import TreeNode


def right_side_view(root: Optional[TreeNode]) -> List[int]:
    """Return the right-side view of a binary tree using iterative BFS."""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        result.append(queue[-1].val)  # Rightmost element in current level

        for _ in range(level_size):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return result
