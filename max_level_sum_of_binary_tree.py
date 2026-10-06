'''
Given the root of a binary tree, the level of its root is 1, the level of its children is 2, and so on.

Return the smallest level x such that the sum of all the values of nodes at level x is maximal.

Example 1:
Input: root = [1,7,0,7,-8,null,null]
Output: 2
Explanation: 
Level 1 sum = 1.
Level 2 sum = 7 + 0 = 7.
Level 3 sum = 7 + -8 = -1.
So we return the level with the maximum sum which is level 2.

Example 2:
Input: root = [989,null,10250,98697,-34348,null,null,null,-89388]
Output: 3

Constraints:
- The number of nodes in the tree is in the range [1, 10^4].
- -10^5 <= Node.val <= 10^5
'''

from collections import deque
from typing import Optional
from tree_node import TreeNode


def max_level_sum(root: Optional[TreeNode]) -> int:
    """Return the smallest 1-based level x such that the sum of all node values at level x is maximal.

    Time Complexity: O(N) where N is the number of nodes in the binary tree.
    Space Complexity: O(W) where W is the maximum width of the tree (up to N / 2).
    """
    if not root:
        return 0

    max_sum = float('-inf')
    best_level = 1
    current_level = 1
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

        # Strictly greater ensures we keep the smallest level on ties
        if current_sum > max_sum:
            max_sum = current_sum
            best_level = current_level

        current_level += 1

    return best_level
