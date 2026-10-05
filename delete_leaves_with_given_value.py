'''
Given a binary tree root and an integer target, delete all the leaf nodes with value target.

Note that once you delete a leaf node with value target, if its parent node becomes a leaf node 
and has the value target, it should also be deleted (you need to continue doing that until you cannot). 
'''

from tree_node import TreeNode


def remove_leaf_nodes(root: TreeNode | None, target: int) -> TreeNode | None:
    """Remove all leaf nodes with value target using bottom-up post-order DFS."""
    if not root:
        return None

    # Post-order: Process subtrees first (bottom-up pruning)
    root.left = remove_leaf_nodes(root.left, target)
    root.right = remove_leaf_nodes(root.right, target)

    # If current node becomes a leaf and matches target, delete it
    if not root.left and not root.right and root.val == target:
        return None

    return root


# LeetCode backward compatibility aliases
removeLeafNodes = remove_leaf_nodes
delete_leaves = remove_leaf_nodes
