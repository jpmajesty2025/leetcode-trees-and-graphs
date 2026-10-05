import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from path_sum_iii import path_sum as path_sum_optimal
from path_sum_iii_brute_force import path_sum_brute_force

SOLUTIONS = [
    path_sum_optimal,
    path_sum_brute_force,
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
    vals = [10, 5, -3, 3, 2, None, 11, 3, -2, None, 1]
    root = build_tree_from_list(vals)
    assert fn(root, 8) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    vals = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]
    root = build_tree_from_list(vals)
    assert fn(root, 22) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    assert fn(None, 8) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_matching(fn):
    root = TreeNode(8)
    assert fn(root, 8) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_not_matching(fn):
    root = TreeNode(5)
    assert fn(root, 8) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_negative_values_and_zeros(fn):
    vals = [1, -2, -3, 1, 3, -2, None, -1]
    root = build_tree_from_list(vals)
    assert fn(root, -1) == 4


# --- Hypothesis Property-Based Tests ---

@st.composite
def binary_tree_strategy(draw, max_d=3):
    def build_subtree(curr_d):
        if curr_d > max_d or draw(st.booleans()):
            return None
        val = draw(st.integers(min_value=-15, max_value=15))
        node = TreeNode(val)
        node.left = build_subtree(curr_d + 1)
        node.right = build_subtree(curr_d + 1)
        return node

    val = draw(st.integers(min_value=-15, max_value=15))
    root = TreeNode(val)
    root.left = build_subtree(1)
    root.right = build_subtree(1)
    target = draw(st.integers(min_value=-30, max_value=30))
    return root, target


@given(data=binary_tree_strategy())
def test_hypothesis_optimal_vs_brute_force_equivalence(data):
    root, target = data
    optimal_result = path_sum_optimal(root, target)
    brute_force_result = path_sum_brute_force(root, target)

    assert optimal_result == brute_force_result
