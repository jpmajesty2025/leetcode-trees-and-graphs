'''
Given the root of a binary tree, return True if the binary tree is Even-Odd, otherwise return False.

Iterative DFS Approach with Explicit Stack.
'''

from typing import Optional, List, Tuple
from tree_node import TreeNode


def is_even_odd_tree_iterative(root: Optional[TreeNode]) -> bool:
    """Return True if the binary tree is Even-Odd using iterative DFS with an explicit stack.

    Time Complexity: O(N) where N is the number of nodes in the binary tree.
    Space Complexity: O(H) auxiliary stack space, where H is the height of the tree.
    """
    if not root:
        return True

    prev_values: List[int] = []
    stack: List[Tuple[TreeNode, int]] = [(root, 0)]

    while stack:
        node, depth = stack.pop()

        # Parity check
        if depth % 2 == 0:
            if node.val % 2 == 0:
                return False
        else:
            if node.val % 2 != 0:
                return False

        # Monotonicity check against the previous node at this same depth
        if depth == len(prev_values):
            prev_values.append(node.val)
        else:
            if depth % 2 == 0:
                if node.val <= prev_values[depth]:
                    return False
            else:
                if node.val >= prev_values[depth]:
                    return False
            prev_values[depth] = node.val

        # Push right child first so left child is popped and processed first
        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))

    return True
