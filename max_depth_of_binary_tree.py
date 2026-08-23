'''
Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path 
from the root node down to the farthest leaf node.
'''

from collections import deque
from typing import Optional
from tree_node import TreeNode


def max_depth(root: Optional[TreeNode]) -> int:
    """
    Calculate maximum depth using recursive Depth-First Search (DFS).

    Time Complexity: O(N) where N is the number of nodes.
    Space Complexity: O(H) where H is the height of the tree (call stack).
    """
    if not root:
        return 0

    left = max_depth(root.left)
    right = max_depth(root.right)
    return max(left, right) + 1


def max_depth_iterative(root: Optional[TreeNode]) -> int:
    """
    Calculate maximum depth using iterative Depth-First Search (DFS) with an explicit stack.

    Time Complexity: O(N) where N is the number of nodes.
    Space Complexity: O(H) where H is the height of the tree.
    """
    if not root:
        return 0

    stack = [(root, 1)]
    ans = 0

    while stack:
        node, depth = stack.pop()
        ans = max(ans, depth)
        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))

    return ans


def max_depth_bfs(root: Optional[TreeNode]) -> int:
    """
    Calculate maximum depth using iterative Breadth-First Search (BFS) / Level-Order Traversal.

    Time Complexity: O(N) where N is the number of nodes.
    Space Complexity: O(W) where W is the maximum width of the tree (up to N/2).
    """
    if not root:
        return 0

    queue = deque([root])
    depth = 0

    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return depth
