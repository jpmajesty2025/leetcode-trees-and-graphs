import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from leaf_similar_trees import leaf_similar as leaf_similar_gen
from leaf_similar_trees_iterative import leaf_similar_iterative
from leaf_similar_trees_recursive import leaf_similar_recursive

SOLUTIONS = [
    leaf_similar_gen,
    leaf_similar_iterative,
    leaf_similar_recursive,
]


# --- Helper to construct tree from level-order list ---

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


# --- Independent Reference Oracle ---

def oracle_leaves(root: Optional[TreeNode]) -> List[int]:
    """Independent oracle collecting leaves."""
    if not root:
        return []
    if not root.left and not root.right:
        return [root.val]
    return oracle_leaves(root.left) + oracle_leaves(root.right)


def oracle_leaf_similar(root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
    return oracle_leaves(root1) == oracle_leaves(root2)


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_both_empty_trees(fn):
    assert fn(None, None) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_one_empty_tree(fn):
    assert fn(TreeNode(1), None) is False
    assert fn(None, TreeNode(1)) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_identical_nodes(fn):
    assert fn(TreeNode(42), TreeNode(42)) is True
    assert fn(TreeNode(42), TreeNode(99)) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # tree1 = [3,5,1,6,2,9,8,null,null,7,4], tree2 = [3,5,1,6,7,4,2,null,null,null,null,null,null,9,8]
    # leaves: [6, 7, 4, 9, 8]
    t1 = build_tree_from_list([3, 5, 1, 6, 2, 9, 8, None, None, 7, 4])
    t2 = build_tree_from_list([3, 5, 1, 6, 7, 4, 2, None, None, None, None, None, None, 9, 8])
    assert fn(t1, t2) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # tree1 = [1,2,3], tree2 = [1,3,2] -> leaves [2,3] vs [3,2] -> False
    t1 = build_tree_from_list([1, 2, 3])
    t2 = build_tree_from_list([1, 3, 2])
    assert fn(t1, t2) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_different_lengths_of_leaves(fn):
    # Tree 1 has 2 leaves [2, 3], Tree 2 has 3 leaves [2, 3, 4]
    t1 = TreeNode(1, left=TreeNode(2), right=TreeNode(3))
    t2 = TreeNode(1, left=TreeNode(2), right=TreeNode(5, left=TreeNode(3), right=TreeNode(4)))
    assert fn(t1, t2) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_different_shapes_same_leaves(fn):
    # Tree 1: Left-skewed with leaf 10
    t1 = TreeNode(1, left=TreeNode(2, left=TreeNode(10)))
    # Tree 2: Right-skewed with leaf 10
    t2 = TreeNode(3, right=TreeNode(4, right=TreeNode(10)))
    assert fn(t1, t2) is True


# --- Hypothesis Property-Based Tests ---

tree_strategy = st.recursive(
    st.builds(TreeNode, val=st.integers(min_value=-50, max_value=50)),
    lambda children: st.builds(
        TreeNode,
        val=st.integers(min_value=-50, max_value=50),
        left=st.one_of(st.none(), children),
        right=st.one_of(st.none(), children),
    ),
    max_leaves=12
)


@given(t1=tree_strategy, t2=tree_strategy)
def test_hypothesis_matches_oracle(t1, t2):
    expected = oracle_leaf_similar(t1, t2)
    for fn in SOLUTIONS:
        assert fn(t1, t2) == expected


@given(t=tree_strategy)
def test_hypothesis_reflexivity(t):
    """A tree must always be leaf-similar to itself."""
    for fn in SOLUTIONS:
        assert fn(t, t) is True
