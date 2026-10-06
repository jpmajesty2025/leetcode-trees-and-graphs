'''
Given the root of a binary tree, return the average value of the nodes on each level in the form of an array.
Answers within 10^-5 of the actual answer will be accepted.

Iterative DFS Approach with Explicit Stack.
'''

from typing import Optional, List, Tuple
from tree_node import TreeNode


def average_of_levels_iterative(root: Optional[TreeNode]) -> List[float]:
    """Return the average value of the nodes on each level using iterative DFS with an explicit stack.

    Time Complexity: O(N) where N is the number of nodes in the binary tree.
    Space Complexity: O(H) auxiliary stack space, where H is the height of the tree.
    """
    if not root:
        return []

    sums: List[float] = []
    counts: List[int] = []
    stack: List[Tuple[TreeNode, int]] = [(root, 0)]

    while stack:
        node, depth = stack.pop()

        if depth == len(sums):
            sums.append(0.0)
            counts.append(0)

        sums[depth] += node.val
        counts[depth] += 1

        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))

    return [s / c for s, c in zip(sums, counts)]
