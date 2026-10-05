import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from symmetric_tree import is_symmetric as is_symmetric_dfs
from symmetric_tree_bfs import is_symmetric_bfs

SOLUTIONS = [
    is_symmetric_dfs,
    is_symmetric_bfs,
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


def clone_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root:
        return None
    new_node = TreeNode(root.val)
    new_node.left = clone_tree(root.left)
    new_node.right = clone_tree(root.right)
    return new_node


def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root:
        return None
    new_node = TreeNode(root.val)
    new_node.left = invert_tree(root.right)
    new_node.right = invert_tree(root.left)
    return new_node


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    root = build_tree_from_list([1, 2, 2, 3, 4, 4, 3])
    assert fn(root) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    root = build_tree_from_list([1, 2, 2, None, 3, None, 3])
    assert fn(root) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    assert fn(None) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    root = TreeNode(1)
    assert fn(root) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_asymmetric_values(fn):
    root = build_tree_from_list([1, 2, 2, 2, None, 2])
    assert fn(root) is False


# --- Hypothesis Property-Based Tests ---

@st.composite
def binary_subtree_strategy(draw, max_depth=3):
    def build_subtree(curr_d):
        if curr_d > max_depth or draw(st.booleans()):
            return None
        val = draw(st.integers(min_value=-50, max_value=50))
        node = TreeNode(val)
        node.left = build_subtree(curr_d + 1)
        node.right = build_subtree(curr_d + 1)
        return node

    return build_subtree(0)


@given(subtree=binary_subtree_strategy())
def test_hypothesis_constructed_symmetric_tree(subtree):
    # Construct an inherently symmetric tree: root with left = subtree and right = invert(subtree)
    root = TreeNode(100)
    root.left = clone_tree(subtree)
    root.right = invert_tree(subtree)

    for fn in SOLUTIONS:
        assert fn(root) is True


@given(subtree=binary_subtree_strategy())
def test_hypothesis_corrupted_symmetry(subtree):
    if not subtree:
        return
    root = TreeNode(100)
    root.left = clone_tree(subtree)
    root.right = invert_tree(subtree)
    
    # Corrupt right child's value to break symmetry
    root.right.val += 999

    for fn in SOLUTIONS:
        assert fn(root) is False
