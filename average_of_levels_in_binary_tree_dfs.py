'''
Given the root of a binary tree, return the average value of the nodes on each level in the form of an array.
Answers within 10^-5 of the actual answer will be accepted.

Recursive DFS Approach with Depth Tracking.
'''

from typing import Optional, List
from tree_node import TreeNode


def average_of_levels_dfs(root: Optional[TreeNode]) -> List[float]:
    """Return the average value of the nodes on each level using recursive DFS.

    Time Complexity: O(N) where N is the number of nodes in the binary tree.
    Space Complexity: O(H) auxiliary recursion stack space, where H is the height of the tree.
    """
    if not root:
        return []

    sums: List[float] = []
    counts: List[int] = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if not node:
            return

        if depth == len(sums):
            sums.append(0.0)
            counts.append(0)

        sums[depth] += node.val
        counts[depth] += 1

        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return [s / c for s, c in zip(sums, counts)]
