import pytest
from hypothesis import given, strategies as st
from collections import Counter
from typing import Optional, List

from tree_node import TreeNode
from find_mode_in_bst import find_mode as find_mode_dfs
from find_mode_in_bst_iterative import find_mode_iterative
from find_mode_in_bst_morris import find_mode_morris

SOLUTIONS = [
    find_mode_dfs,
    find_mode_iterative,
    find_mode_morris,
]


# --- Helper to construct BST with duplicates from sorted list ---

def sorted_list_to_bst_with_duplicates(arr: List[int]) -> Optional[TreeNode]:
    if not arr:
        return None
    mid = len(arr) // 2
    root = TreeNode(arr[mid])
    root.left = sorted_list_to_bst_with_duplicates(arr[:mid])
    root.right = sorted_list_to_bst_with_duplicates(arr[mid + 1:])
    return root


# --- Independent Reference Oracle ---

def oracle_find_mode(root: Optional[TreeNode]) -> List[int]:
    """Independent dictionary frequency count oracle."""
    if not root:
        return []
    counts: Counter = Counter()

    def collect(node: Optional[TreeNode]):
        if not node:
            return
        counts[node.val] += 1
        collect(node.left)
        collect(node.right)

    collect(root)
    if not counts:
        return []
    max_freq = max(counts.values())
    return sorted([val for val, freq in counts.items() if freq == max_freq])


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    assert fn(None) == []


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    assert fn(TreeNode(1)) == [1]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [1, null, 2, 2] -> [2]
    root = TreeNode(1, right=TreeNode(2, left=TreeNode(2)))
    assert sorted(fn(root)) == [2]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [0] -> [0]
    assert fn(TreeNode(0)) == [0]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_elements_unique_tie(fn):
    # [1, 2, 3] -> [1, 2, 3]
    root = TreeNode(2, left=TreeNode(1), right=TreeNode(3))
    assert sorted(fn(root)) == [1, 2, 3]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_multiple_modes_with_tie_frequency(fn):
    # BST with values [1, 1, 2, 3, 3] -> [1, 3] (freq 2)
    root = TreeNode(2,
        left=TreeNode(1, left=TreeNode(1)),
        right=TreeNode(3, right=TreeNode(3))
    )
    assert sorted(fn(root)) == [1, 3]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_elements_identical(fn):
    # 2 -> 2 -> 2 -> 2
    root = TreeNode(2, left=TreeNode(2, left=TreeNode(2, left=TreeNode(2))))
    assert fn(root) == [2]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_negative_values(fn):
    # [-2, -2, -1] -> [-2]
    root = TreeNode(-1, left=TreeNode(-2, left=TreeNode(-2)))
    assert fn(root) == [-2]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_deep_skewed_chain(fn):
    # Chain of 500 identical 7s
    n = 500
    root = TreeNode(7)
    curr = root
    for _ in range(n - 1):
        curr.left = TreeNode(7)
        curr = curr.left

    assert fn(root) == [7]


# --- Hypothesis Property-Based Tests ---

@given(
    values=st.lists(
        st.integers(min_value=-50, max_value=50),
        min_size=1,
        max_size=30
    )
)
def test_hypothesis_matches_oracle(values):
    bst = sorted_list_to_bst_with_duplicates(sorted(values))
    expected = oracle_find_mode(bst)
    for fn in SOLUTIONS:
        assert sorted(fn(bst)) == expected


@given(
    values=st.lists(
        st.integers(min_value=-50, max_value=50),
        min_size=1,
        max_size=30
    )
)
def test_hypothesis_modes_in_tree(values):
    bst = sorted_list_to_bst_with_duplicates(sorted(values))
    for fn in SOLUTIONS:
        res = fn(bst)
        assert len(res) >= 1
        for val in res:
            assert val in values
