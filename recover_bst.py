'''
You are given the root of a binary search tree (BST), where the values of exactly two nodes of the 
tree were swapped by mistake. Recover the tree without changing its structure.

Example:
Input: root = [1,3,null,null,2]
Output: [3,1,null,null,2]
Explanation: 3 cannot be a left child of 1 because 3 > 1. Swapping 1 and 3 makes the BST valid.
'''

from tree_node import TreeNode


def recover_tree(root: TreeNode | None) -> None:
    """
    Recover swapped BST in O(1) auxiliary space using Morris In-Order Traversal.
    Modifies root in-place.
    """
    first: TreeNode | None = None
    second: TreeNode | None = None
    prev: TreeNode | None = None
    curr = root

    while curr:
        if curr.left is None:
            # Visit curr
            if prev and prev.val > curr.val:
                if first is None:
                    first = prev
                second = curr
            prev = curr
            curr = curr.right
        else:
            # Find in-order predecessor
            pred = curr.left
            while pred.right and pred.right is not curr:
                pred = pred.right

            if pred.right is None:
                # Establish temporary thread to successor
                pred.right = curr
                curr = curr.left
            else:
                # Thread already exists: break thread and visit curr
                pred.right = None
                if prev and prev.val > curr.val:
                    if first is None:
                        first = prev
                    second = curr
                prev = curr
                curr = curr.right

    if first and second:
        first.val, second.val = second.val, first.val


# LeetCode backward compatibility aliases
recoverTree = recover_tree
recover_Tree = recover_tree
