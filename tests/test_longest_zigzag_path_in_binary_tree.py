import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from longest_zigzag_path_in_binary_tree import longest_zig_zag as longest_zig_zag_top_down
from longest_zigzag_path_in_binary_tree_bottom_up import longest_zig_zag_bottom_up
from longest_zigzag_path_in_binary_tree_bfs import longest_zig_zag_bfs

SOLUTIONS = [
    longest_zig_zag_top_down,
    longest_zig_zag_bottom_up,
    longest_zig_zag_bfs,
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
    vals = [1, None, 1, 1, 1, None, None, 1, 1, None, 1, None, None, None, 1]
    root = build_tree_from_list(vals)
    assert fn(root) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    vals = [1, 1, 1, None, 1, None, None, 1, 1, None, 1]
    root = build_tree_from_list(vals)
    assert fn(root) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    root = TreeNode(1)
    assert fn(root) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    assert fn(None) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_linear_left_skewed_tree(fn):
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(3)
    root.left.left.left = TreeNode(4)
    # Longest zigzag is 1 (only 1 left step, can't zigzag right)
    assert fn(root) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_perfect_alternating_zigzag(fn):
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.right = TreeNode(3)
    root.left.right.left = TreeNode(4)
    root.left.right.left.right = TreeNode(5)
    # 4 edges: left -> right -> left -> right
    assert fn(root) == 4


# --- Hypothesis Property-Based Tests ---

@st.composite
def binary_tree_strategy(draw, max_d=3):
    def build_subtree(curr_d):
        if curr_d > max_d or draw(st.booleans()):
            return None
        node = TreeNode(1)
        node.left = build_subtree(curr_d + 1)
        node.right = build_subtree(curr_d + 1)
        return node

    root = TreeNode(1)
    root.left = build_subtree(1)
    root.right = build_subtree(1)
    return root


@given(root=binary_tree_strategy())
def test_hypothesis_solutions_consistency(root):
    results = [fn(root) for fn in SOLUTIONS]
    assert results[0] == results[1] == results[2]
