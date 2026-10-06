'''
Given the root of a binary tree, return the level order traversal of its nodes' values.
(i.e., from left to right, level by level).

Iterative DFS Approach with an Explicit Stack.
'''

from typing import Optional, List, Tuple
from tree_node import TreeNode


def level_order_iterative(root: Optional[TreeNode]) -> List[List[int]]:
    """Return level order traversal using iterative DFS with an explicit stack.

    Time Complexity: O(N) where N is the total number of nodes in the binary tree.
    Space Complexity: O(H) auxiliary stack space, where H is the height of the tree
                      (O(log N) for balanced trees, O(N) for skewed trees).
    """
    if not root:
        return []

    result: List[List[int]] = []
    stack: List[Tuple[TreeNode, int]] = [(root, 0)]

    while stack:
        node, depth = stack.pop()

        if depth == len(result):
            result.append([])

        result[depth].append(node.val)

        # Push right child first so that left child is popped and processed first
        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))

    return result
