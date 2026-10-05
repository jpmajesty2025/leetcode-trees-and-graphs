'''
Given a binary tree root and an integer target, delete all the leaf nodes with value target.

This module implements the iterative post-order traversal using an explicit stack
and a dummy parent node to prune leaves bottom-up without recursion.
'''

from tree_node import TreeNode


def remove_leaf_nodes_iterative(
    root: TreeNode | None, target: int
) -> TreeNode | None:
    """Remove all leaf nodes with value target using iterative post-order traversal."""
    dummy = TreeNode(0)
    dummy.left = root

    stack: list[TreeNode] = []
    curr: TreeNode | None = dummy
    last_visited: TreeNode | None = None

    while stack or curr:
        if curr:
            stack.append(curr)
            curr = curr.left
        else:
            peek_node = stack[-1]
            if peek_node.right and last_visited != peek_node.right:
                curr = peek_node.right
            else:
                # Post-order: children of peek_node are already processed
                if (
                    peek_node.left
                    and not peek_node.left.left
                    and not peek_node.left.right
                    and peek_node.left.val == target
                ):
                    peek_node.left = None

                if (
                    peek_node.right
                    and not peek_node.right.left
                    and not peek_node.right.right
                    and peek_node.right.val == target
                ):
                    peek_node.right = None

                last_visited = stack.pop()

    return dummy.left


# Aliases
remove_leaf_nodes = remove_leaf_nodes_iterative
removeLeafNodes = remove_leaf_nodes_iterative
delete_leaves = remove_leaf_nodes_iterative
