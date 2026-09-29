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


class FindElementsBinaryPath:
    """Navigates recovered binary tree in O(H) time using binary bit representation of target + 1."""

    def __init__(self, root: TreeNode | None):
        self.root = root

        def recover(node: TreeNode | None, val: int) -> None:
            if not node:
                return
            node.val = val
            recover(node.left, 2 * val + 1)
            recover(node.right, 2 * val + 2)

        if root:
            recover(root, 0)

    def find(self, target: int) -> bool:
        """Navigate to target in O(H) time without extra hash set memory."""
        if not self.root or target < 0:
            return False

        # target + 1 in binary (strip the MSB '0b1')
        path = bin(target + 1)[3:]
        curr = self.root

        for bit in path:
            if bit == '0':
                curr = curr.left
            else:
                curr = curr.right
            if not curr:
                return False

        return True


# Alias
FindElements = FindElementsBinaryPath
