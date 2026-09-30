'''
Consider all the leaves of a binary tree, from left to right order, the values of those leaves form a 
leaf value sequence.

Two binary trees are considered leaf-similar if their leaf value sequence is the same.

Return true if and only if the two given trees with head nodes root1 and root2 are leaf-similar.
'''

from itertools import zip_longest
from typing import Iterator
from tree_node import TreeNode


def leaf_similar(root1: TreeNode | None, root2: TreeNode | None) -> bool:
    """Compare leaf sequences lazily using Python generators with early exit on mismatch."""
    def get_leaves(node: TreeNode | None) -> Iterator[int]:
        if not node:
            return
        if not node.left and not node.right:
            yield node.val
        else:
            yield from get_leaves(node.left)
            yield from get_leaves(node.right)

    return all(a == b for a, b in zip_longest(get_leaves(root1), get_leaves(root2)))


# LeetCode backward compatibility aliases
leaf_similar_generator = leaf_similar
leafSimilar = leaf_similar
