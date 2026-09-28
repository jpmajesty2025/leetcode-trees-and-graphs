import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from minimum_distance_between_bst_nodes import min_diff_in_bst as min_diff_dfs
from minimum_distance_between_bst_nodes_iterative import min_diff_in_bst_iterative
from minimum_distance_between_bst_nodes_morris import min_diff_in_bst_morris

SOLUTIONS = [
    min_diff_dfs,
    min_diff_in_bst_iterative,
    min_diff_in_bst_morris,
]


# --- Helper to construct BST from sorted list ---

def sorted_list_to_bst(arr: List[int]) -> Optional[TreeNode]:
    if not arr:
        return None
    mid = len(arr) // 2
    root = TreeNode(arr[mid])
    root.left = sorted_list_to_bst(arr[:mid])
    root.right = sorted_list_to_bst(arr[mid + 1:])
    return root


# --- Independent Reference Oracle ---

def oracle_min_diff(root: Optional[TreeNode]) -> int:
    """Independent brute force oracle collecting all values."""
    if not root:
        return 0
    values: list[int] = []

    def collect(node: Optional[TreeNode]):
        if not node:
            return
        values.append(node.val)
        collect(node.left)
        collect(node.right)

    collect(root)
    if len(values) < 2:
        return 0
    values.sort()
    return min(values[i] - values[i - 1] for i in range(1, len(values)))


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_or_single_node(fn):
    assert fn(None) == 0
    assert fn(TreeNode(42)) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [4,2,6,1,3] -> 1
    root = TreeNode(4,
        left=TreeNode(2, left=TreeNode(1), right=TreeNode(3)),
        right=TreeNode(6)
    )
    assert fn(root) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [1,0,48,null,null,12,49] -> 1
    root = TreeNode(1,
        left=TreeNode(0),
        right=TreeNode(48, left=TreeNode(12), right=TreeNode(49))
    )
    assert fn(root) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_node_tree(fn):
    root = TreeNode(10, right=TreeNode(25))
    assert fn(root) == 15


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_negative_values(fn):
    root = TreeNode(-50, left=TreeNode(-100), right=TreeNode(-20))
    assert fn(root) == 30


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_left_skewed_bst(fn):
    root = TreeNode(5, left=TreeNode(4, left=TreeNode(3, left=TreeNode(2, left=TreeNode(1)))))
    assert fn(root) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_large_gap_skewed_bst(fn):
    root = TreeNode(100, right=TreeNode(200, right=TreeNode(500)))
    assert fn(root) == 100


# --- Hypothesis Property-Based Tests ---

@given(
    values=st.lists(
        st.integers(min_value=-1000, max_value=1000),
        min_size=2,
        max_size=35,
        unique=True
    )
)
def test_hypothesis_matches_oracle(values):
    bst = sorted_list_to_bst(sorted(values))
    expected = oracle_min_diff(bst)
    for fn in SOLUTIONS:
        assert fn(bst) == expected


@given(
    values=st.lists(
        st.integers(min_value=-1000, max_value=1000),
        min_size=2,
        max_size=35,
        unique=True
    )
)
def test_hypothesis_strictly_positive(values):
    bst = sorted_list_to_bst(sorted(values))
    for fn in SOLUTIONS:
        res = fn(bst)
        assert res > 0
