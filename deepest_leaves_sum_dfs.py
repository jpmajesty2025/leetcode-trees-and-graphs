'''
Given the root of a binary tree, return the sum of values of its deepest leaves.
'''

from tree_node import TreeNode


def deepest_leaves_sum_dfs(root: TreeNode | None) -> int:
    """Return the sum of values of the deepest leaves using recursive DFS."""
    if not root:
        return 0

    max_depth = -1
    total = 0

    def dfs(node: TreeNode | None, depth: int) -> None:
        nonlocal max_depth, total
        if not node:
            return

        if depth > max_depth:
            max_depth = depth
            total = node.val
        elif depth == max_depth:
            total += node.val

        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return total
