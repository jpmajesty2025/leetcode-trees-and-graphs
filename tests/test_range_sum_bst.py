import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from range_sum_bst import range_sum_bst
from range_sum_bst_iterative import range_sum_bst_iterative

SOLUTIONS = [
    range_sum_bst,
    range_sum_bst_iterative,
]


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


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    assert fn(None, 5, 10) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_in_range(fn):
    root = TreeNode(7)
    assert fn(root, 5, 10) == 7


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_below_range(fn):
    root = TreeNode(3)
    assert fn(root, 5, 10) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_above_range(fn):
    root = TreeNode(15)
    assert fn(root, 5, 10) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [10, 5, 15, 3, 7, null, 18], low = 7, high = 15 -> 32
    root = build_tree_from_list([10, 5, 15, 3, 7, None, 18])
    assert fn(root, 7, 15) == 32


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [10, 5, 15, 3, 7, 13, 18, 1, null, 6], low = 6, high = 10 -> 23
    root = build_tree_from_list([10, 5, 15, 3, 7, 13, 18, 1, None, 6])
    assert fn(root, 6, 10) == 23


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_low_equals_high(fn):
    root = build_tree_from_list([10, 5, 15, 3, 7, None, 18])
    assert fn(root, 7, 7) == 7
    assert fn(root, 12, 12) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_nodes_in_range(fn):
    root = build_tree_from_list([10, 5, 15, 3, 7, None, 18])
    # 10 + 5 + 15 + 3 + 7 + 18 = 58
    assert fn(root, 1, 100) == 58


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_nodes_outside_range(fn):
    root = build_tree_from_list([10, 5, 15, 3, 7, None, 18])
    assert fn(root, 20, 30) == 0
    assert fn(root, 0, 2) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_skewed_bst(fn):
    # Skewed right: 1 -> 2 -> 3 -> 4 -> 5
    root = TreeNode(1, right=TreeNode(2, right=TreeNode(3, right=TreeNode(4, right=TreeNode(5)))))
    assert fn(root, 2, 4) == 2 + 3 + 4


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


bst_strategy = st.lists(
    st.integers(min_value=-500, max_value=500),
    unique=True,
    max_size=30
).map(sorted).map(sorted_list_to_bst)


def oracle_range_sum_bst(root: Optional[TreeNode], low: int, high: int) -> int:
    """Independent oracle that visits all nodes without pruning."""
    if not root:
        return 0
    nodes = []

    def collect(node: Optional[TreeNode]):
        if not node:
            return
        nodes.append(node.val)
        collect(node.left)
        collect(node.right)

    collect(root)
    return sum(v for v in nodes if low <= v <= high)


@given(
    tree=bst_strategy,
    low=st.integers(min_value=-600, max_value=600),
    high=st.integers(min_value=-600, max_value=600)
)
def test_matches_oracle(tree, low, high):
    if low > high:
        low, high = high, low
    expected = oracle_range_sum_bst(tree, low, high)
    for fn in SOLUTIONS:
        assert fn(tree, low, high) == expected
