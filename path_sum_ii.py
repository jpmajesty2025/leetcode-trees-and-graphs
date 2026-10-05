'''
Given the root of a binary tree and an integer targetSum, return all root-to-leaf paths where the 
sum of the node values in the path equals targetSum. Each path should be returned as a list of the 
node values, not node references.

A root-to-leaf path is a path starting from the root and ending at any leaf node. A leaf is a node 
with no children.
'''

from tree_node import TreeNode


def path_sum(root: TreeNode | None, target_sum: int) -> list[list[int]]:
    """Return all root-to-leaf paths equaling target_sum using backtracking DFS."""
    result: list[list[int]] = []
    current_path: list[int] = []

    def dfs(node: TreeNode | None, remaining: int) -> None:
        if not node:
            return

        current_path.append(node.val)
        remaining -= node.val

        # Leaf node check
        if not node.left and not node.right and remaining == 0:
            result.append(list(current_path))
        else:
            dfs(node.left, remaining)
            dfs(node.right, remaining)

        current_path.pop()  # Backtrack

    dfs(root, target_sum)
    return result


# LeetCode backward compatibility aliases
pathSum = path_sum
