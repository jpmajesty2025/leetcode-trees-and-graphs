'''
Given the root of a binary search tree (BST) with duplicates, return all the mode(s) (i.e., 
the most frequently occurred element) in it.

This module implements Morris Inorder Traversal in O(1) auxiliary space using threaded binary trees.
'''

from tree_node import TreeNode


def find_mode_morris(root: TreeNode | None) -> list[int]:
    """Find mode(s) in a BST in O(1) auxiliary space using Morris Traversal."""
    curr = root
    prev: int | None = None
    count = 0
    max_count = 0
    modes: list[int] = []

    def update_mode(val: int) -> None:
        nonlocal prev, count, max_count, modes
        count = (count + 1) if (prev is not None and val == prev) else 1
        if count > max_count:
            max_count = count
            modes = [val]
        elif count == max_count:
            modes.append(val)
        prev = val

    while curr:
        if not curr.left:
            update_mode(curr.val)
            curr = curr.right
        else:
            predecessor = curr.left
            while predecessor.right and predecessor.right is not curr:
                predecessor = predecessor.right

            if not predecessor.right:
                predecessor.right = curr
                curr = curr.left
            else:
                predecessor.right = None
                update_mode(curr.val)
                curr = curr.right

    return modes


# Aliases
find_mode = find_mode_morris
findMode = find_mode_morris
