import pytest
from hypothesis import given, strategies as st
from typing import Optional, List, Tuple

from tree_node import TreeNode
from same_tree import is_same_tree
from same_tree_iterative import is_same_tree_iterative
from same_tree_bfs import is_same_tree_bfs

SOLUTIONS = [
    is_same_tree,
    is_same_tree_iterative,
    is_same_tree_bfs,
]


# --- Helper to construct trees from LeetCode-style level order lists ---
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


def clone_tree(node: Optional[TreeNode]) -> Optional[TreeNode]:
    if not node:
        return None
    return TreeNode(node.val, clone_tree(node.left), clone_tree(node.right))


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_both_empty_trees(fn):
    assert fn(None, None) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_one_empty_one_non_empty(fn):
    root = TreeNode(1)
    assert fn(root, None) is False
    assert fn(None, root) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_same_val(fn):
    p = TreeNode(1)
    q = TreeNode(1)
    assert fn(p, q) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_different_val(fn):
    p = TreeNode(1)
    q = TreeNode(2)
    assert fn(p, q) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_example_1_identical(fn):
    # p = [1,2,3], q = [1,2,3] -> True
    p = build_tree_from_list([1, 2, 3])
    q = build_tree_from_list([1, 2, 3])
    assert fn(p, q) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_example_2_structural_difference(fn):
    # p = [1,2], q = [1,null,2] -> False
    p = build_tree_from_list([1, 2])
    q = build_tree_from_list([1, None, 2])
    assert fn(p, q) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_example_3_different_values(fn):
    # p = [1,2,1], q = [1,1,2] -> False
    p = build_tree_from_list([1, 2, 1])
    q = build_tree_from_list([1, 1, 2])
    assert fn(p, q) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_skewed_trees_same(fn):
    # 1 -> 2 -> 3 (left skewed)
    p = TreeNode(1, left=TreeNode(2, left=TreeNode(3)))
    q = TreeNode(1, left=TreeNode(2, left=TreeNode(3)))
    assert fn(p, q) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_skewed_trees_different_direction(fn):
    # p: 1 -> 2 (left), q: 1 -> 2 (right)
    p = TreeNode(1, left=TreeNode(2))
    q = TreeNode(1, right=TreeNode(2))
    assert fn(p, q) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_negative_values(fn):
    p = TreeNode(-10, left=TreeNode(-20), right=TreeNode(-30))
    q = TreeNode(-10, left=TreeNode(-20), right=TreeNode(-30))
    assert fn(p, q) is True

    q_diff = TreeNode(-10, left=TreeNode(-20), right=TreeNode(30))
    assert fn(p, q_diff) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_subtle_deep_difference(fn):
    # Deep trees identical except for one leaf
    p = build_tree_from_list([1, 2, 3, 4, 5, 6, 7])
    q = build_tree_from_list([1, 2, 3, 4, 5, 6, 8])
    assert fn(p, q) is False


# --- Hypothesis Property-Based Tests ---

# Strategy for generating binary trees
tree_strategy = st.recursive(
    st.none().map(lambda _: None),
    lambda children: st.builds(
        TreeNode,
        val=st.integers(min_value=-1000, max_value=1000),
        left=children,
        right=children,
    ),
    max_leaves=15
)


def serialize_tree(node: Optional[TreeNode]) -> Tuple:
    """Independent oracle: converts tree to nested tuple structure representing (val, left, right)."""
    if node is None:
        return ()
    return (node.val, serialize_tree(node.left), serialize_tree(node.right))


@given(tree=tree_strategy)
def test_reflexivity_and_clone(tree):
    """Property: A tree is always equal to itself and to a distinct clone of itself."""
    cloned = clone_tree(tree)
    for fn in SOLUTIONS:
        assert fn(tree, tree) is True
        assert fn(tree, cloned) is True


@given(tree_p=tree_strategy, tree_q=tree_strategy)
def test_equivalence_with_independent_oracle(tree_p, tree_q):
    """Property: All implementations agree with the structural tuple serialization oracle."""
    expected = (serialize_tree(tree_p) == serialize_tree(tree_q))
    for fn in SOLUTIONS:
        assert fn(tree_p, tree_q) == expected


@given(tree=tree_strategy)
def test_symmetry(tree):
    """Property: if tree is modified at any node, symmetry holds is_same_tree(p, q) == is_same_tree(q, p)."""
    cloned = clone_tree(tree)
    if cloned:
        cloned.val += 1  # mutate to make different
    for fn in SOLUTIONS:
        assert fn(tree, cloned) == fn(cloned, tree)
