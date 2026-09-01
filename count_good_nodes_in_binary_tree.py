'''
Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with a value greater than X.

Return the number of good nodes in the binary tree
'''
from typing import Optional
from tree_node import TreeNode


def good_nodes(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    def dfs(node: Optional[TreeNode], max_val: int) -> int:
        if not node:
            return 0

        is_good = 1 if node.val >= max_val else 0
        new_max = max(max_val, node.val)

        return is_good + dfs(node.left, new_max) + dfs(node.right, new_max)

    return dfs(root, root.val)
