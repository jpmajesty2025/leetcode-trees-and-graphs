'''
Given the root of a binary tree, return the level order traversal of its nodes' values.
(i.e., from left to right, level by level).

DFS Preorder Traversal Approach with Depth Indexing.
'''

from typing import Optional, List
from tree_node import TreeNode


def level_order_dfs(root: Optional[TreeNode]) -> List[List[int]]:
    """Return the level order traversal of a binary tree's values using DFS with level indexing.

    Time Complexity: O(N) where N is the total number of nodes in the binary tree.
    Space Complexity: O(H) call stack overhead, where H is the height of the tree
                      (O(log N) for balanced trees, O(N) for skewed trees),
                      excluding the output storage.
    """
    if not root:
        return []

    result: List[List[int]] = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if not node:
            return

        if depth == len(result):
            result.append([])

        result[depth].append(node.val)
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return result
