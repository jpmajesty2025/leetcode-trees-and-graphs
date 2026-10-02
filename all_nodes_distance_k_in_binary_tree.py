'''
Given the root of a binary tree, the value of a target node target, and an integer k, return an array 
of the values of all nodes that have a distance k from the target node.

You can return the answer in any order.
'''

from collections import deque
from tree_node import TreeNode


def distance_k(root: TreeNode | None, target: TreeNode, k: int) -> list[int]:
    """Find all nodes at distance k from target using a parent map and level-by-level BFS."""
    if not root or not target:
        return []

    # Map each child node to its parent
    parents: dict[TreeNode, TreeNode] = {}
    queue: deque[TreeNode] = deque([root])
    while queue:
        curr = queue.popleft()
        if curr.left:
            parents[curr.left] = curr
            queue.append(curr.left)
        if curr.right:
            parents[curr.right] = curr
            queue.append(curr.right)

    # Radiate outward from target using BFS
    bfs_queue: deque[TreeNode] = deque([target])
    visited: set[TreeNode] = {target}
    curr_distance = 0

    while bfs_queue and curr_distance < k:
        for _ in range(len(bfs_queue)):
            node = bfs_queue.popleft()
            for neighbor in (node.left, node.right, parents.get(node)):
                if neighbor and neighbor not in visited:
                    visited.add(neighbor)
                    bfs_queue.append(neighbor)
        curr_distance += 1

    return [node.val for node in bfs_queue]


# LeetCode backward compatibility alias
distanceK = distance_k
