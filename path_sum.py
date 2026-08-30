'''
Given the root of a binary tree and an integer target_sum, return true if the tree has a root-to-leaf path such 
that adding up all the values along the path equals target_sum.

A leaf is a node with no children.

Input: root = [5,4,8,11,null,13,4,7,2,null,null,null,1], target_sum = 22
Output: true (5 -> 4 -> 11 -> 2)

Input: root = [1,2,3], target_sum = 5
Output: false
'''

from typing import Optional
from tree_node import TreeNode


def has_path_sum(root: Optional[TreeNode], target_sum: int) -> bool:
    if not root:
        return False

    # A leaf is a node with no children
    if not root.left and not root.right:
        return root.val == target_sum

    remaining = target_sum - root.val
    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)
