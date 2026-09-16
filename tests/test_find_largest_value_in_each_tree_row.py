import pytest
from hypothesis import given, strategies as st
from typing import Optional, List
from collections import deque

from tree_node import TreeNode
from find_largest_value_in_each_tree_row import largest_values

SOLUTIONS = [
    largest_values,
]


# --- Helper to construct trees from LeetCode-style level order lists ---
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
    assert fn(None) == []


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    root = TreeNode(42)
    assert fn(root) == [42]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [1, 3, 2, 5, 3, null, 9] -> Output: [1, 3, 9]
    root = build_tree_from_list([1, 3, 2, 5, 3, None, 9])
    assert fn(root) == [1, 3, 9]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [1, 2, 3] -> Output: [1, 3]
    root = build_tree_from_list([1, 2, 3])
    assert fn(root) == [1, 3]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_negative_values(fn):
    # Root: -10, Row 1: [-20, -5], Row 2: [-30, -2] -> Output: [-10, -5, -2]
    root = TreeNode(-10)
    root.left = TreeNode(-20, left=TreeNode(-30))
    root.right = TreeNode(-5, right=TreeNode(-2))
    assert fn(root) == [-10, -5, -2]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_left_skewed_chain(fn):
    # 1 -> 2 -> 3 -> 4
    root = TreeNode(1, left=TreeNode(2, left=TreeNode(3, left=TreeNode(4))))
    assert fn(root) == [1, 2, 3, 4]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_right_skewed_chain(fn):
    # 1 -> 2 -> 3 -> 4
    root = TreeNode(1, right=TreeNode(2, right=TreeNode(3, right=TreeNode(4))))
    assert fn(root) == [1, 2, 3, 4]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_uniform_duplicate_values(fn):
    # [7, 7, 7, 7] -> Output: [7, 7, 7]
    root = build_tree_from_list([7, 7, 7, 7])
    assert fn(root) == [7, 7, 7]


# --- Hypothesis Property-Based Tests ---

tree_strategy = st.recursive(
    st.builds(TreeNode, val=st.integers(min_value=-1000, max_value=1000)),
    lambda children: st.builds(
        TreeNode,
        val=st.integers(min_value=-1000, max_value=1000),
        left=st.one_of(st.none(), children),
        right=st.one_of(st.none(), children),
    ),
    max_leaves=20
)


def oracle_largest_values(root: Optional[TreeNode]) -> List[int]:
    """Independent brute-force oracle grouping nodes by level and taking max of each level."""
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
    return [max(lvl) for lvl in levels]


@given(tree=tree_strategy)
def test_matches_oracle(tree):
    expected = oracle_largest_values(tree)
    for fn in SOLUTIONS:
        assert fn(tree) == expected


def get_tree_height(node: Optional[TreeNode]) -> int:
    if not node:
        return 0
    return 1 + max(get_tree_height(node.left), get_tree_height(node.right))


@given(tree=tree_strategy)
def test_result_length_equals_height(tree):
    h = get_tree_height(tree)
    for fn in SOLUTIONS:
        assert len(fn(tree)) == h
