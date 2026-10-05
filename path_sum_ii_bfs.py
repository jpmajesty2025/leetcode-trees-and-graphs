'''
Given the root of a binary tree and an integer targetSum, return all root-to-leaf paths where the 
sum of the node values in the path equals targetSum.

This module implements the iterative level-order BFS traversal approach.
'''

from collections import deque
from tree_node import TreeNode


def path_sum_bfs(root: TreeNode | None, target_sum: int) -> list[list[int]]:
    """Return all root-to-leaf paths equaling target_sum using iterative BFS."""
    if not root:
        return []

    result: list[list[int]] = []
    queue: deque[tuple[TreeNode, int, list[int]]] = deque(
        [(root, target_sum - root.val, [root.val])]
    )

    while queue:
        node, remaining, path = queue.popleft()

        if not node.left and not node.right and remaining == 0:
            result.append(path)
            continue

        if node.left:
            queue.append(
                (node.left, remaining - node.left.val, path + [node.left.val])
            )
        if node.right:
            queue.append(
                (node.right, remaining - node.right.val, path + [node.right.val])
            )

    return result


# Aliases
path_sum = path_sum_bfs
pathSum = path_sum_bfs
