'''
Given a binary tree with the following rules:

root.val == 0
For any treeNode:
If treeNode.val has a value x and treeNode.left != null, then treeNode.left.val == 2 * x + 1
If treeNode.val has a value x and treeNode.right != null, then treeNode.right.val == 2 * x + 2
Now the binary tree is contaminated, which means all treeNode.val have been changed to -1.

Implement the FindElements class:

FindElements(TreeNode* root) Initializes the object with a contaminated binary tree and recovers it.
bool find(int target) Returns true if the target value exists in the recovered binary tree.
'''

from tree_node import TreeNode


class FindElements:
    """Recovers a contaminated binary tree and provides O(1) target queries using a hash set."""

    def __init__(self, root: TreeNode | None):
        self.seen: set[int] = set()

        def recover(node: TreeNode | None, val: int) -> None:
            if not node:
                return
            node.val = val
            self.seen.add(val)
            recover(node.left, 2 * val + 1)
            recover(node.right, 2 * val + 2)

        if root:
            recover(root, 0)

    def find(self, target: int) -> bool:
        """Return True if target exists in the recovered tree in O(1) time."""
        return target in self.seen
