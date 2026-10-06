import pytest
from hypothesis import given, strategies as st
from typing import Optional, List
from collections import deque

from tree_node import TreeNode
from average_of_levels_in_binary_tree import average_of_levels as average_of_levels_bfs
from average_of_levels_in_binary_tree_dfs import average_of_levels_dfs
from average_of_levels_in_binary_tree_iterative import average_of_levels_iterative

SOLUTIONS = [
    average_of_levels_bfs,
    average_of_levels_dfs,
    average_of_levels_iterative,
]


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
    assert fn(None) == []


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    root = TreeNode(42)
    assert fn(root) == pytest.approx([42.0])


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [3, 9, 20, None, None, 15, 7] -> [3.0, 14.5, 11.0]
    root = build_tree_from_list([3, 9, 20, None, None, 15, 7])
    assert fn(root) == pytest.approx([3.0, 14.5, 11.0])


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [3, 9, 20, 15, 7] -> [3.0, 14.5, 11.0]
    root = build_tree_from_list([3, 9, 20, 15, 7])
    assert fn(root) == pytest.approx([3.0, 14.5, 11.0])


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_negative_and_zero_values(fn):
    # Level 0: 0 -> avg 0.0
    # Level 1: -10, 10 -> avg 0.0
    # Level 2: -30, -10 -> avg -20.0
    root = build_tree_from_list([0, -10, 10, -30, -10, None, None])
    assert fn(root) == pytest.approx([0.0, 0.0, -20.0])


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_left_skewed_tree(fn):
    root = TreeNode(10, left=TreeNode(20, left=TreeNode(30, left=TreeNode(40))))
    assert fn(root) == pytest.approx([10.0, 20.0, 30.0, 40.0])


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_right_skewed_tree(fn):
    root = TreeNode(5, right=TreeNode(15, right=TreeNode(25)))
    assert fn(root) == pytest.approx([5.0, 15.0, 25.0])


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_precision_large_values(fn):
    # Large 32-bit integer boundaries
    v1 = 2147483647
    v2 = 2147483645
    root = build_tree_from_list([v1, v1, v2])
    expected = [float(v1), float((v1 + v2) / 2)]
    assert fn(root) == pytest.approx(expected, rel=1e-5, abs=1e-5)


# --- Hypothesis Property-Based Tests ---

tree_strategy = st.recursive(
    st.builds(TreeNode, val=st.integers(min_value=-10000, max_value=10000)),
    lambda children: st.builds(
        TreeNode,
        val=st.integers(min_value=-10000, max_value=10000),
        left=st.one_of(st.none(), children),
        right=st.one_of(st.none(), children),
    ),
    max_leaves=25
)


def oracle_average_of_levels(root: Optional[TreeNode]) -> List[float]:
    """Independent oracle collecting level sums and counts."""
    if not root:
        return []
    levels: List[List[int]] = []
    queue = deque([(root, 0)])
    while queue:
        node, depth = queue.popleft()
        if depth == len(levels):
            levels.append([])
        levels[depth].append(node.val)
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    return [sum(lvl) / len(lvl) for lvl in levels]


def get_tree_height(node: Optional[TreeNode]) -> int:
    if not node:
        return 0
    return 1 + max(get_tree_height(node.left), get_tree_height(node.right))


@given(tree=tree_strategy)
def test_matches_oracle(tree):
    expected = oracle_average_of_levels(tree)
    for fn in SOLUTIONS:
        res = fn(tree)
        assert len(res) == len(expected)
        assert res == pytest.approx(expected, rel=1e-5, abs=1e-5)


@given(tree=tree_strategy)
def test_length_matches_height(tree):
    h = get_tree_height(tree)
    for fn in SOLUTIONS:
        res = fn(tree)
        assert len(res) == h
