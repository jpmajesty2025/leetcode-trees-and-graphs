import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from binary_tree_in_order_traversal import inorder_traversal as inorder_iterative
from binary_tree_in_order_traversal_recursive import inorder_traversal_recursive
from binary_tree_in_order_traversal_morris import inorder_traversal_morris

SOLUTIONS = [
    inorder_iterative,
    inorder_traversal_recursive,
    inorder_traversal_morris,
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

def oracle_inorder(root: Optional[TreeNode]) -> List[int]:
    """Independent recursive oracle."""
    if not root:
        return []
    return oracle_inorder(root.left) + [root.val] + oracle_inorder(root.right)


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    assert fn(None) == []


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    root = TreeNode(42)
    assert fn(root) == [42]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [1, null, 2, 3] -> [1, 3, 2]
    root = TreeNode(1, right=TreeNode(2, left=TreeNode(3)))
    assert fn(root) == [1, 3, 2]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [] -> []
    assert fn(None) == []


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    # [1] -> [1]
    assert fn(TreeNode(1)) == [1]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_full_binary_tree(fn):
    #       4
    #     /   \
    #    2     6
    #   / \   / \
    #  1   3 5   7
    root = build_tree_from_list([4, 2, 6, 1, 3, 5, 7])
    assert fn(root) == [1, 2, 3, 4, 5, 6, 7]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_left_skewed_tree(fn):
    # 3 -> 2 -> 1
    root = TreeNode(3, left=TreeNode(2, left=TreeNode(1)))
    assert fn(root) == [1, 2, 3]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_right_skewed_tree(fn):
    # 1 -> 2 -> 3
    root = TreeNode(1, right=TreeNode(2, right=TreeNode(3)))
    assert fn(root) == [1, 2, 3]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_deep_adversarial_skewed_tree(fn):
    # 500 node left-skewed tree
    n = 500
    root = TreeNode(n)
    curr = root
    for val in range(n - 1, 0, -1):
        curr.left = TreeNode(val)
        curr = curr.left

    expected = list(range(1, n + 1))
    assert fn(root) == expected


# --- Hypothesis Property-Based Tests ---

tree_strategy = st.recursive(
    st.builds(TreeNode, val=st.integers(min_value=-1000, max_value=1000)),
    lambda children: st.builds(
        TreeNode,
        val=st.integers(min_value=-1000, max_value=1000),
        left=st.one_of(st.none(), children),
        right=st.one_of(st.none(), children),
    ),
    max_leaves=20
)


@given(tree=tree_strategy)
def test_hypothesis_matches_oracle(tree):
    expected = oracle_inorder(tree)
    for fn in SOLUTIONS:
        assert fn(tree) == expected


@given(tree=tree_strategy)
def test_hypothesis_preserves_length(tree):
    def count_nodes(node):
        if not node:
            return 0
        return 1 + count_nodes(node.left) + count_nodes(node.right)

    n = count_nodes(tree)
    for fn in SOLUTIONS:
        assert len(fn(tree)) == n
