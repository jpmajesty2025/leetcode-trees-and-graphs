'''
Given the root of a binary tree, return the sum of values of its deepest leaves.
'''

from tree_node import TreeNode


def deepest_leaves_sum_iterative(root: TreeNode | None) -> int:
    """Return the sum of values of the deepest leaves using iterative DFS with an explicit stack."""
    if not root:
        return 0

    max_depth = -1
    total = 0
    stack: list[tuple[TreeNode, int]] = [(root, 0)]

    while stack:
        node, depth = stack.pop()

        if depth > max_depth:
            max_depth = depth
            total = node.val
        elif depth == max_depth:
            total += node.val

        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))

    return total
