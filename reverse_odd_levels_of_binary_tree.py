'''
Given the root of a perfect binary tree, reverse the node values at each odd level of the tree.

For example, suppose the node values at level 3 are [2,1,3,4,7,11,29,18], then it should 
become [18,29,11,7,4,3,1,2].
Return the root of the reversed tree.

A binary tree is perfect if all parent nodes have two children and all leaves are on the same level.
The level of a node is the number of edges along the path between it and the root node.
'''

from tree_node import TreeNode


def reverse_odd_levels(root: TreeNode | None) -> TreeNode | None:
    """Reverse node values at odd levels using symmetric dual-pointer DFS."""
    if not root or not root.left:
        return root

    def dfs(
        node_left: TreeNode | None, node_right: TreeNode | None, is_odd: bool
    ) -> None:
        if not node_left or not node_right:
            return

        if is_odd:
            node_left.val, node_right.val = node_right.val, node_left.val

        # Recurse symmetrically: outer pair and inner pair
        dfs(node_left.left, node_right.right, not is_odd)
        dfs(node_left.right, node_right.left, not is_odd)

    dfs(root.left, root.right, True)
    return root


# LeetCode backward compatibility aliases
reverseOddLevels = reverse_odd_levels
