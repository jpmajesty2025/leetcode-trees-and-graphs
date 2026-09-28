'''
Given the root of a Binary Search Tree (BST), return the minimum difference between the values of any two 
different nodes in the tree.
'''

from tree_node import TreeNode


def min_diff_in_bst(root: TreeNode | None) -> int:
    """Find minimum distance between BST nodes using single-pass recursive in-order traversal."""
    prev: int | None = None
    min_diff = float('inf')

    def inorder(node: TreeNode | None) -> None:
        nonlocal prev, min_diff
        if not node:
            return

        inorder(node.left)

        if prev is not None:
            min_diff = min(min_diff, node.val - prev)
        prev = node.val

        inorder(node.right)

    inorder(root)
    return int(min_diff) if min_diff != float('inf') else 0


# LeetCode backward compatibility aliases
min_diff_in_bst_dfs = min_diff_in_bst
minDiffInBST = min_diff_in_bst
