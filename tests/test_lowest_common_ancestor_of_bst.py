import pytest
from hypothesis import given, strategies as st
from typing import Optional, List, Tuple
from collections import deque

from tree_node import TreeNode
from lowest_common_ancestor_of_bst import lowest_common_ancestor as lca_iterative
from lowest_common_ancestor_of_bst_recursive import lowest_common_ancestor_recursive as lca_recursive

SOLUTIONS = [
    lca_iterative,
    lca_recursive,
]


def build_bst_from_sorted_list(nums: List[int]) -> Optional[TreeNode]:
    """Helper to build a balanced BST from a sorted list of unique integers."""
    if not nums:
        return None
    mid = len(nums) // 2
    root = TreeNode(nums[mid])
    root.left = build_bst_from_sorted_list(nums[:mid])
    root.right = build_bst_from_sorted_list(nums[mid + 1:])
    return root


def build_tree_from_list(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Helper to build a binary tree from level-order list representation with None values."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        current = queue.popleft()
        if i < len(values) and values[i] is not None:
            current.left = TreeNode(values[i])
            queue.append(current.left)
        i += 1
        if i < len(values) and values[i] is not None:
            current.right = TreeNode(values[i])
            queue.append(current.right)
        i += 1
    return root


def find_node(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """Helper to locate a node object in a tree by its value."""
    if not root or root.val == val:
        return root
    if val < root.val:
        return find_node(root.left, val)
    return find_node(root.right, val)


def tree_contains(root: Optional[TreeNode], target: Optional[TreeNode]) -> bool:
    """Helper to check if target node exists in subtree rooted at root."""
    if not root or not target:
        return False
    if root is target or root.val == target.val:
        return True
    return tree_contains(root.left, target) or tree_contains(root.right, target)


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8 -> LCA = 6
    root = build_tree_from_list([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    p = find_node(root, 2)
    q = find_node(root, 8)
    lca = fn(root, p, q)
    assert lca is not None
    assert lca.val == 6


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4 -> LCA = 2 (p is ancestor of q)
    root = build_tree_from_list([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    p = find_node(root, 2)
    q = find_node(root, 4)
    lca = fn(root, p, q)
    assert lca is not None
    assert lca.val == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    # root = [2,1], p = 2, q = 1 -> LCA = 2
    root = build_tree_from_list([2, 1])
    p = find_node(root, 2)
    q = find_node(root, 1)
    lca = fn(root, p, q)
    assert lca is not None
    assert lca.val == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_subtree_lca(fn):
    # root = [6,2,8,0,4,7,9,null,null,3,5], p = 3, q = 5 -> LCA = 4
    root = build_tree_from_list([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    p = find_node(root, 3)
    q = find_node(root, 5)
    lca = fn(root, p, q)
    assert lca is not None
    assert lca.val == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_order_symmetry(fn):
    root = build_tree_from_list([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    p = find_node(root, 7)
    q = find_node(root, 9)
    assert fn(root, p, q).val == fn(root, q, p).val == 8


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_left_skewed_chain(fn):
    # 5 -> 4 -> 3 -> 2 -> 1
    root = TreeNode(5, left=TreeNode(4, left=TreeNode(3, left=TreeNode(2, left=TreeNode(1)))))
    p = find_node(root, 1)
    q = find_node(root, 3)
    assert fn(root, p, q).val == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_right_skewed_chain(fn):
    # 1 -> 2 -> 3 -> 4 -> 5
    root = TreeNode(1, right=TreeNode(2, right=TreeNode(3, right=TreeNode(4, right=TreeNode(5)))))
    p = find_node(root, 2)
    q = find_node(root, 5)
    assert fn(root, p, q).val == 2


# --- Hypothesis Property-Based Tests ---

@given(
    nums=st.lists(st.integers(min_value=-1000, max_value=1000), unique=True, min_size=2, max_size=30),
    data=st.data()
)
def test_lca_bst_properties(nums, data):
    sorted_nums = sorted(nums)
    root = build_bst_from_sorted_list(sorted_nums)

    # Pick two distinct nodes
    val_p, val_q = data.draw(st.tuples(st.sampled_from(sorted_nums), st.sampled_from(sorted_nums)).filter(lambda pair: pair[0] != pair[1]))
    p = find_node(root, val_p)
    q = find_node(root, val_q)

    for fn in SOLUTIONS:
        lca = fn(root, p, q)
        assert lca is not None
        # Invariant 1: LCA value must be between min(p, q) and max(p, q) inclusive
        assert min(val_p, val_q) <= lca.val <= max(val_p, val_q)
        # Invariant 2: LCA subtree must contain both p and q
        assert tree_contains(lca, p)
        assert tree_contains(lca, q)
