'''
Given the root of a binary tree, return an array of the largest value in each row of the tree (0-indexed).
'''

from collections import deque
from typing import Optional
from tree_node import TreeNode

def largest_values(root: Optional[TreeNode]) -> list[int]:
    """Return the largest value in each row of a binary tree using iterative BFS."""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        max_value = float('-inf')

        for _ in range(level_size):
            node = queue.popleft()
            max_value = max(max_value, node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(max_value)

    return result