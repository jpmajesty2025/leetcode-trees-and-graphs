'''
Given the root of a binary tree, return the average value of the nodes on each level in the form of an array.
Answers within 10^-5 of the actual answer will be accepted.

Example 1:
Input: root = [3,9,20,null,null,15,7]
Output: [3.00000,14.50000,11.00000]
Explanation: The average value of nodes on level 0 is 3, on level 1 is 14.5, and on level 2 is 11.
Hence return [3, 14.5, 11].

Example 2:
Input: root = [3,9,20,15,7]
Output: [3.00000,14.50000,11.00000]

Constraints:
- The number of nodes in the tree is in the range [1, 10^4].
- -2^31 <= Node.val <= 2^31 - 1
'''

from collections import deque
from typing import Optional, List
from tree_node import TreeNode


def average_of_levels(root: Optional[TreeNode]) -> List[float]:
    """Return the average value of the nodes on each level using BFS.

    Time Complexity: O(N) where N is the number of nodes in the binary tree.
    Space Complexity: O(W) where W is the maximum width of the tree (up to N / 2).
    """
    if not root:
        return []

    result: List[float] = []
    queue: deque[TreeNode] = deque([root])

    while queue:
        level_size = len(queue)
        current_sum = 0

        for _ in range(level_size):
            node = queue.popleft()
            current_sum += node.val

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_sum / level_size)

    return result
