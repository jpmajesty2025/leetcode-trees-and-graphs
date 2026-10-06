'''
Given the root of a binary tree, return the smallest level x such that the sum of all the values of nodes at level x is maximal.

Iterative DFS Approach with Explicit Stack.
'''

from typing import Optional, List, Tuple
from tree_node import TreeNode


def max_level_sum_iterative(root: Optional[TreeNode]) -> int:
    """Return the smallest 1-based level with the maximum sum using iterative DFS with an explicit stack.

    Time Complexity: O(N) where N is the number of nodes in the binary tree.
    Space Complexity: O(H) auxiliary stack space, where H is the height of the tree.
    """
    if not root:
        return 0

    level_sums: List[int] = []
    stack: List[Tuple[TreeNode, int]] = [(root, 0)]

    while stack:
        node, depth = stack.pop()

        if depth == len(level_sums):
            level_sums.append(0)

        level_sums[depth] += node.val

        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))

    max_val = max(level_sums)
    return level_sums.index(max_val) + 1
