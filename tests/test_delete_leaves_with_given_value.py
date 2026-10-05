import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from delete_leaves_with_given_value import remove_leaf_nodes as remove_leaf_nodes_dfs
from delete_leaves_with_given_value_iterative import remove_leaf_nodes_iterative

SOLUTIONS = [
    remove_leaf_nodes_dfs,
    remove_leaf_nodes_iterative,
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


def tree_has_target_leaf(root: Optional[TreeNode], target: int) -> bool:
    if not root:
        return False
    if not root.left and not root.right:
        return root.val == target
    return tree_has_target_leaf(root.left, target) or tree_has_target_leaf(root.right, target)


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    vals = [1, 2, 3, 2, None, 2, 4]
    root = build_tree_from_list(vals)
    res = fn(root, 2)
    assert tree_to_list(res) == [1, None, 3, None, 4]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    vals = [1, 3, 3, 3, 2]
    root = build_tree_from_list(vals)
    res = fn(root, 3)
    assert tree_to_list(res) == [1, 3, None, None, 2]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    vals = [1, 2, None, 2, None, 2]
    root = build_tree_from_list(vals)
    res = fn(root, 2)
    assert tree_to_list(res) == [1]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_nodes_matching(fn):
    vals = [2, 2, 2]
    root = build_tree_from_list(vals)
    res = fn(root, 2)
    assert res is None


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_matching_node(fn):
    root = TreeNode(2)
    assert fn(root, 2) is None


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_non_matching_node(fn):
    root = TreeNode(3)
    res = fn(root, 2)
    assert res is not None and res.val == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    assert fn(None, 2) is None


# --- Hypothesis Property-Based Tests ---

@st.composite
def binary_tree_strategy(draw, max_d=3):
    def build_subtree(curr_d):
        if curr_d > max_d or draw(st.booleans()):
            return None
        val = draw(st.integers(min_value=1, max_value=5))
        node = TreeNode(val)
        node.left = build_subtree(curr_d + 1)
        node.right = build_subtree(curr_d + 1)
        return node

    val = draw(st.integers(min_value=1, max_value=5))
    root = TreeNode(val)
    root.left = build_subtree(1)
    root.right = build_subtree(1)
    target = draw(st.integers(min_value=1, max_value=5))
    return root, target


@given(data=binary_tree_strategy())
def test_hypothesis_no_target_leaves_and_consistency(data):
    root, target = data
    t1 = clone_tree(root)
    t2 = clone_tree(root)

    res1 = remove_leaf_nodes_dfs(t1, target)
    res2 = remove_leaf_nodes_iterative(t2, target)

    # Property 1: Identical results between both algorithms
    assert trees_are_identical(res1, res2)

    # Property 2: No leaf with target value remains
    assert not tree_has_target_leaf(res1, target)
    assert not tree_has_target_leaf(res2, target)
