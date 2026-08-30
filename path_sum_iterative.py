'''
Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf path such 
that adding up all the values along the path equals targetSum.

A leaf is a node with no children.

Input: root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22
Output: true (5 -> 4 -> 11 -> 2)

Input: root = [1,2,3], targetSum = 5
Output: false
'''

from typing import Optional
from tree_node import TreeNode


def has_path_sum_iterative(root: Optional[TreeNode], targetSum: int) -> bool:
    if not root:
        return False

    stack = [(root, targetSum - root.val)]
    while stack:
        node, remaining = stack.pop()
        # if both children are null, then the node is a leaf
        if not node.left and not node.right and remaining == 0:
            return True

        if node.right:
            stack.append((node.right, remaining - node.right.val))
        if node.left:
            stack.append((node.left, remaining - node.left.val))

    return False
