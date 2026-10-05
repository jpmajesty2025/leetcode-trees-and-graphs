import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from invert_binary_tree import invert_tree as invert_tree_recursive
from invert_binary_tree_bfs import invert_tree_bfs
from invert_binary_tree_iterative import invert_tree_dfs_iterative

SOLUTIONS = [
    invert_tree_recursive,
    invert_tree_bfs,
    invert_tree_dfs_iterative,
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
    root = build_tree_from_list([4, 2, 7, 1, 3, 6, 9])
    inverted = fn(root)
    assert tree_to_list(inverted) == [4, 7, 2, 9, 6, 3, 1]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    root = build_tree_from_list([2, 1, 3])
    inverted = fn(root)
    assert tree_to_list(inverted) == [2, 3, 1]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    assert fn(None) is None


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    root = TreeNode(1)
    inverted = fn(root)
    assert tree_to_list(inverted) == [1]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_asymmetric_tree(fn):
    root = build_tree_from_list([1, 2, None, 3])
    inverted = fn(root)
    assert tree_to_list(inverted) == [1, None, 2, None, 3]


# --- Hypothesis Property-Based Tests ---

@st.composite
def binary_tree_strategy(draw, max_depth=4):
    def build_subtree(depth):
        if depth > max_depth or draw(st.booleans()):
            return None
        val = draw(st.integers(min_value=-100, max_value=100))
        node = TreeNode(val)
        node.left = build_subtree(depth + 1)
        node.right = build_subtree(depth + 1)
        return node

    val = draw(st.integers(min_value=-100, max_value=100))
    root = TreeNode(val)
    root.left = build_subtree(1)
    root.right = build_subtree(1)
    return root


@given(root=binary_tree_strategy())
def test_hypothesis_involution_property(root):
    # Inverting a tree twice must return the original tree
    original_copy = clone_tree(root)
    for fn in SOLUTIONS:
        t = clone_tree(original_copy)
        t_inverted = fn(t)
        t_restored = fn(t_inverted)
        assert trees_are_identical(t_restored, original_copy)
