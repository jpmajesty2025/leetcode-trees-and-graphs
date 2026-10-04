import pytest
import copy
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from recover_bst import recover_tree as recover_tree_morris
from recover_bst_iterative import recover_tree_iterative
from recover_bst_recursive import recover_tree_recursive

SOLUTIONS = [
    recover_tree_morris,
    recover_tree_iterative,
    recover_tree_recursive,
]


# --- Helpers ---

def build_tree_from_list(values: List[Optional[int]]) -> Optional[TreeNode]:
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        current = queue.pop(0)
        if i < len(values) and values[i] is not None:
            current.left = TreeNode(values[i])
            queue.append(current.left)
        i += 1
        if i < len(values) and values[i] is not None:
            current.right = TreeNode(values[i])
            queue.append(current.right)
        i += 1
    return root


def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    result = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)
    dfs(root)
    return result


def clone_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root:
        return None
    new_node = TreeNode(root.val)
    new_node.left = clone_tree(root.left)
    new_node.right = clone_tree(root.right)
    return new_node


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # Input: [1, 3, None, None, 2]
    # In-order before: [1, 3, 2] (3 and 2 were swapped? No, 1 and 3 were swapped, correct in-order is [1, 2, 3])
    root = TreeNode(1)
    root.left = TreeNode(3)
    root.left.right = TreeNode(2)
    
    fn(root)
    assert inorder_traversal(root) == [1, 2, 3]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # Input: [3, 1, 4, None, None, 2] -> in-order before: [1, 3, 2, 4]
    # Correct in-order: [1, 2, 3, 4] (3 and 2 swapped)
    root = TreeNode(3)
    root.left = TreeNode(1)
    root.right = TreeNode(4)
    root.right.left = TreeNode(2)

    fn(root)
    assert inorder_traversal(root) == [1, 2, 3, 4]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_node_tree(fn):
    # root = 2, left = 1 swapped -> root = 1, left = 2
    root = TreeNode(1)
    root.left = TreeNode(2)
    
    fn(root)
    assert inorder_traversal(root) == [1, 2]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_distant_swap(fn):
    # Valid BST in-order: [10, 20, 30, 40, 50]
    # Swap 10 and 50 -> in-order: [50, 20, 30, 40, 10]
    root = TreeNode(30)
    root.left = TreeNode(20)
    root.left.left = TreeNode(50)  # was 10
    root.right = TreeNode(40)
    root.right.right = TreeNode(10)  # was 50

    fn(root)
    assert inorder_traversal(root) == [10, 20, 30, 40, 50]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_adjacent_root_swap(fn):
    # Valid BST in-order: [10, 20, 30, 40]
    # Swap root 20 and right child 30 -> [10, 30, 20, 40]
    root = TreeNode(30)  # was 20
    root.left = TreeNode(10)
    root.right = TreeNode(20)  # was 30
    root.right.right = TreeNode(40)

    fn(root)
    assert inorder_traversal(root) == [10, 20, 30, 40]


# --- Hypothesis Property-Based Tests ---

def insert_into_bst(root: Optional[TreeNode], val: int) -> TreeNode:
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    elif val > root.val:
        root.right = insert_into_bst(root.right, val)
    return root


def get_all_nodes(root: Optional[TreeNode]) -> List[TreeNode]:
    nodes = []
    def dfs(node):
        if not node:
            return
        nodes.append(node)
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return nodes


@st.composite
def swapped_bst_strategy(draw):
    unique_vals = draw(st.lists(st.integers(min_value=-1000, max_value=1000), min_size=2, max_size=15, unique=True))
    root = None
    for v in unique_vals:
        root = insert_into_bst(root, v)

    nodes = get_all_nodes(root)
    idx1 = draw(st.integers(min_value=0, max_value=len(nodes) - 1))
    idx2 = draw(st.integers(min_value=0, max_value=len(nodes) - 1))
    if idx1 == idx2:
        idx2 = (idx1 + 1) % len(nodes)

    # Swap node values
    nodes[idx1].val, nodes[idx2].val = nodes[idx2].val, nodes[idx1].val
    expected_sorted = sorted(unique_vals)
    return root, expected_sorted


@given(data=swapped_bst_strategy())
def test_hypothesis_recovers_all_trees(data):
    root, expected_sorted = data
    for fn in SOLUTIONS:
        tree_copy = clone_tree(root)
        fn(tree_copy)
        assert inorder_traversal(tree_copy) == expected_sorted
