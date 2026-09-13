'''
Given the root of a binary tree, find the maximum value v for which there exist different nodes a and b where 
v = |a.val - b.val| and a is an ancestor of b.

A node a is an ancestor of b if either: any child of a is equal to b or any child of a is an ancestor of b.
'''

from collections import deque
from typing import Optional
from tree_node import TreeNode


def max_ancestor_diff_bfs(root: Optional[TreeNode]) -> int:
    """Find the maximum difference |a.val - b.val| between ancestor a and descendant b using iterative BFS."""
    if not root:
        return 0

    max_diff = 0
    queue = deque([(root, root.val, root.val)])

    while queue:
        node, cur_min, cur_max = queue.popleft()
        cur_min = min(cur_min, node.val)
        cur_max = max(cur_max, node.val)

        if not node.left and not node.right:
            max_diff = max(max_diff, cur_max - cur_min)
            continue

        if node.left:
            queue.append((node.left, cur_min, cur_max))
        if node.right:
            queue.append((node.right, cur_min, cur_max))

    return max_diff
