'''
Given the root of a binary tree, invert the tree, and return its root.

Example:
Input: root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]
'''

from tree_node import TreeNode


def invert_tree(root: TreeNode | None) -> TreeNode | None:
    """Invert a binary tree recursively by swapping subtrees."""
    if not root:
        return None

    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


# LeetCode backward compatibility aliases
invertTree = invert_tree
