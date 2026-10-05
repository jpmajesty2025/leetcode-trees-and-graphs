'''
Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric 
around its center).
'''

from tree_node import TreeNode


def is_symmetric(root: TreeNode | None) -> bool:
    """Check if a binary tree is symmetric around its center using recursive DFS."""
    if not root:
        return True

    def is_mirror(t1: TreeNode | None, t2: TreeNode | None) -> bool:
        if not t1 and not t2:
            return True
        if not t1 or not t2:
            return False
        return (
            t1.val == t2.val
            and is_mirror(t1.left, t2.right)
            and is_mirror(t1.right, t2.left)
        )

    return is_mirror(root.left, root.right)


# LeetCode backward compatibility aliases
isSymmetric = is_symmetric
