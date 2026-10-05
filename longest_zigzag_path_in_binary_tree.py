'''
You are given the root of a binary tree.

A ZigZag path for a binary tree is defined as follow:
Choose any node in the binary tree and a direction (right or left).
If the current direction is right, move to the right child of the current node; otherwise, 
move to the left child.
Change the direction from right to left or from left to right.
Repeat the second and third steps until you can't move in the tree.
Zigzag length is defined as the number of nodes visited - 1. (A single node has a length of 0).

Return the longest ZigZag path contained in that tree.
'''

from tree_node import TreeNode


def longest_zig_zag(root: TreeNode | None) -> int:
    """Return the length of the longest ZigZag path using top-down DFS."""
    if not root:
        return 0

    max_len = 0

    # go_left: True if the next valid zigzag step should be to the left child
    def dfs(node: TreeNode | None, go_left: bool, length: int) -> None:
        nonlocal max_len
        if not node:
            return

        max_len = max(max_len, length)

        if go_left:
            dfs(node.left, False, length + 1)  # Continue zigzag
            dfs(node.right, True, 1)  # Restart zigzag from current node
        else:
            dfs(node.right, True, length + 1)  # Continue zigzag
            dfs(node.left, False, 1)  # Restart zigzag from current node

    if root.left:
        dfs(root.left, False, 1)  # Step left, expect right next
    if root.right:
        dfs(root.right, True, 1)  # Step right, expect left next

    return max_len


# LeetCode backward compatibility aliases
longestZigZag = longest_zig_zag
