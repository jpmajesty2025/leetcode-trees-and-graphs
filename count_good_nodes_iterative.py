'''
Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with a value greater than X.

Return the number of good nodes in the binary tree
'''
from typing import Optional
from tree_node import TreeNode


def good_nodes_iterative(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    count = 0
    stack = [(root, root.val)]

    while stack:
        node, max_val = stack.pop()
        if node.val >= max_val:
            count += 1
            max_val = node.val

        if node.right:
            stack.append((node.right, max_val))
        if node.left:
            stack.append((node.left, max_val))

    return count
