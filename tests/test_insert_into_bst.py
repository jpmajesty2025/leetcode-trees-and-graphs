import pytest
from hypothesis import given, strategies as st
from typing import Optional, List, Set
import copy

from tree_node import TreeNode
from insert_into_bst import insert_into_bst
from insert_into_bst_iterative import insert_into_bst_iterative

SOLUTIONS = [
    insert_into_bst,
    insert_into_bst_iterative,
]


def build_tree_from_list(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Helper to build a binary tree from level-order list representation with None for empty children."""
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


def clone_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """Helper to deeply clone a binary tree."""
    if not root:
        return None
    new_node = TreeNode(root.val)
    new_node.left = clone_tree(root.left)
    new_node.right = clone_tree(root.right)
    return new_node


def tree_to_inorder(root: Optional[TreeNode]) -> List[int]:
    """Helper to collect in-order traversal of a tree."""
    values: List[int] = []

    def dfs(node: Optional[TreeNode]):
        if not node:
            return
        dfs(node.left)
        values.append(node.val)
        dfs(node.right)

    dfs(root)
    return values


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """Helper to check if a tree is a valid BST."""
    vals = tree_to_inorder(root)
    return all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    result = fn(None, 5)
    assert result is not None
    assert result.val == 5
    assert result.left is None
    assert result.right is None


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_left_insert(fn):
    root = TreeNode(10)
    result = fn(root, 5)
    assert result.val == 10
    assert result.left is not None
    assert result.left.val == 5
    assert result.right is None
    assert is_valid_bst(result)


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_right_insert(fn):
    root = TreeNode(10)
    result = fn(root, 15)
    assert result.val == 10
    assert result.right is not None
    assert result.right.val == 15
    assert result.left is None
    assert is_valid_bst(result)


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [4, 2, 7, 1, 3], val = 5
    root = build_tree_from_list([4, 2, 7, 1, 3])
    result = fn(root, 5)
    assert is_valid_bst(result)
    assert set(tree_to_inorder(result)) == {1, 2, 3, 4, 5, 7}
    # Specifically, 5 should be attached to left of 7
    assert result.right.left is not None
    assert result.right.left.val == 5


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [40, 20, 60, 10, 30, 50, 70], val = 25
    root = build_tree_from_list([40, 20, 60, 10, 30, 50, 70])
    result = fn(root, 25)
    assert is_valid_bst(result)
    assert set(tree_to_inorder(result)) == {10, 20, 25, 30, 40, 50, 60, 70}
    # 25 should be left child of 30
    assert result.left.right.left is not None
    assert result.left.right.left.val == 25


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_left_skewed_chain_insert_smallest(fn):
    # 5 -> 4 -> 3 -> 2, insert 1
    root = TreeNode(5, left=TreeNode(4, left=TreeNode(3, left=TreeNode(2))))
    result = fn(root, 1)
    assert is_valid_bst(result)
    assert tree_to_inorder(result) == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_right_skewed_chain_insert_largest(fn):
    # 1 -> 2 -> 3 -> 4, insert 5
    root = TreeNode(1, right=TreeNode(2, right=TreeNode(3, right=TreeNode(4))))
    result = fn(root, 5)
    assert is_valid_bst(result)
    assert tree_to_inorder(result) == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_negative_values(fn):
    # [-20, -30, -10], insert -25
    root = build_tree_from_list([-20, -30, -10])
    result = fn(root, -25)
    assert is_valid_bst(result)
    assert tree_to_inorder(result) == [-30, -25, -20, -10]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_boundary_int_values(fn):
    min_int = -2147483648
    max_int = 2147483647
    root = TreeNode(0)
    root = fn(root, min_int)
    root = fn(root, max_int)
    assert is_valid_bst(root)
    assert tree_to_inorder(root) == [min_int, 0, max_int]


# --- Hypothesis Property-Based Tests ---

def sorted_list_to_bst(arr: List[int]) -> Optional[TreeNode]:
    """Helper to convert a sorted array of unique ints to a balanced BST."""
    if not arr:
        return None
    mid = len(arr) // 2
    root = TreeNode(arr[mid])
    root.left = sorted_list_to_bst(arr[:mid])
    root.right = sorted_list_to_bst(arr[mid + 1:])
    return root


@given(
    values=st.lists(
        st.integers(min_value=-10000, max_value=10000),
        min_size=0,
        max_size=30,
        unique=True
    ),
    insert_val=st.integers(min_value=-10000, max_value=10000)
)
def test_insert_into_bst_hypothesis(values, insert_val):
    # Ensure insert_val is not already in values per problem guarantee
    if insert_val in values:
        values.remove(insert_val)

    sorted_vals = sorted(values)
    expected_values = sorted(sorted_vals + [insert_val])

    for fn in SOLUTIONS:
        tree = sorted_list_to_bst(sorted_vals)
        result = fn(tree, insert_val)

        # 1. Result must not be None
        assert result is not None

        # 2. Result must be a valid BST
        inorder = tree_to_inorder(result)
        assert is_valid_bst(result)

        # 3. In-order traversal must match sorted original values + inserted value
        assert inorder == expected_values
        assert len(inorder) == len(sorted_vals) + 1
