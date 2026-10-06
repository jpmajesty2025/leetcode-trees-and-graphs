import pytest
from hypothesis import given, strategies as st
from typing import Optional, List
from collections import deque

from tree_node import TreeNode
from binary_tree_level_order_traversal import level_order as level_order_bfs
from binary_tree_level_order_traversal_dfs import level_order_dfs
from binary_tree_level_order_traversal_iterative import level_order_iterative

SOLUTIONS = [
    level_order_bfs,
    level_order_dfs,
    level_order_iterative,
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
    assert fn(root) == [[42]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [3, 9, 20, None, None, 15, 7] -> [[3], [9, 20], [15, 7]]
    root = build_tree_from_list([3, 9, 20, None, None, 15, 7])
    assert fn(root) == [[3], [9, 20], [15, 7]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    root = build_tree_from_list([1])
    assert fn(root) == [[1]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    root = build_tree_from_list([])
    assert fn(root) == []


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
        [2, 3],
        [4, 5, 6, 7],
    ]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_unbalanced_tree(fn):
    #       1
    #     /   \
    #    2     3
    #     \   /
    #      4 5
    root = build_tree_from_list([1, 2, 3, None, 4, 5, None])
    assert fn(root) == [
        [1],
        [2, 3],
        [4, 5],
    ]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_negative_values(fn):
    root = build_tree_from_list([-10, -20, -30, None, -5, -15, None])
    assert fn(root) == [
        [-10],
        [-20, -30],
        [-5, -15],
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
    max_leaves=25
)


def oracle_level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """Independent oracle collecting nodes by depth using simple queue with pairs."""
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
    return levels


def get_tree_height(node: Optional[TreeNode]) -> int:
    if not node:
        return 0
    return 1 + max(get_tree_height(node.left), get_tree_height(node.right))


def count_nodes(node: Optional[TreeNode]) -> int:
    if not node:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)


@given(tree=tree_strategy)
def test_matches_oracle(tree):
    expected = oracle_level_order(tree)
    for fn in SOLUTIONS:
        assert fn(tree) == expected


@given(tree=tree_strategy)
def test_height_invariant(tree):
    h = get_tree_height(tree)
    for fn in SOLUTIONS:
        res = fn(tree)
        assert len(res) == h


@given(tree=tree_strategy)
def test_node_count_invariant(tree):
    n = count_nodes(tree)
    for fn in SOLUTIONS:
        res = fn(tree)
        total_elements = sum(len(lvl) for lvl in res)
        assert total_elements == n
