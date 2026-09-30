import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from balanced_binary_tree import is_balanced as is_balanced_dfs
from balanced_binary_tree_iterative import is_balanced_iterative
from balanced_binary_tree_top_down import is_balanced_top_down

SOLUTIONS = [
    is_balanced_dfs,
    is_balanced_iterative,
    is_balanced_top_down,
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

def oracle_is_balanced(root: Optional[TreeNode]) -> bool:
    """Independent oracle using depth calculation."""
    def depth(node):
        if not node:
            return 0
        return max(depth(node.left), depth(node.right)) + 1

    if not root:
        return True
    return (
        abs(depth(root.left) - depth(root.right)) <= 1
        and oracle_is_balanced(root.left)
        and oracle_is_balanced(root.right)
    )


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    assert fn(None) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    assert fn(TreeNode(1)) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [3,9,20,null,null,15,7] -> True
    root = build_tree_from_list([3, 9, 20, None, None, 15, 7])
    assert fn(root) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [1,2,2,3,3,null,null,4,4] -> False
    root = TreeNode(1,
        left=TreeNode(2,
            left=TreeNode(3, left=TreeNode(4), right=TreeNode(4)),
            right=TreeNode(3)
        ),
        right=TreeNode(2)
    )
    assert fn(root) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_linear_left_skewed_unbalanced(fn):
    # 3 -> 2 -> 1 (height 3 vs 0 on right)
    root = TreeNode(3, left=TreeNode(2, left=TreeNode(1)))
    assert fn(root) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_perfect_binary_tree(fn):
    #       1
    #     /   \
    #    2     3
    #   / \   / \
    #  4   5 6   7
    root = build_tree_from_list([1, 2, 3, 4, 5, 6, 7])
    assert fn(root) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_unbalanced_at_deep_subtree_only(fn):
    # Root has height diff 1, but left subtree is internally unbalanced
    root = TreeNode(1,
        left=TreeNode(2, left=TreeNode(3, left=TreeNode(4))),
        right=TreeNode(5, left=TreeNode(6), right=TreeNode(7))
    )
    assert fn(root) is False


# --- Hypothesis Property-Based Tests ---

tree_strategy = st.recursive(
    st.builds(TreeNode, val=st.integers(min_value=-100, max_value=100)),
    lambda children: st.builds(
        TreeNode,
        val=st.integers(min_value=-100, max_value=100),
        left=st.one_of(st.none(), children),
        right=st.one_of(st.none(), children),
    ),
    max_leaves=15
)


@given(tree=tree_strategy)
def test_hypothesis_matches_oracle(tree):
    expected = oracle_is_balanced(tree)
    for fn in SOLUTIONS:
        assert fn(tree) == expected
