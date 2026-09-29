'''
Given the root of a binary search tree (BST) with duplicates, return all the mode(s) (i.e., 
the most frequently occurred element) in it.

If the tree has more than one mode, return them in any order.

Assume a BST is defined as follows:

The left subtree of a node contains only nodes with keys less than or equal to the node's key.
The right subtree of a node contains only nodes with keys greater than or equal to the node's key.
Both the left and right subtrees must also be binary search trees.
'''

from tree_node import TreeNode


def find_mode(root: TreeNode | None) -> list[int]:
    """Find mode(s) in a BST using clean single-pass recursive in-order traversal."""
    prev: int | None = None
    count = 0
    max_count = 0
    modes: list[int] = []

    def inorder(node: TreeNode | None) -> None:
        nonlocal prev, count, max_count, modes
        if not node:
            return

        inorder(node.left)

        count = (count + 1) if (prev is not None and node.val == prev) else 1

        if count > max_count:
            max_count = count
            modes = [node.val]
        elif count == max_count:
            modes.append(node.val)

        prev = node.val

        inorder(node.right)

    inorder(root)
    return modes


# LeetCode backward compatibility aliases
find_mode_dfs = find_mode
findMode = find_mode
