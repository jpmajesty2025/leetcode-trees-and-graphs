import pytest
from hypothesis import given, strategies as st
from typing import Optional, List
from collections import deque

from tree_node import TreeNode
from binary_tree_zigzag_level_order_traversal import zigzag_level_order
from binary_tree_zigzag_level_order_traversal_dfs import zigzag_level_order_dfs
from binary_tree_zigzag_level_order_traversal_iterative import zigzag_level_order_iterative

SOLUTIONS = [
    zigzag_level_order,
    zigzag_level_order_dfs,
    zigzag_level_order_iterative,
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
    assert fn(None) == []


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    root = TreeNode(42)
    assert fn(root) == [[42]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [3, 9, 20, None, None, 15, 7] -> [[3], [20, 9], [15, 7]]
    root = build_tree_from_list([3, 9, 20, None, None, 15, 7])
    assert fn(root) == [[3], [20, 9], [15, 7]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [1] -> [[1]]
    root = build_tree_from_list([1])
    assert fn(root) == [[1]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_left_skewed_tree(fn):
    # 1 -> 2 -> 3 -> 4
    root = TreeNode(1, left=TreeNode(2, left=TreeNode(3, left=TreeNode(4))))
    assert fn(root) == [[1], [2], [3], [4]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_right_skewed_tree(fn):
    # 1 -> 2 -> 3 -> 4
    root = TreeNode(1, right=TreeNode(2, right=TreeNode(3, right=TreeNode(4))))
    assert fn(root) == [[1], [2], [3], [4]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_perfect_binary_tree_3_levels(fn):
    #       1
    #     /   \
    #    2     3
    #   / \   / \
    #  4   5 6   7
    root = build_tree_from_list([1, 2, 3, 4, 5, 6, 7])
    assert fn(root) == [
        [1],
        [3, 2],
        [4, 5, 6, 7]
    ]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_four_level_balanced_tree(fn):
    # Tier 0: [1] (L->R)
    # Tier 1: [3, 2] (R->L)
    # Tier 2: [4, 5, 6, 7] (L->R)
    # Tier 3: [15..8] (R->L)
    root = build_tree_from_list(list(range(1, 16)))
    assert fn(root) == [
        [1],
        [3, 2],
        [4, 5, 6, 7],
        [15, 14, 13, 12, 11, 10, 9, 8]
    ]


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


def oracle_zigzag(root: Optional[TreeNode]) -> List[List[int]]:
    """Independent oracle collecting levels and reversing odd rows."""
    if not root:
        return []
    levels: List[List[int]] = []
    queue = [(root, 0)]
    while queue:
        node, depth = queue.pop(0)
        if depth == len(levels):
            levels.append([])
        levels[depth].append(node.val)
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    for i in range(len(levels)):
        if i % 2 == 1:
            levels[i].reverse()
    return levels


def get_tree_height(node: Optional[TreeNode]) -> int:
    if not node:
        return 0
    return 1 + max(get_tree_height(node.left), get_tree_height(node.right))


@given(tree=tree_strategy)
def test_matches_oracle(tree):
    expected = oracle_zigzag(tree)
    for fn in SOLUTIONS:
        assert fn(tree) == expected


@given(tree=tree_strategy)
def test_invariants(tree):
    h = get_tree_height(tree)
    for fn in SOLUTIONS:
        result = fn(tree)
        assert len(result) == h
