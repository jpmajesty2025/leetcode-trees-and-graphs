'''
Given a binary tree, determine if it is height-balanced.

This module implements an explicit stack-safe iterative post-order approach.
'''

from tree_node import TreeNode


def is_balanced_iterative(root: TreeNode | None) -> bool:
    """Determine if a binary tree is height-balanced using iterative post-order traversal."""
    if not root:
        return True

    stack: list[TreeNode] = []
    curr = root
    last_visited: TreeNode | None = None
    heights: dict[TreeNode, int] = {}

    while curr or stack:
        if curr:
            stack.append(curr)
            curr = curr.left
        else:
            peek = stack[-1]
            if peek.right and last_visited is not peek.right:
                curr = peek.right
            else:
                node = stack.pop()
                left_h = heights.get(node.left, 0)
                right_h = heights.get(node.right, 0)

                if abs(left_h - right_h) > 1:
                    return False

                heights[node] = max(left_h, right_h) + 1
                last_visited = node

    return True


# Aliases
is_balanced = is_balanced_iterative
isBalanced = is_balanced_iterative
