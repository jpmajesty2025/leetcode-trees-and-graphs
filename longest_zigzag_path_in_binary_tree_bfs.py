'''
You are given the root of a binary tree.
Return the longest ZigZag path contained in that tree.

This module implements the iterative level-order BFS traversal approach.
'''

from collections import deque
from tree_node import TreeNode


def longest_zig_zag_bfs(root: TreeNode | None) -> int:
    """Return the longest ZigZag path using iterative level-order BFS."""
    if not root:
        return 0

    max_len = 0
    # Queue stores: (node, go_left, length)
    queue: deque[tuple[TreeNode, bool, int]] = deque()
    if root.left:
        queue.append((root.left, False, 1))
    if root.right:
        queue.append((root.right, True, 1))

    while queue:
        node, go_left, length = queue.popleft()
        max_len = max(max_len, length)

        if go_left:
            if node.left:
                queue.append((node.left, False, length + 1))
            if node.right:
                queue.append((node.right, True, 1))
        else:
            if node.right:
                queue.append((node.right, True, length + 1))
            if node.left:
                queue.append((node.left, False, 1))

    return max_len


# Aliases
longest_zig_zag = longest_zig_zag_bfs
longestZigZag = longest_zig_zag_bfs
