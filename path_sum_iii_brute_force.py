'''
Given the root of a binary tree and an integer targetSum, return the number of paths where the sum 
of the values along the path equals targetSum.

This module implements the baseline double DFS brute-force approach (O(N^2) worst case).
'''

from tree_node import TreeNode


def path_sum_brute_force(root: TreeNode | None, target_sum: int) -> int:
    """Count paths summing to target_sum using double DFS recursion."""
    if not root:
        return 0

    def count_from_node(node: TreeNode | None, remaining: int) -> int:
        if not node:
            return 0
        matches = 1 if node.val == remaining else 0
        return (
            matches
            + count_from_node(node.left, remaining - node.val)
            + count_from_node(node.right, remaining - node.val)
        )

    return (
        count_from_node(root, target_sum)
        + path_sum_brute_force(root.left, target_sum)
        + path_sum_brute_force(root.right, target_sum)
    )


# Aliases
path_sum = path_sum_brute_force
pathSum = path_sum_brute_force
