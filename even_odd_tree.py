'''
A binary tree is named Even-Odd if it meets the following conditions:

The root of the binary tree is at level index 0, its children are at level index 1, their children 
are at level index 2, etc.
- For every even-indexed level, all nodes at the level have odd integer values in strictly 
  increasing order (from left to right).
- For every odd-indexed level, all nodes at the level have even integer values in strictly 
  decreasing order (from left to right).

Given the root of a binary tree, return true if the binary tree is Even-Odd, otherwise return false.

Example 1:
Input: root = [1,10,4,3,null,7,9,12,8,6,null,null,2]
Output: true
Explanation: The node values on each level are:
Level 0: [1]
Level 1: [10,4]
Level 2: [3,7,9]
Level 3: [12,8,6,2]
Since levels 0 and 2 are all odd and strictly increasing, and levels 1 and 3 are all even and strictly decreasing, the tree is Even-Odd.

Example 2:
Input: root = [5,4,2,3,3,7]
Output: false
Explanation: The node values on level 2 are [3,3,7], which is not strictly increasing.

Example 3:
Input: root = [5,9,1,3,5,7]
Output: false
Explanation: Node values on level 1 are [9,1] (odd integers, but level 1 is odd-indexed so must be even).

Constraints:
- The number of nodes in the tree is in the range [1, 10^5].
- 1 <= Node.val <= 10^6
'''

from collections import deque
from typing import Optional
from tree_node import TreeNode


def is_even_odd_tree(root: Optional[TreeNode]) -> bool:
    """Return True if the binary tree satisfies the Even-Odd conditions using BFS.

    Time Complexity: O(N) where N is the number of nodes in the binary tree.
    Space Complexity: O(W) where W is the maximum width of the tree (up to N / 2).
    """
    if not root:
        return True

    queue: deque[TreeNode] = deque([root])
    level = 0

    while queue:
        level_size = len(queue)
        prev_value: Optional[int] = None

        for _ in range(level_size):
            node = queue.popleft()

            # Even-indexed level: values must be odd and strictly increasing
            if level % 2 == 0:
                if node.val % 2 == 0 or (prev_value is not None and node.val <= prev_value):
                    return False
            # Odd-indexed level: values must be even and strictly decreasing
            else:
                if node.val % 2 != 0 or (prev_value is not None and node.val >= prev_value):
                    return False

            prev_value = node.val

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        level += 1

    return True
