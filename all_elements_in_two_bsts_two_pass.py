'''
Given two binary search trees root1 and root2, return a list containing all the integers from both 
trees sorted in ascending order.

Two-Pass In-Order Traversal + Linear Two-Pointer Merge Approach.
'''

from typing import Optional, List
from tree_node import TreeNode


def get_all_elements_two_pass(root1: Optional[TreeNode], root2: Optional[TreeNode]) -> List[int]:
    """Return sorted elements from two BSTs using two in-order traversals followed by a two-pointer merge.

    Time Complexity: O(N + M) where N and M are the number of nodes in root1 and root2.
    Space Complexity: O(N + M) auxiliary memory for storing intermediate in-order lists.
    """
    def inorder(node: Optional[TreeNode], acc: List[int]) -> None:
        if not node:
            return
        inorder(node.left, acc)
        acc.append(node.val)
        inorder(node.right, acc)

    list1: List[int] = []
    list2: List[int] = []
    inorder(root1, list1)
    inorder(root2, list2)

    # Linear two-pointer merge of two pre-sorted lists
    merged: List[int] = []
    i, j = 0, 0
    n1, n2 = len(list1), len(list2)

    while i < n1 and j < n2:
        if list1[i] <= list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1

    if i < n1:
        merged.extend(list1[i:])
    if j < n2:
        merged.extend(list2[j:])

    return merged
