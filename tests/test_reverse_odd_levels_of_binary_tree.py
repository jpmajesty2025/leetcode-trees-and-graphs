import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from reverse_odd_levels_of_binary_tree import reverse_odd_levels as reverse_odd_levels_dfs
from reverse_odd_levels_of_binary_tree_bfs import reverse_odd_levels_bfs

SOLUTIONS = [
    reverse_odd_levels_dfs,
    reverse_odd_levels_bfs,
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


def tree_to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    if not root:
        return []
    result = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    while result and result[-1] is None:
        result.pop()
    return result


def clone_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root:
        return None
    new_node = TreeNode(root.val)
    new_node.left = clone_tree(root.left)
    new_node.right = clone_tree(root.right)
    return new_node


def trees_are_identical(t1: Optional[TreeNode], t2: Optional[TreeNode]) -> bool:
    if not t1 and not t2:
        return True
    if not t1 or not t2:
        return False
    return (
        t1.val == t2.val
        and trees_are_identical(t1.left, t2.left)
        and trees_are_identical(t1.right, t2.right)
    )


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    root = build_tree_from_list([2, 3, 5, 8, 13, 21, 34])
    reversed_tree = fn(root)
    assert tree_to_list(reversed_tree) == [2, 5, 3, 8, 13, 21, 34]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    root = build_tree_from_list([7, 13, 11])
    reversed_tree = fn(root)
    assert tree_to_list(reversed_tree) == [7, 11, 13]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    root = TreeNode(1)
    assert tree_to_list(fn(root)) == [1]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    assert fn(None) is None


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_four_level_perfect_tree(fn):
    vals = [0, 1, 2, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]
    root = build_tree_from_list(vals)
    reversed_tree = fn(root)
    expected = [0, 2, 1, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1]
    assert tree_to_list(reversed_tree) == expected


# --- Hypothesis Property-Based Tests ---

@st.composite
def perfect_binary_tree_strategy(draw, max_d=3):
    depth = draw(st.integers(min_value=0, max_value=max_d))

    def build_perfect(curr_d):
        if curr_d > depth:
            return None
        val = draw(st.integers(min_value=-100, max_value=100))
        node = TreeNode(val)
        node.left = build_perfect(curr_d + 1)
        node.right = build_perfect(curr_d + 1)
        return node

    return build_perfect(0)


@given(root=perfect_binary_tree_strategy())
def test_hypothesis_involution_and_consistency(root):
    original = clone_tree(root)
    for fn in SOLUTIONS:
        t = clone_tree(original)
        rev = fn(t)
        restored = fn(rev)
        assert trees_are_identical(restored, original)
