'''
Given the root of a binary tree, return True if the binary tree is Even-Odd, otherwise return False.

Recursive DFS Approach with Depth-Indexed Last Visited Values.
'''

from typing import Optional, List
from tree_node import TreeNode


def is_even_odd_tree_dfs(root: Optional[TreeNode]) -> bool:
    """Return True if the binary tree is Even-Odd using recursive DFS with depth indexing.

    Time Complexity: O(N) where N is the number of nodes in the binary tree.
    Space Complexity: O(H) auxiliary recursion stack space, where H is the height of the tree.
    """
    if not root:
        return True

    prev_values: List[int] = []

    def dfs(node: Optional[TreeNode], depth: int) -> bool:
        if not node:
            return True

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

        # Preorder: traverse left subtree before right subtree
        return dfs(node.left, depth + 1) and dfs(node.right, depth + 1)

    return dfs(root, 0)
