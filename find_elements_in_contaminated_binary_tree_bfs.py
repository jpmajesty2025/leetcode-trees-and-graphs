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

from collections import deque
from tree_node import TreeNode


class FindElementsBFS:
    """Recovers a contaminated binary tree using iterative BFS for stack safety."""

    def __init__(self, root: TreeNode | None):
        self.seen: set[int] = set()
        if not root:
            return

        root.val = 0
        self.seen.add(0)
        queue = deque([root])

        while queue:
            curr = queue.popleft()
            val = curr.val

            if curr.left:
                curr.left.val = 2 * val + 1
                self.seen.add(curr.left.val)
                queue.append(curr.left)

            if curr.right:
                curr.right.val = 2 * val + 2
                self.seen.add(curr.right.val)
                queue.append(curr.right)

    def find(self, target: int) -> bool:
        """Return True if target exists in the recovered tree in O(1) time."""
        return target in self.seen


# Alias
FindElements = FindElementsBFS
