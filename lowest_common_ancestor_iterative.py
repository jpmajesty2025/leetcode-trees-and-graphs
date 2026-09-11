'''
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

Iterative Parent-Pointer approach using Stack and Hash Map.
'''

from typing import Optional, Dict, Set, List
from tree_node import TreeNode


def lowest_common_ancestor_iterative(root: Optional[TreeNode], p: Optional[TreeNode], q: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root or not p or not q:
        return None

    # Map each node to its parent; explicitly annotated to avoid Pylance inferring Dict[TreeNode, None]
    parent_map: Dict[TreeNode, Optional[TreeNode]] = {root: None}
    stack: List[TreeNode] = [root]

    # Traverse until both p and q have their parents mapped
    while stack and (p not in parent_map or q not in parent_map):
        node = stack.pop()

        if node.left:
            parent_map[node.left] = node
            stack.append(node.left)
        if node.right:
            parent_map[node.right] = node
            stack.append(node.right)

    # Edge case: If either node was not found in the tree
    if p not in parent_map or q not in parent_map:
        return None

    # Collect all ancestors of p (including p itself)
    ancestors_of_p: Set[TreeNode] = set()
    curr_p: Optional[TreeNode] = p
    while curr_p is not None:
        ancestors_of_p.add(curr_p)
        curr_p = parent_map[curr_p]

    # First ancestor of q that is also an ancestor of p is the LCA
    curr_q: Optional[TreeNode] = q
    while curr_q is not None and curr_q not in ancestors_of_p:
        curr_q = parent_map[curr_q]

    return curr_q
