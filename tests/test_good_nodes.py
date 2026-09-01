import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from count_good_nodes_in_binary_tree import good_nodes
from count_good_nodes_iterative import good_nodes_iterative
from count_good_nodes_bfs import good_nodes_bfs

SOLUTIONS = [
    good_nodes,
    good_nodes_iterative,
    good_nodes_bfs,
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
    assert fn(root) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_example_1(fn):
    # [3,1,4,3,null,1,5] -> Output: 4
    root = build_tree_from_list([3, 1, 4, 3, None, 1, 5])
    assert fn(root) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_example_2(fn):
    # [3,3,null,4,2] -> Output: 3
    root = build_tree_from_list([3, 3, None, 4, 2])
    assert fn(root) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_equal_values(fn):
    # All nodes equal, every node is good
    root = build_tree_from_list([2, 2, 2, 2, 2])
    assert fn(root) == 5


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_strictly_increasing_chain(fn):
    # 1 -> 2 -> 3 -> 4
    root = TreeNode(1, left=TreeNode(2, left=TreeNode(3, left=TreeNode(4))))
    assert fn(root) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_strictly_decreasing_chain(fn):
    # 4 -> 3 -> 2 -> 1
    root = TreeNode(4, left=TreeNode(3, left=TreeNode(2, left=TreeNode(1))))
    assert fn(root) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_negative_values(fn):
    # Root -3 (good), left -5 (not good), right -1 (good)
    root = build_tree_from_list([-3, -5, -1])
    assert fn(root) == 2


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


def oracle_count_good_nodes(node: Optional[TreeNode], max_so_far: float = float('-inf')) -> int:
    """Independent oracle implementation."""
    if not node:
        return 0
    is_good = 1 if node.val >= max_so_far else 0
    new_max = max(max_so_far, node.val)
    return is_good + oracle_count_good_nodes(node.left, new_max) + oracle_count_good_nodes(node.right, new_max)


@given(tree=tree_strategy)
def test_all_solutions_match_oracle(tree):
    expected = oracle_count_good_nodes(tree)
    for fn in SOLUTIONS:
        assert fn(tree) == expected
