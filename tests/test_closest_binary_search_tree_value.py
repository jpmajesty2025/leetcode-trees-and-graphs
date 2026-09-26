import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from closest_binary_search_tree_value import closest_value
from closest_binary_search_tree_value_recursive import closest_value_recursive

SOLUTIONS = [
    closest_value,
    closest_value_recursive,
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


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    assert fn(None, 3.14) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    root = TreeNode(10)
    assert fn(root, 10.0) == 10
    assert fn(root, 100.5) == 10
    assert fn(root, -50.0) == 10


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_exact_match(fn):
    # [4, 2, 5, 1, 3], target = 3.0 -> 3
    root = build_tree_from_list([4, 2, 5, 1, 3])
    assert fn(root, 3.0) == 3
    assert fn(root, 5.0) == 5
    assert fn(root, 1.0) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [4, 2, 5, 1, 3], target = 3.714286 -> 4
    root = build_tree_from_list([4, 2, 5, 1, 3])
    assert fn(root, 3.714286) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [1], target = 4.428571 -> 1
    root = TreeNode(1)
    assert fn(root, 4.428571) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_tie_breaking_picks_smaller_value(fn):
    # Tree: [2, 1, 3], target = 1.5 -> distance to 1 is 0.5, distance to 2 is 0.5
    # Smaller value (1) must be selected
    root1 = build_tree_from_list([2, 1, 3])
    assert fn(root1, 1.5) == 1

    # Tree: [4, 2, 5, 1, 3], target = 3.5 -> distance to 3 is 0.5, distance to 4 is 0.5
    # Smaller value (3) must be selected
    root2 = build_tree_from_list([4, 2, 5, 1, 3])
    assert fn(root2, 3.5) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_tie_breaking_with_negative_values(fn):
    # [-20, -30, -10], target = -15.0 -> distance to -20 is 5.0, distance to -10 is 5.0
    # Smaller value (-20) must be selected
    root = build_tree_from_list([-20, -30, -10])
    assert fn(root, -15.0) == -20


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_skewed_chains(fn):
    # Left-skewed: 5 -> 4 -> 3 -> 2 -> 1
    left_skewed = TreeNode(5, left=TreeNode(4, left=TreeNode(3, left=TreeNode(2, left=TreeNode(1)))))
    assert fn(left_skewed, 2.4) == 2
    assert fn(left_skewed, 0.0) == 1
    assert fn(left_skewed, 10.0) == 5

    # Right-skewed: 1 -> 2 -> 3 -> 4 -> 5
    right_skewed = TreeNode(1, right=TreeNode(2, right=TreeNode(3, right=TreeNode(4, right=TreeNode(5)))))
    assert fn(right_skewed, 3.6) == 4
    assert fn(right_skewed, 6.0) == 5
    assert fn(right_skewed, -1.0) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_large_gap_boundary(fn):
    # [100, 1, 200], target = 50.49 -> closer to 1 (gap 49.49) vs 100 (gap 49.51)
    root = build_tree_from_list([100, 1, 200])
    assert fn(root, 50.49) == 1
    assert fn(root, 50.51) == 100


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


def oracle_closest_value(root: Optional[TreeNode], target: float) -> int:
    """Independent brute-force oracle collecting all node values and finding the lexicographical minimum."""
    if not root:
        return 0
    values: List[int] = []

    def collect(node: Optional[TreeNode]):
        if not node:
            return
        values.append(node.val)
        collect(node.left)
        collect(node.right)

    collect(root)
    # Pick value minimizing distance |v - target|, breaking ties with smaller v
    return min(values, key=lambda v: (abs(v - target), v))


@given(
    values=st.lists(
        st.integers(min_value=-1000, max_value=1000),
        min_size=1,
        max_size=40,
        unique=True
    ),
    target=st.floats(min_value=-2000.0, max_value=2000.0, allow_nan=False, allow_infinity=False)
)
def test_closest_value_hypothesis(values, target):
    tree = sorted_list_to_bst(sorted(values))
    expected = oracle_closest_value(tree, target)
    for fn in SOLUTIONS:
        assert fn(tree, target) == expected
