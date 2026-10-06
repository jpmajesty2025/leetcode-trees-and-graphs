import pytest
from hypothesis import given, strategies as st
from typing import Optional, List
from collections import deque

from tree_node import TreeNode
from even_odd_tree import is_even_odd_tree as is_even_odd_tree_bfs
from even_odd_tree_dfs import is_even_odd_tree_dfs
from even_odd_tree_iterative import is_even_odd_tree_iterative

SOLUTIONS = [
    is_even_odd_tree_bfs,
    is_even_odd_tree_dfs,
    is_even_odd_tree_iterative,
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
    assert fn(None) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_odd(fn):
    assert fn(TreeNode(1)) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_even(fn):
    assert fn(TreeNode(2)) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [1, 10, 4, 3, None, 7, 9, 12, 8, 6, None, None, 2]
    # Level 0: [1] (odd, inc)
    # Level 1: [10, 4] (even, dec)
    # Level 2: [3, 7, 9] (odd, inc)
    # Level 3: [12, 8, 6, 2] (even, dec)
    root = build_tree_from_list([1, 10, 4, 3, None, 7, 9, 12, 8, 6, None, None, 2])
    assert fn(root) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [5, 4, 2, 3, 3, 7] -> Level 2 has [3, 3, 7] which is not strictly increasing
    root = build_tree_from_list([5, 4, 2, 3, 3, 7])
    assert fn(root) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    # [5, 9, 1, 3, 5, 7] -> Level 1 has [9, 1] which are odd instead of even
    root = build_tree_from_list([5, 9, 1, 3, 5, 7])
    assert fn(root) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_even_level_not_increasing(fn):
    # Level 0: [1]
    # Level 1: [10, 8]
    # Level 2: [9, 7] (decreasing on even level -> False)
    root = build_tree_from_list([1, 10, 8, 9, 7, None, None])
    assert fn(root) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_odd_level_not_decreasing(fn):
    # Level 0: [1]
    # Level 1: [4, 6] (increasing on odd level -> False)
    root = build_tree_from_list([1, 4, 6])
    assert fn(root) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_alternating_chain_valid(fn):
    # 1 (odd) -> 10 (even) -> 3 (odd) -> 4 (even)
    root = TreeNode(1, left=TreeNode(10, left=TreeNode(3, left=TreeNode(4))))
    assert fn(root) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_alternating_chain_invalid_parity(fn):
    # 1 (odd) -> 11 (odd at level 1 -> False)
    root = TreeNode(1, left=TreeNode(11))
    assert fn(root) is False


# --- Hypothesis Property-Based Tests ---

tree_strategy = st.recursive(
    st.builds(TreeNode, val=st.integers(min_value=1, max_value=100)),
    lambda children: st.builds(
        TreeNode,
        val=st.integers(min_value=1, max_value=100),
        left=st.one_of(st.none(), children),
        right=st.one_of(st.none(), children),
    ),
    max_leaves=20
)


def oracle_is_even_odd(root: Optional[TreeNode]) -> bool:
    """Independent oracle collecting nodes level-by-level and checking rules directly."""
    if not root:
        return True
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

    for depth, values in enumerate(levels):
        if depth % 2 == 0:
            # Even depth: must be odd and strictly increasing
            if any(v % 2 == 0 for v in values):
                return False
            for i in range(1, len(values)):
                if values[i] <= values[i - 1]:
                    return False
        else:
            # Odd depth: must be even and strictly decreasing
            if any(v % 2 != 0 for v in values):
                return False
            for i in range(1, len(values)):
                if values[i] >= values[i - 1]:
                    return False

    return True


@given(tree=tree_strategy)
def test_matches_oracle(tree):
    expected = oracle_is_even_odd(tree)
    for fn in SOLUTIONS:
        assert fn(tree) == expected
