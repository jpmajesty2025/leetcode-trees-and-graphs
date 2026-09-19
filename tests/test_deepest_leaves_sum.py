import pytest
from hypothesis import given, strategies as st
from typing import Optional, List
from collections import deque

from tree_node import TreeNode
from deepest_leaves_sum import deepest_leaves_sum
from deepest_leaves_sum_dfs import deepest_leaves_sum_dfs
from deepest_leaves_sum_iterative import deepest_leaves_sum_iterative

SOLUTIONS = [
    deepest_leaves_sum,
    deepest_leaves_sum_dfs,
    deepest_leaves_sum_iterative,
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
    assert fn(None) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    root = TreeNode(42)
    assert fn(root) == 42


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [1,2,3,4,5,null,6,7,null,null,null,null,8] -> Output: 15
    root = build_tree_from_list([1, 2, 3, 4, 5, None, 6, 7, None, None, None, None, 8])
    assert fn(root) == 15


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [6,7,8,2,7,1,3,9,null,1,4,null,null,null,5] -> Output: 19
    root = build_tree_from_list([6, 7, 8, 2, 7, 1, 3, 9, None, 1, 4, None, None, None, 5])
    assert fn(root) == 19


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_left_skewed_tree(fn):
    # 1 -> 2 -> 3 -> 4
    root = TreeNode(1, left=TreeNode(2, left=TreeNode(3, left=TreeNode(4))))
    assert fn(root) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_right_skewed_tree(fn):
    # 1 -> 2 -> 3 -> 4
    root = TreeNode(1, right=TreeNode(2, right=TreeNode(3, right=TreeNode(4))))
    assert fn(root) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_perfect_binary_tree(fn):
    #       1
    #     /   \
    #    2     3
    #   / \   / \
    #  4   5 6   7
    root = build_tree_from_list([1, 2, 3, 4, 5, 6, 7])
    assert fn(root) == 4 + 5 + 6 + 7


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


def oracle_deepest_leaves_sum(root: Optional[TreeNode]) -> int:
    """Independent oracle using depth tracking."""
    if not root:
        return 0
    max_depth = -1
    total = 0

    def dfs(node: Optional[TreeNode], depth: int):
        nonlocal max_depth, total
        if not node:
            return
        if depth > max_depth:
            max_depth = depth
            total = node.val
        elif depth == max_depth:
            total += node.val
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return total


@given(tree=tree_strategy)
def test_matches_oracle(tree):
    expected = oracle_deepest_leaves_sum(tree)
    for fn in SOLUTIONS:
        assert fn(tree) == expected
