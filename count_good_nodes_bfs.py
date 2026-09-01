'''
Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with a value greater than X.

Return the number of good nodes in the binary tree
'''
from collections import deque
from typing import Optional
from tree_node import TreeNode


def good_nodes_bfs(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    count = 0
    queue = deque([(root, root.val)])

    while queue:
        node, max_val = queue.popleft()
        if node.val >= max_val:
            count += 1
            max_val = node.val

        if node.left:
            queue.append((node.left, max_val))
        if node.right:
            queue.append((node.right, max_val))

    return count
