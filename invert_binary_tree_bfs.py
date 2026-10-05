'''
Given the root of a binary tree, invert the tree, and return its root.

This module implements the level-order BFS traversal approach.
'''

from collections import deque
from tree_node import TreeNode


def invert_tree_bfs(root: TreeNode | None) -> TreeNode | None:
    """Invert a binary tree iteratively using level-order BFS."""
    if not root:
        return None

    queue: deque[TreeNode] = deque([root])
    while queue:
        curr = queue.popleft()
        curr.left, curr.right = curr.right, curr.left

        if curr.left:
            queue.append(curr.left)
        if curr.right:
            queue.append(curr.right)

    return root


# Aliases
invert_tree = invert_tree_bfs
invertTree = invert_tree_bfs
