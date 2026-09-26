import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from minimum_absolute_difference_in_bst import get_minimum_difference
from minimum_absolute_difference_in_bst_iterative import get_minimum_difference_iterative

SOLUTIONS = [
    get_minimum_difference,
    get_minimum_difference_iterative,
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
def test_empty_or_single_node(fn):
    assert fn(None) == 0
    assert fn(TreeNode(10)) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_nodes(fn):
    root = TreeNode(1, right=TreeNode(3))
    assert fn(root) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [4, 2, 6, 1, 3] -> 1
    root = build_tree_from_list([4, 2, 6, 1, 3])
    assert fn(root) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [1, 0, 48, null, null, 12, 49] -> 1
    root = build_tree_from_list([1, 0, 48, None, None, 12, 49])
    assert fn(root) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_left_skewed_chain(fn):
    # 5 -> 4 -> 3 -> 2 -> 1
    root = TreeNode(5, left=TreeNode(4, left=TreeNode(3, left=TreeNode(2, left=TreeNode(1)))))
    assert fn(root) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_right_skewed_chain(fn):
    # 1 -> 10 -> 100 -> 1000
    root = TreeNode(1, right=TreeNode(10, right=TreeNode(100, right=TreeNode(1000))))
    assert fn(root) == 9  # 10 - 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_large_gap_with_single_close_pair(fn):
    # [50, 10, 90, 8, 12] -> min difference is 2 (10-8 or 12-10)
    root = build_tree_from_list([50, 10, 90, 8, 12])
    assert fn(root) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_negative_values(fn):
    # [-10, -20, 0, -30, -15] -> min difference is 5 (-15 - (-20) = 5)
    root = build_tree_from_list([-10, -20, 0, -30, -15])
    assert fn(root) == 5


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
    st.integers(min_value=-1000, max_value=1000),
    unique=True,
    min_size=2,
    max_size=30
).map(sorted).map(sorted_list_to_bst)


def oracle_min_diff(root: Optional[TreeNode]) -> int:
    """Independent oracle collecting all values and finding minimum difference."""
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
    nodes.sort()
    return min(nodes[i] - nodes[i - 1] for i in range(1, len(nodes)))


@given(tree=bst_strategy)
def test_matches_oracle(tree):
    expected = oracle_min_diff(tree)
    for fn in SOLUTIONS:
        assert fn(tree) == expected
