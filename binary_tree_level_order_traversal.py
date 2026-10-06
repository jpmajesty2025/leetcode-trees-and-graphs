'''
Given the root of a binary tree, return the level order traversal of its nodes' values.
(i.e., from left to right, level by level).

Example 1:
Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]

Example 2:
Input: root = [1]
Output: [[1]]

Example 3:
Input: root = []
Output: []

Constraints:
- The number of nodes in the tree is in the range [0, 2000].
- -1000 <= Node.val <= 1000
'''

from collections import deque
from typing import Optional, List
from tree_node import TreeNode


def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """Return the level order traversal of a binary tree's values using BFS.

    Time Complexity: O(N) where N is the total number of nodes in the binary tree.
    Space Complexity: O(W) where W is the maximum width of the binary tree (up to N / 2 in a full tree).
    """
    if not root:
        return []

    result: List[List[int]] = []
    queue: deque[TreeNode] = deque([root])

    while queue:
        level_size = len(queue)
        current_level: List[int] = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)

    return result
