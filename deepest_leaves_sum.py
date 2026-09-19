'''
Given the root of a binary tree, return the sum of values of its deepest leaves.
'''

from collections import deque
from tree_node import TreeNode


def deepest_leaves_sum(root: TreeNode | None) -> int:
    if not root:
        return 0

    queue = deque([root])
    deepest_sum = 0

    while queue:
        deepest_sum = 0
        for _ in range(len(queue)):
            node = queue.popleft()
            deepest_sum += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return deepest_sum
