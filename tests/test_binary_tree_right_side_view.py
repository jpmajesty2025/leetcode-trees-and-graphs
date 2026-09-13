import pytest
from hypothesis import given, strategies as st
from typing import Optional, List
from collections import deque

from tree_node import TreeNode
from binaary_tree_right_side_view import right_side_view


# Wrapper to handle potential 'self' bug or normal signature cleanly in test suite
def safe_right_side_view(root: Optional[TreeNode]) -> List[int]:
    import inspect
    sig = inspect.signature(right_side_view)
    if len(sig.parameters) == 2:
        return right_side_view(None, root)
    return right_side_view(root)


SOLUTIONS = [
    safe_right_side_view,
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
    assert fn(None) == []


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    root = TreeNode(1)
    assert fn(root) == [1]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [1, 2, 3, None, 5, None, 4] -> Output: [1, 3, 4]
    root = build_tree_from_list([1, 2, 3, None, 5, None, 4])
    assert fn(root) == [1, 3, 4]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [1, None, 3] -> Output: [1, 3]
    root = build_tree_from_list([1, None, 3])
    assert fn(root) == [1, 3]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_left_subtree_longer_than_right(fn):
    #          1
    #        /   \
    #       2     3
    #      /
    #     4
    #    /
    #   5
    # Output: [1, 3, 4, 5]
    node5 = TreeNode(5)
    node4 = TreeNode(4, left=node5)
    node2 = TreeNode(2, left=node4)
    node3 = TreeNode(3)
    root = TreeNode(1, left=node2, right=node3)
    assert fn(root) == [1, 3, 4, 5]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_left_skewed_chain(fn):
    # 1 -> left: 2 -> left: 3 -> left: 4
    root = TreeNode(1, left=TreeNode(2, left=TreeNode(3, left=TreeNode(4))))
    assert fn(root) == [1, 2, 3, 4]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_right_skewed_chain(fn):
    # 1 -> right: 2 -> right: 3 -> right: 4
    root = TreeNode(1, right=TreeNode(2, right=TreeNode(3, right=TreeNode(4))))
    assert fn(root) == [1, 2, 3, 4]


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


def oracle_right_side_view(root: Optional[TreeNode]) -> List[int]:
    """Independent brute-force oracle grouping nodes by level and picking the rightmost."""
    if not root:
        return []
    levels: List[List[int]] = []
    queue = deque([(root, 0)])
    while queue:
        node, depth = queue.popleft()
        if depth == len(levels):
            levels.append([])
        levels[depth].append(node.val)
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    return [lvl[-1] for lvl in levels]


@given(tree=tree_strategy)
def test_matches_oracle(tree):
    expected = oracle_right_side_view(tree)
    for fn in SOLUTIONS:
        assert fn(tree) == expected
