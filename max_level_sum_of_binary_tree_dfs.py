'''
Given the root of a binary tree, return the smallest level x such that the sum of all the values of nodes at level x is maximal.

Recursive DFS Approach with Level Sum Tracking.
'''

from typing import Optional, List
from tree_node import TreeNode


def max_level_sum_dfs(root: Optional[TreeNode]) -> int:
    """Return the smallest 1-based level with the maximum sum using recursive DFS.

    Time Complexity: O(N) where N is the number of nodes in the binary tree.
    Space Complexity: O(H) auxiliary recursion stack space, where H is the height of the tree.
    """
    if not root:
        return 0

    level_sums: List[int] = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if not node:
            return

        if depth == len(level_sums):
            level_sums.append(0)

        level_sums[depth] += node.val
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)

    # index() naturally returns the smallest 0-based index of the first occurrence of max value
    max_val = max(level_sums)
    return level_sums.index(max_val) + 1
