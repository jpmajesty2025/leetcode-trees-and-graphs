'''
Given the root of a binary tree, the value of a target node target, and an integer k, return an array 
of the values of all nodes that have a distance k from the target node.

This module implements a pure recursive DFS approach without building an auxiliary graph.
'''

from tree_node import TreeNode


def distance_k_dfs(root: TreeNode | None, target: TreeNode, k: int) -> list[int]:
    """Find all nodes at distance k from target using pure subtree and ancestor DFS."""
    result: list[int] = []

    def collect_subtree(node: TreeNode | None, dist: int) -> None:
        """Collect nodes at distance 'dist' below current node."""
        if not node or dist < 0:
            return
        if dist == 0:
            result.append(node.val)
            return
        collect_subtree(node.left, dist - 1)
        collect_subtree(node.right, dist - 1)

    def find_target(node: TreeNode | None) -> int:
        """Return distance from node to target, or -1 if target not in subtree."""
        if not node:
            return -1
        if node is target:
            collect_subtree(node, k)
            return 0

        # Check left subtree
        left_dist = find_target(node.left)
        if left_dist != -1:
            if left_dist + 1 == k:
                result.append(node.val)
            else:
                collect_subtree(node.right, k - left_dist - 2)
            return left_dist + 1

        # Check right subtree
        right_dist = find_target(node.right)
        if right_dist != -1:
            if right_dist + 1 == k:
                result.append(node.val)
            else:
                collect_subtree(node.left, k - right_dist - 2)
            return right_dist + 1

        return -1

    find_target(root)
    return result


# Aliases
distance_k = distance_k_dfs
distanceK = distance_k_dfs
