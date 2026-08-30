import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from path_sum import has_path_sum
from path_sum_iterative import has_path_sum_iterative
from path_sum_iterative_accumulator import has_path_sum_accumulator
from path_sum_bfs import has_path_sum_bfs

SOLUTIONS = [
    has_path_sum,
    has_path_sum_iterative,
    has_path_sum_accumulator,
    has_path_sum_bfs,
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
    assert fn(None, 0) is False
    assert fn(None, 10) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_match(fn):
    root = TreeNode(5)
    assert fn(root, 5) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_no_match(fn):
    root = TreeNode(5)
    assert fn(root, 1) is False
    assert fn(root, 0) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_zero(fn):
    root = TreeNode(0)
    assert fn(root, 0) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_example_1(fn):
    # [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22
    root = build_tree_from_list([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
    assert fn(root, 22) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_example_2(fn):
    # [1,2,3], targetSum = 5
    root = build_tree_from_list([1, 2, 3])
    assert fn(root, 5) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_example_3_empty(fn):
    root = build_tree_from_list([])
    assert fn(root, 0) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_intermediate_node_match_not_leaf(fn):
    # Root value equals targetSum, but root has children, so it's not a leaf
    # 1 -> 2
    root = TreeNode(1, left=TreeNode(2))
    assert fn(root, 1) is False
    assert fn(root, 3) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_negative_values(fn):
    # -2 -> -3 (leaf), sum = -5
    root = TreeNode(-2, right=TreeNode(-3))
    assert fn(root, -5) is True
    assert fn(root, -2) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_skewed_left_chain(fn):
    # 1 -> 2 -> 3 -> 4
    root = TreeNode(1, left=TreeNode(2, left=TreeNode(3, left=TreeNode(4))))
    assert fn(root, 10) is True
    assert fn(root, 6) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_multiple_paths(fn):
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    # Paths: 1->2->4 (7), 1->2->5 (8), 1->3 (4)
    root = build_tree_from_list([1, 2, 3, 4, 5])
    assert fn(root, 7) is True
    assert fn(root, 8) is True
    assert fn(root, 4) is True
    assert fn(root, 3) is False
    assert fn(root, 6) is False


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
    max_leaves=20
)


def get_all_root_to_leaf_sums(node: Optional[TreeNode], current_sum: int = 0) -> List[int]:
    """Independent oracle to compute all root-to-leaf path sums."""
    if not node:
        return []
    current_sum += node.val
    if not node.left and not node.right:
        return [current_sum]
    return get_all_root_to_leaf_sums(node.left, current_sum) + get_all_root_to_leaf_sums(node.right, current_sum)


@given(tree=tree_strategy, target_sum=st.integers(min_value=-5000, max_value=5000))
def test_all_solutions_equivalent(tree, target_sum):
    expected = target_sum in get_all_root_to_leaf_sums(tree)
    for fn in SOLUTIONS:
        assert fn(tree, target_sum) == expected


@given(target_sum=st.integers())
def test_none_is_always_false(target_sum):
    for fn in SOLUTIONS:
        assert fn(None, target_sum) is False
