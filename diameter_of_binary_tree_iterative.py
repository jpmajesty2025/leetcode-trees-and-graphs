'''
Given the root of a binary tree, return the length of the diameter of the tree.

The diameter of a binary tree is the length of the longest path between any two nodes in a tree. 
This path may or may not pass through the root.

The length of a path between two nodes is represented by the number of edges between them.
'''

from typing import Optional, Dict
from tree_node import TreeNode


def diameter_of_binary_tree_iterative(root: Optional[TreeNode]) -> int:
    """Find the diameter of a binary tree using an iterative post-order traversal with an explicit stack."""
    if not root:
        return 0

    max_diameter = 0
    stack = [root]
    depths: Dict[Optional[TreeNode], int] = {None: 0}

    while stack:
        node = stack[-1]

        if (node.left and node.left not in depths) or (node.right and node.right not in depths):
            if node.right and node.right not in depths:
                stack.append(node.right)
            if node.left and node.left not in depths:
                stack.append(node.left)
        else:
            stack.pop()
            left_depth = depths[node.left]
            right_depth = depths[node.right]

            max_diameter = max(max_diameter, left_depth + right_depth)
            depths[node] = max(left_depth, right_depth) + 1

    return max_diameter
