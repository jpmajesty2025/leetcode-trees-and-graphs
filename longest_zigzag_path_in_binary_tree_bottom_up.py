'''
You are given the root of a binary tree.
Return the longest ZigZag path contained in that tree.

This module implements the bottom-up post-order Tree DP approach.
'''

from tree_node import TreeNode


def longest_zig_zag_bottom_up(root: TreeNode | None) -> int:
    """Return the longest ZigZag path using bottom-up post-order DP."""
    max_len = 0

    def dfs(node: TreeNode | None) -> tuple[int, int]:
        nonlocal max_len
        if not node:
            return -1, -1  # -1 allows 1 + (-1) = 0 for leaf base case

        left_l, left_r = dfs(node.left)
        right_l, right_r = dfs(node.right)

        curr_left_zigzag = 1 + left_r
        curr_right_zigzag = 1 + right_l

        max_len = max(max_len, curr_left_zigzag, curr_right_zigzag)

        return curr_left_zigzag, curr_right_zigzag

    dfs(root)
    return max_len


# Aliases
longest_zig_zag = longest_zig_zag_bottom_up
longestZigZag = longest_zig_zag_bottom_up
