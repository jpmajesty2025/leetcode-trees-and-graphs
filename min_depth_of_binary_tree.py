'''
Given a binary tree, find its minimum depth.

The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.
'''

from typing import Optional

from typing import Optional, List, Tuple
from tree_node import TreeNode


def min_depth(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    # Base case: Leaf node
    if not root.left and not root.right:
        return 1

    # If left subtree is empty, recurse into right subtree only
    if not root.left:
        return min_depth(root.right) + 1

    # If right subtree is empty, recurse into left subtree only
    if not root.right:
        return min_depth(root.left) + 1

    # Both subtrees exist
    return min(min_depth(root.left), min_depth(root.right)) + 1


from typing import Optional, List, Tuple

def min_depth_iterative(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    stack: List[Tuple[TreeNode, int]] = [(root, 1)]
    min_d = float('inf')

    while stack:
        node, depth = stack.pop()

        if not node.left and not node.right:
            min_d = min(min_d, depth)
            continue

        # Prune branches that are already deeper than the current minimum found
        if depth >= min_d:
            continue

        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))

    return int(min_d)