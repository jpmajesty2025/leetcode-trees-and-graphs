'''
Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.

Recursive BST Approach.
'''

from typing import Optional
from tree_node import TreeNode


def lowest_common_ancestor_recursive(root: TreeNode, p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """Find the lowest common ancestor (LCA) of two nodes in a BST recursively.

    Time Complexity: O(H) where H is the height of the tree (O(log N) for balanced BST, O(N) for skewed).
    Space Complexity: O(H) call stack overhead.
    """
    if not root:
        return None

    if p.val < root.val and q.val < root.val:
        return lowest_common_ancestor_recursive(root.left, p, q)
    elif p.val > root.val and q.val > root.val:
        return lowest_common_ancestor_recursive(root.right, p, q)

    return root
