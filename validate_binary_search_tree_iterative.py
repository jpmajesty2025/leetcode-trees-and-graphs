'''
Given the root of a binary tree, determine if it is a valid BST.
'''

from typing import Optional, List, Tuple, Union
from tree_node import TreeNode


def is_valid_bst_iterative(root: Optional[TreeNode]) -> bool:
    """Determine if a binary tree is a valid Binary Search Tree (BST) using iterative DFS with an explicit stack."""
    if not root:
        return True

    stack: List[Tuple[TreeNode, Union[int, float], Union[int, float]]] = [(root, float("-inf"), float("inf"))]
    while stack:
        node, small, large = stack.pop()
        if not (small < node.val < large):
            return False

        if node.left:
            stack.append((node.left, small, node.val))
        if node.right:
            stack.append((node.right, node.val, large))

    return True
