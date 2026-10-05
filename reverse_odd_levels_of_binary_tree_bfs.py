'''
Given the root of a perfect binary tree, reverse the node values at each odd level of the tree.

This module implements the level-order BFS two-pointer value swapping approach.
'''

from collections import deque
from tree_node import TreeNode


def reverse_odd_levels_bfs(root: TreeNode | None) -> TreeNode | None:
    """Reverse node values at odd levels using level-order BFS."""
    if not root:
        return None

    queue: deque[TreeNode] = deque([root])
    is_odd = False

    while queue:
        level_size = len(queue)
        current_level_nodes: list[TreeNode] = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level_nodes.append(node)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        if is_odd:
            left, right = 0, len(current_level_nodes) - 1
            while left < right:
                current_level_nodes[left].val, current_level_nodes[right].val = (
                    current_level_nodes[right].val,
                    current_level_nodes[left].val,
                )
                left += 1
                right -= 1

        is_odd = not is_odd

    return root


# Aliases
reverse_odd_levels = reverse_odd_levels_bfs
reverseOddLevels = reverse_odd_levels_bfs
