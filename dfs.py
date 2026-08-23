'''
Implementation of Depth First Search (DFS) algorithm in Python.

## Complexity
* **Time Complexity:** O(N) because every node in the tree is visited exactly once.
* **Space Complexity:** O(H) where H is the height of the tree, 
determined by the call stack during recursion.
'''
from tree_node import TreeNode
from typing import Optional

def dfs(node: Optional[TreeNode]):
    if node == None:
        return

    dfs(node.left)
    dfs(node.right)
    return

def preorder(node: Optional[TreeNode]):
  if node is None:
    return
  print(node.val)  # Process root
  preorder(node.left)  # Visit left
  preorder(node.right)  # Visit right

def inorder(node: Optional[TreeNode]):
    if node is None:
      return
    inorder(node.left)  # Visit left
    print(node.val)  # Process root
    inorder(node.right)  # Visit right

def postorder(node: Optional[TreeNode]):
  if node is None:
    return
  postorder(node.left)  # Visit left
  postorder(node.right)  # Visit right
  print(node.val)  # Process root