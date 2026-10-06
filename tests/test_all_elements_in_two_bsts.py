import pytest
from hypothesis import given, strategies as st
from typing import Optional, List
from collections import deque

from tree_node import TreeNode
from all_elements_in_two_bsts import get_all_elements as get_all_elements_stack
from all_elements_in_two_bsts_two_pass import get_all_elements_two_pass

SOLUTIONS = [
    get_all_elements_stack,
    get_all_elements_two_pass,
]


def build_bst_from_sorted_list(nums: List[int]) -> Optional[TreeNode]:
    """Helper to build a balanced BST from a sorted list of integers."""
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


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_both_empty(fn):
    assert fn(None, None) == []


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_first_empty(fn):
    root2 = build_tree_from_list([1, 0, 3])
    assert fn(None, root2) == [0, 1, 3]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_second_empty(fn):
    root1 = build_tree_from_list([2, 1, 4])
    assert fn(root1, None) == [1, 2, 4]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # root1 = [2,1,4], root2 = [1,0,3] -> [0,1,1,2,3,4]
    root1 = build_tree_from_list([2, 1, 4])
    root2 = build_tree_from_list([1, 0, 3])
    assert fn(root1, root2) == [0, 1, 1, 2, 3, 4]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # root1 = [1,null,8], root2 = [8,1] -> [1,1,8,8]
    root1 = build_tree_from_list([1, None, 8])
    root2 = build_tree_from_list([8, 1])
    assert fn(root1, root2) == [1, 1, 8, 8]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_disjoint_ranges(fn):
    # Tree 1: 1, 2, 3 ; Tree 2: 10, 20, 30
    root1 = build_bst_from_sorted_list([1, 2, 3])
    root2 = build_bst_from_sorted_list([10, 20, 30])
    assert fn(root1, root2) == [1, 2, 3, 10, 20, 30]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_interleaved_negative_and_positive(fn):
    root1 = build_bst_from_sorted_list([-50, -10, 0, 40])
    root2 = build_bst_from_sorted_list([-30, -5, 20, 50])
    assert fn(root1, root2) == [-50, -30, -10, -5, 0, 20, 40, 50]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_skewed_trees(fn):
    # root1 left-skewed: 3 -> 2 -> 1
    # root2 right-skewed: 4 -> 5 -> 6
    root1 = TreeNode(3, left=TreeNode(2, left=TreeNode(1)))
    root2 = TreeNode(4, right=TreeNode(5, right=TreeNode(6)))
    assert fn(root1, root2) == [1, 2, 3, 4, 5, 6]


# --- Hypothesis Property-Based Tests ---

def extract_inorder(node: Optional[TreeNode]) -> List[int]:
    if not node:
        return []
    return extract_inorder(node.left) + [node.val] + extract_inorder(node.right)


@given(
    list1=st.lists(st.integers(min_value=-1000, max_value=1000), unique=True, max_size=20),
    list2=st.lists(st.integers(min_value=-1000, max_value=1000), unique=True, max_size=20),
)
def test_property_matches_sorted_oracle(list1, list2):
    root1 = build_bst_from_sorted_list(sorted(list1))
    root2 = build_bst_from_sorted_list(sorted(list2))

    expected = sorted(extract_inorder(root1) + extract_inorder(root2))

    for fn in SOLUTIONS:
        res = fn(root1, root2)
        assert res == expected
        assert len(res) == len(list1) + len(list2)
        assert all(res[i] <= res[i + 1] for i in range(len(res) - 1))
