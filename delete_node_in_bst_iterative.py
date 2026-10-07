'''
Given a root node reference of a BST and a key, delete the node with the given key in the BST. 
Return the root node reference (possibly updated) of the BST.

Iterative Approach with O(1) Auxiliary Space.
'''

from typing import Optional
from tree_node import TreeNode


def delete_node_iterative(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """Delete a node with the given key in a BST iteratively.

    Time Complexity: O(H) where H is the height of the tree (O(log N) for balanced BST, O(N) for skewed).
    Space Complexity: O(1) auxiliary space.
    """
    curr: Optional[TreeNode] = root
    parent: Optional[TreeNode] = None

    # Step 1: Search for target node and its parent
    while curr and curr.val != key:
        parent = curr
        if key < curr.val:
            curr = curr.left
        else:
            curr = curr.right

    # Node not found
    if not curr:
        return root

    # Step 2: Handle node deletion
    # Case A: 0 or 1 child
    if not curr.left or not curr.right:
        child = curr.left if curr.left else curr.right
        if not parent:
            return child
        if parent.left is curr:
            parent.left = child
        else:
            parent.right = child
        return root

    # Case B: 2 children - find in-order successor and its parent
    succ_parent = curr
    succ = curr.right
    while succ.left:
        succ_parent = succ
        succ = succ.left

    # Replace target's value with successor's value
    curr.val = succ.val

    # Unlink successor (which has at most one right child)
    if succ_parent.left is succ:
        succ_parent.left = succ.right
    else:
        succ_parent.right = succ.right

    return root
