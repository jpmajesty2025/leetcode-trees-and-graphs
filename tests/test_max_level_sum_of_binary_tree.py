import pytest
from hypothesis import given, strategies as st
from typing import Optional, List
from collections import deque

from tree_node import TreeNode
from max_level_sum_of_binary_tree import max_level_sum as max_level_sum_bfs
from max_level_sum_of_binary_tree_dfs import max_level_sum_dfs
from max_level_sum_of_binary_tree_iterative import max_level_sum_iterative

SOLUTIONS = [
    max_level_sum_bfs,
    max_level_sum_dfs,
    max_level_sum_iterative,
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
    assert fn(None) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_positive(fn):
    root = TreeNode(50)
    assert fn(root) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_negative(fn):
    root = TreeNode(-100)
    assert fn(root) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # root = [1, 7, 0, 7, -8, null, null] -> Level 1: 1, Level 2: 7, Level 3: -1 -> max level 2
    root = build_tree_from_list([1, 7, 0, 7, -8, None, None])
    assert fn(root) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # root = [989, null, 10250, 98697, -34348, null, null, null, -89388]
    # Level 1: 989
    # Level 2: 10250
    # Level 3: 98697 + (-34348) = 64349
    # Level 4: -89388
    # Max sum is 64349 at level 3
    root = build_tree_from_list([989, None, 10250, 98697, -34348, None, None, None, -89388])
    assert fn(root) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_tie_breaking_returns_smallest_level(fn):
    # Level 1: 10
    # Level 2: 5 + 5 = 10
    # Level 3: 2 + 3 + 2 + 3 = 10
    # On tie, smallest level is 1
    root = build_tree_from_list([10, 5, 5, 2, 3, 2, 3])
    assert fn(root) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_negative_values(fn):
    # Level 1: -100
    # Level 2: -200 + -300 = -500
    # Level 3: -10 + -20 = -30
    # Max sum is -30 at level 3
    root = build_tree_from_list([-100, -200, -300, -10, -20, None, None])
    assert fn(root) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_skewed_left_tree(fn):
    # 1 -> 10 -> 2 -> 3
    root = TreeNode(1, left=TreeNode(10, left=TreeNode(2, left=TreeNode(3))))
    assert fn(root) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_skewed_right_tree(fn):
    # -5 -> -2 -> 50 -> 10
    root = TreeNode(-5, right=TreeNode(-2, right=TreeNode(50, right=TreeNode(10))))
    assert fn(root) == 3


# --- Hypothesis Property-Based Tests ---

tree_strategy = st.recursive(
    st.builds(TreeNode, val=st.integers(min_value=-100000, max_value=100000)),
    lambda children: st.builds(
        TreeNode,
        val=st.integers(min_value=-100000, max_value=100000),
        left=st.one_of(st.none(), children),
        right=st.one_of(st.none(), children),
    ),
    max_leaves=25
)


def oracle_max_level_sum(root: Optional[TreeNode]) -> int:
    """Independent oracle collecting level sums using simple level order traversal."""
    if not root:
        return 0
    levels: List[int] = []
    queue = deque([(root, 0)])
    while queue:
        node, depth = queue.popleft()
        if depth == len(levels):
            levels.append(0)
        levels[depth] += node.val
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    max_val = max(levels)
    return levels.index(max_val) + 1


def get_tree_height(node: Optional[TreeNode]) -> int:
    if not node:
        return 0
    return 1 + max(get_tree_height(node.left), get_tree_height(node.right))


@given(tree=tree_strategy)
def test_matches_oracle(tree):
    expected = oracle_max_level_sum(tree)
    for fn in SOLUTIONS:
        assert fn(tree) == expected


@given(tree=tree_strategy)
def test_level_range_invariant(tree):
    h = get_tree_height(tree)
    for fn in SOLUTIONS:
        res = fn(tree)
        if h == 0:
            assert res == 0
        else:
            assert 1 <= res <= h
