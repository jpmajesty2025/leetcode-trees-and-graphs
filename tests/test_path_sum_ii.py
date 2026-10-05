import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from path_sum_ii import path_sum as path_sum_dfs
from path_sum_ii_bfs import path_sum_bfs

SOLUTIONS = [
    path_sum_dfs,
    path_sum_bfs,
]


# --- Helpers ---

def build_tree_from_list(values: List[Optional[int]]) -> Optional[TreeNode]:
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        curr = queue.pop(0)
        if i < len(values) and values[i] is not None:
            curr.left = TreeNode(values[i])
            queue.append(curr.left)
        i += 1
        if i < len(values) and values[i] is not None:
            curr.right = TreeNode(values[i])
            queue.append(curr.right)
        i += 1
    return root


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    vals = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]
    root = build_tree_from_list(vals)
    target_sum = 22
    expected = [[5, 4, 11, 2], [5, 8, 4, 5]]
    result = fn(root, target_sum)
    assert sorted(result) == sorted(expected)


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    root = build_tree_from_list([1, 2, 3])
    target_sum = 5
    assert fn(root, target_sum) == []


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    root = build_tree_from_list([1, 2])
    target_sum = 0
    assert fn(root, target_sum) == []


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    assert fn(None, 0) == []


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_matching(fn):
    root = TreeNode(5)
    assert fn(root, 5) == [[5]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_not_matching(fn):
    root = TreeNode(5)
    assert fn(root, 1) == []


# --- Hypothesis Property-Based Tests ---

@st.composite
def binary_tree_strategy(draw, max_d=3):
    def build_subtree(curr_d):
        if curr_d > max_d or draw(st.booleans()):
            return None
        val = draw(st.integers(min_value=-20, max_value=20))
        node = TreeNode(val)
        node.left = build_subtree(curr_d + 1)
        node.right = build_subtree(curr_d + 1)
        return node

    val = draw(st.integers(min_value=-20, max_value=20))
    root = TreeNode(val)
    root.left = build_subtree(1)
    root.right = build_subtree(1)
    target = draw(st.integers(min_value=-50, max_value=50))
    return root, target


@given(data=binary_tree_strategy())
def test_hypothesis_paths_validity_and_consistency(data):
    root, target = data
    results = [fn(root, target) for fn in SOLUTIONS]

    # Both DFS and BFS must return identical paths (order-independent)
    assert sorted(results[0]) == sorted(results[1])

    # Every returned path must sum to target
    for path in results[0]:
        assert sum(path) == target
