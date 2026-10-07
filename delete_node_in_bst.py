'''
Given a root node reference of a BST and a key, delete the node with the given key in the BST. 
Return the root node reference (possibly updated) of the BST.

Basically, the deletion can be divided into two stages:
1. Search for a node to remove.
2. If the node is found, delete the node.

Example 1:
Input: root = [5,3,6,2,4,null,7], key = 3
Output: [5,4,6,2,null,null,7]
Explanation: Given key to delete is 3. So we find the node with value 3 and delete it.
One valid answer is [5,4,6,2,null,null,7], shown in the diagram.
Another valid answer is [5,2,6,null,4,null,7].

Example 2:
Input: root = [5,3,6,2,4,null,7], key = 0
Output: [5,3,6,2,4,null,7]
Explanation: The tree does not contain a node with value = 0.

Example 3:
Input: root = [], key = 0
Output: []

Constraints:
- The number of nodes in the tree is in the range [0, 10^4].
- -10^5 <= Node.val <= 10^5
- Each node has a unique value.
- root is a valid binary search tree.
- -10^5 <= key <= 10^5
'''

from typing import Optional
from tree_node import TreeNode


def delete_node(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """Delete a node with the given key in a BST recursively using in-order successor replacement.

    Time Complexity: O(H) where H is the height of the tree (O(log N) for balanced BST, O(N) for skewed).
    Space Complexity: O(H) auxiliary call stack space due to recursion.
    """
    if not root:
        return None

    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        # Case 1 & Case 2: 0 or 1 child
        if not root.left:
            return root.right
        if not root.right:
            return root.left

        # Case 3: 2 children - find in-order successor (minimum in right subtree)
        successor = _find_min(root.right)
        root.val = successor.val
        root.right = delete_node(root.right, successor.val)

    return root


def _find_min(node: TreeNode) -> TreeNode:
    """Find the leftmost node in a non-empty subtree."""
    curr = node
    while curr.left:
        curr = curr.left
    return curr
