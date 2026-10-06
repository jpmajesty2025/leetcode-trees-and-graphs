'''
Given two binary search trees root1 and root2, return a list containing all the integers from both 
trees sorted in ascending order.

Example 1:
Input: root1 = [2,1,4], root2 = [1,0,3]
Output: [0,1,1,2,3,4]

Example 2:
Input: root1 = [1,null,8], root2 = [8,1]
Output: [1,1,8,8]

Constraints:
- The number of nodes in each tree is in the range [0, 5000].
- -10^5 <= Node.val <= 10^5
'''

from typing import Optional
from tree_node import TreeNode


def get_all_elements(root1: Optional[TreeNode], root2: Optional[TreeNode]) -> list[int]:
    """Return a sorted list of all elements from two BSTs using single-pass concurrent in-order traversal.

    Time Complexity: O(N + M) where N and M are the number of nodes in root1 and root2.
    Space Complexity: O(H1 + H2) auxiliary stack space, where H1 and H2 are the heights of the two trees.
    """
    stack1: list[TreeNode] = []
    stack2: list[TreeNode] = []
    result: list[int] = []

    curr1 = root1
    curr2 = root2

    while curr1 or curr2 or stack1 or stack2:
        # Traverse left subtree for tree 1
        while curr1:
            stack1.append(curr1)
            curr1 = curr1.left

        # Traverse left subtree for tree 2
        while curr2:
            stack2.append(curr2)
            curr2 = curr2.left

        # Compare the next smallest elements from both BST stacks
        if not stack2 or (stack1 and stack1[-1].val <= stack2[-1].val):
            node = stack1.pop()
            result.append(node.val)
            curr1 = node.right
        else:
            node = stack2.pop()
            result.append(node.val)
            curr2 = node.right

    return result
