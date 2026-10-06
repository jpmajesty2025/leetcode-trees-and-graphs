import pytest
from hypothesis import given, strategies as st
from typing import Optional, List
from collections import deque

from tree_node import TreeNode
from search_in_bst import search_bst as search_bst_iterative
from search_in_bst_recursive import search_bst_recursive

SOLUTIONS = [
    search_bst_iterative,
    search_bst_recursive,
]


def build_bst_from_sorted_list(nums: List[int]) -> Optional[TreeNode]:
    """Helper to build a balanced BST from a sorted list of unique integers."""
    if not nums:
        return None
    mid = len(nums) // 2
    root = TreeNode(nums[mid])
    root.left = build_bst_from_sorted_list(nums[:mid])
    root.right = build_bst_from_sorted_list(nums[mid + 1:])
    return root


def build_tree_from_list(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Helper to build a binary tree from level-order list representation with None values."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        current = queue.popleft()
        if i < len(values) and values[i] is not None:
            current.left = TreeNode(values[i])
            queue.append(current.left)
        i += 1
        if i < len(values) and values[i] is not None:
            current.right = TreeNode(values[i])
            queue.append(current.right)
        i += 1
    return root


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    assert fn(None, 10) is None


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_found(fn):
    root = TreeNode(42)
    res = fn(root, 42)
    assert res is not None
    assert res.val == 42


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_not_found(fn):
    root = TreeNode(42)
    assert fn(root, 10) is None


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # root = [4,2,7,1,3], val = 2 -> returns node 2 with left=1, right=3
    root = build_tree_from_list([4, 2, 7, 1, 3])
    res = fn(root, 2)
    assert res is not None
    assert res.val == 2
    assert res.left is not None and res.left.val == 1
    assert res.right is not None and res.right.val == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # root = [4,2,7,1,3], val = 5 -> None
    root = build_tree_from_list([4, 2, 7, 1, 3])
    assert fn(root, 5) is None


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_find_root_node(fn):
    root = build_tree_from_list([4, 2, 7, 1, 3])
    res = fn(root, 4)
    assert res is root


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_find_leaf_node(fn):
    root = build_tree_from_list([4, 2, 7, 1, 3])
    res = fn(root, 7)
    assert res is not None
    assert res.val == 7
    assert res.left is None
    assert res.right is None


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_skewed_left_bst(fn):
    # 5 -> 4 -> 3 -> 2 -> 1
    root = TreeNode(5, left=TreeNode(4, left=TreeNode(3, left=TreeNode(2, left=TreeNode(1)))))
    res = fn(root, 3)
    assert res is not None
    assert res.val == 3
    assert fn(root, 10) is None


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_skewed_right_bst(fn):
    # 1 -> 2 -> 3 -> 4 -> 5
    root = TreeNode(1, right=TreeNode(2, right=TreeNode(3, right=TreeNode(4, right=TreeNode(5)))))
    res = fn(root, 4)
    assert res is not None
    assert res.val == 4
    assert fn(root, 0) is None


# --- Hypothesis Property-Based Tests ---

@given(
    nums=st.lists(st.integers(min_value=-1000, max_value=1000), unique=True, min_size=1, max_size=30),
    data=st.data()
)
def test_bst_search_properties(nums, data):
    sorted_nums = sorted(nums)
    root = build_bst_from_sorted_list(sorted_nums)

    # Pick an element guaranteed to be in the tree
    target_in_tree = data.draw(st.sampled_from(sorted_nums))
    for fn in SOLUTIONS:
        res = fn(root, target_in_tree)
        assert res is not None
        assert res.val == target_in_tree

    # Pick a value not in the tree
    target_not_in_tree = data.draw(st.integers(min_value=-2000, max_value=2000).filter(lambda x: x not in sorted_nums))
    for fn in SOLUTIONS:
        assert fn(root, target_not_in_tree) is None
