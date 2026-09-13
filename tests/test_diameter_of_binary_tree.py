import pytest
from hypothesis import given, strategies as st
from typing import Optional, List, Tuple

from tree_node import TreeNode
from diameter_of_binary_tree import diameter_of_binary_tree
from diameter_of_binary_tree_iterative import diameter_of_binary_tree_iterative

SOLUTIONS = [
    diameter_of_binary_tree,
    diameter_of_binary_tree_iterative,
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


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    assert fn(None) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    root = TreeNode(1)
    assert fn(root) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_nodes(fn):
    root = TreeNode(1, left=TreeNode(2))
    assert fn(root) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [1, 2, 3, 4, 5] -> longest path is 4-2-1-3 or 5-2-1-3 (length 3)
    root = build_tree_from_list([1, 2, 3, 4, 5])
    assert fn(root) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_diameter_not_passing_through_root(fn):
    # Diameter is completely in the left subtree
    #          1
    #         /
    #        2
    #       / \
    #      3   4
    #     /     \
    #    5       6
    # Longest path is 5-3-2-4-6 (length 4), which does not pass through root 1.
    node5 = TreeNode(5)
    node6 = TreeNode(6)
    node3 = TreeNode(3, left=node5)
    node4 = TreeNode(4, right=node6)
    node2 = TreeNode(2, left=node3, right=node4)
    root = TreeNode(1, left=node2)
    assert fn(root) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_left_skewed_chain(fn):
    # 5 -> 4 -> 3 -> 2 -> 1 (4 edges)
    root = TreeNode(5, left=TreeNode(4, left=TreeNode(3, left=TreeNode(2, left=TreeNode(1)))))
    assert fn(root) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_right_skewed_chain(fn):
    # 1 -> 2 -> 3 -> 4 -> 5 (4 edges)
    root = TreeNode(1, right=TreeNode(2, right=TreeNode(3, right=TreeNode(4, right=TreeNode(5)))))
    assert fn(root) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_zigzag_chain(fn):
    # 1 -> left: 2 -> right: 3 -> left: 4 (3 edges)
    root = TreeNode(1, left=TreeNode(2, right=TreeNode(3, left=TreeNode(4))))
    assert fn(root) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_perfect_binary_tree(fn):
    # Depth 3 full binary tree: 7 nodes, longest leaf-to-leaf path has 4 edges
    root = build_tree_from_list([1, 2, 3, 4, 5, 6, 7])
    assert fn(root) == 4


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


def height(node: Optional[TreeNode]) -> int:
    """Independent helper: computes height of binary tree."""
    if not node:
        return 0
    return 1 + max(height(node.left), height(node.right))


def collect_nodes(node: Optional[TreeNode]) -> List[TreeNode]:
    """Independent helper: collects all nodes in the tree."""
    if not node:
        return []
    return [node] + collect_nodes(node.left) + collect_nodes(node.right)


def oracle_diameter(root: Optional[TreeNode]) -> int:
    """Independent brute-force oracle checking max(height(u.left) + height(u.right)) for all nodes u."""
    if not root:
        return 0
    all_nodes = collect_nodes(root)
    return max(height(u.left) + height(u.right) for u in all_nodes)


@given(tree=tree_strategy)
def test_matches_oracle(tree):
    expected = oracle_diameter(tree)
    for fn in SOLUTIONS:
        assert fn(tree) == expected


@given(tree=tree_strategy)
def test_diameter_bounds(tree):
    nodes = collect_nodes(tree)
    num_nodes = len(nodes)
    for fn in SOLUTIONS:
        result = fn(tree)
        assert result >= 0
        if num_nodes == 0:
            assert result == 0
        else:
            assert result <= num_nodes - 1
