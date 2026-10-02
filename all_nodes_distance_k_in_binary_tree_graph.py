'''
Given the root of a binary tree, the value of a target node target, and an integer k, return an array 
of the values of all nodes that have a distance k from the target node.

This module converts the tree to an explicit undirected adjacency list graph.
'''

from collections import defaultdict, deque
from tree_node import TreeNode


def distance_k_graph(root: TreeNode | None, target: TreeNode, k: int) -> list[int]:
    """Find all nodes at distance k by converting tree to an undirected graph adjacency list."""
    if not root or not target:
        return []

    graph: defaultdict[int, list[int]] = defaultdict(list)

    def build_graph(node: TreeNode | None, parent: TreeNode | None) -> None:
        if not node:
            return
        if parent:
            graph[node.val].append(parent.val)
            graph[parent.val].append(node.val)
        build_graph(node.left, node)
        build_graph(node.right, node)

    build_graph(root, None)

    queue: deque[tuple[int, int]] = deque([(target.val, 0)])
    visited: set[int] = {target.val}
    result: list[int] = []

    while queue:
        curr_val, curr_dist = queue.popleft()
        if curr_dist == k:
            result.append(curr_val)
        elif curr_dist < k:
            for neighbor in graph[curr_val]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, curr_dist + 1))

    return result


# Aliases
distance_k = distance_k_graph
distanceK = distance_k_graph
