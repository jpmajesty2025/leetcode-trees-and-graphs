'''
Given the root of a binary tree and an integer targetSum, return the number of paths where the sum 
of the values along the path equals targetSum.

The path does not need to start or end at the root or a leaf, but it must go downwards 
(i.e., traveling only from parent nodes to child nodes).
'''

from collections import defaultdict
from tree_node import TreeNode


def path_sum(root: TreeNode | None, target_sum: int) -> int:
    """Return the number of downward paths summing to target_sum using prefix sum DFS."""
    prefix_counts: dict[int, int] = defaultdict(int)
    prefix_counts[0] = 1  # Base case: empty path sum of 0

    def dfs(node: TreeNode | None, current_sum: int) -> int:
        if not node:
            return 0

        current_sum += node.val
        # Number of valid sub-paths ending at current node
        valid_paths = prefix_counts[current_sum - target_sum]

        # Register current prefix sum
        prefix_counts[current_sum] += 1

        # Explore subtrees
        valid_paths += dfs(node.left, current_sum)
        valid_paths += dfs(node.right, current_sum)

        # Backtrack prefix count to avoid leaking into sibling branches
        prefix_counts[current_sum] -= 1

        return valid_paths

    return dfs(root, 0)


# LeetCode backward compatibility aliases
pathSum = path_sum
