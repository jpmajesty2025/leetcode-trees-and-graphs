'''
Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf path such 
that adding up all the values along the path equals targetSum.

A leaf is a node with no children.

Input: root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22
Output: true (5 -> 4 -> 11 -> 2)

Input: root = [1,2,3], targetSum = 5
Output: false
'''

from collections import deque
from typing import Optional
from tree_node import TreeNode


def has_path_sum_bfs(root: Optional[TreeNode], targetSum: int) -> bool:
    if not root:
        return False

    queue = deque([(root, root.val)])
    while queue:
        node, curr_sum = queue.popleft()
        # if both children are null, then the node is a leaf
        if not node.left and not node.right and curr_sum == targetSum:
            return True

        if node.left:
            queue.append((node.left, curr_sum + node.left.val))
        if node.right:
            queue.append((node.right, curr_sum + node.right.val))

    return False
