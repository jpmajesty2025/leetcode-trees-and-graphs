import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from maximum_difference_between_node_and_ancestor import max_ancestor_diff
from maximum_difference_between_node_and_ancestor_iterative import max_ancestor_diff_iterative
from maximum_difference_between_node_and_ancestor_bfs import max_ancestor_diff_bfs

SOLUTIONS = [
    max_ancestor_diff,
    max_ancestor_diff_iterative,
    max_ancestor_diff_bfs,
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
    root = TreeNode(42)
    assert fn(root) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [8,3,10,1,6,null,14,null,null,4,7,13] -> Output: 7 (max diff is between 8 and 1 or 14 and 7 -> 7)
    root = build_tree_from_list([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13])
    assert fn(root) == 7


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [1,null,2,null,0,3] -> Output: 3
    root = build_tree_from_list([1, None, 2, None, 0, 3])
    assert fn(root) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_equal_values(fn):
    # [5, 5, 5, 5, 5] -> Output: 0
    root = build_tree_from_list([5, 5, 5, 5, 5])
    assert fn(root) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_strictly_increasing_chain(fn):
    # 1 -> 2 -> 3 -> 4 -> 5 -> Output: |5 - 1| = 4
    root = TreeNode(1, left=TreeNode(2, left=TreeNode(3, left=TreeNode(4, left=TreeNode(5)))))
    assert fn(root) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_strictly_decreasing_chain(fn):
    # 5 -> 4 -> 3 -> 2 -> 1 -> Output: |1 - 5| = 4
    root = TreeNode(5, left=TreeNode(4, left=TreeNode(3, left=TreeNode(2, left=TreeNode(1)))))
    assert fn(root) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_negative_values(fn):
    # Root: -5, Left: -10, Right: -2 -> diff between -5 and -10 is 5, -5 and -2 is 3 -> Output: 5
    root = build_tree_from_list([-5, -10, -2])
    assert fn(root) == 5


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_mixed_positive_and_negative(fn):
    # Root: 0, Left: -100, Right: 100 -> Output: 100
    root = build_tree_from_list([0, -100, 100])
    assert fn(root) == 100


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_interior_ancestor_descendant_max_diff(fn):
    # Root: 10, Left: 100 (left child of 100 is 1)
    # Between 100 and 1 diff is 99, while root 10 to 1 is 9, 10 to 100 is 90
    root = TreeNode(10, left=TreeNode(100, left=TreeNode(1)))
    assert fn(root) == 99


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


def oracle_max_ancestor_diff(root: Optional[TreeNode]) -> int:
    """Independent brute-force oracle checking all ancestor-descendant pairs."""
    if not root:
        return 0
    max_diff = 0

    def collect(node: Optional[TreeNode], ancestors: List[int]):
        nonlocal max_diff
        if not node:
            return
        for anc in ancestors:
            diff = abs(anc - node.val)
            if diff > max_diff:
                max_diff = diff
        new_ancestors = ancestors + [node.val]
        collect(node.left, new_ancestors)
        collect(node.right, new_ancestors)

    collect(root, [])
    return max_diff


@given(tree=tree_strategy)
def test_matches_oracle(tree):
    expected = oracle_max_ancestor_diff(tree)
    for fn in SOLUTIONS:
        assert fn(tree) == expected


@given(tree=tree_strategy)
def test_result_non_negative(tree):
    for fn in SOLUTIONS:
        assert fn(tree) >= 0
