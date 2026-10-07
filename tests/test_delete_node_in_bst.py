import pytest
from hypothesis import given, strategies as st
from typing import Optional, List
from collections import deque

from tree_node import TreeNode
from delete_node_in_bst import delete_node as delete_node_recursive
from delete_node_in_bst_iterative import delete_node_iterative

SOLUTIONS = [
    delete_node_recursive,
    delete_node_iterative,
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


def inorder(node: Optional[TreeNode]) -> List[int]:
    """Extract in-order traversal of a binary tree."""
    if not node:
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)


def is_valid_bst(node: Optional[TreeNode], min_val=float('-inf'), max_val=float('inf')) -> bool:
    """Validate that tree satisfies BST properties."""
    if not node:
        return True
    if not (min_val < node.val < max_val):
        return False
    return is_valid_bst(node.left, min_val, node.val) and is_valid_bst(node.right, node.val, max_val)


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_tree(fn):
    assert fn(None, 5) is None


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_match(fn):
    root = TreeNode(5)
    assert fn(root, 5) is None


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_no_match(fn):
    root = TreeNode(5)
    res = fn(root, 10)
    assert res is not None
    assert res.val == 5


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_delete_leaf_node(fn):
    # root = [5,3,6,2,4,null,7], delete 7 (leaf)
    root = build_tree_from_list([5, 3, 6, 2, 4, None, 7])
    res = fn(root, 7)
    assert is_valid_bst(res)
    assert inorder(res) == [2, 3, 4, 5, 6]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_delete_node_with_one_child(fn):
    # root = [5,3,6,2,null,null,7], delete 3 (has left child 2)
    root = build_tree_from_list([5, 3, 6, 2, None, None, 7])
    res = fn(root, 3)
    assert is_valid_bst(res)
    assert inorder(res) == [2, 5, 6, 7]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_delete_node_with_two_children(fn):
    # root = [5,3,6,2,4,null,7], delete 3 (has children 2 and 4)
    root = build_tree_from_list([5, 3, 6, 2, 4, None, 7])
    res = fn(root, 3)
    assert is_valid_bst(res)
    assert inorder(res) == [2, 4, 5, 6, 7]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_delete_root_with_two_children(fn):
    # root = [5,3,6,2,4,null,7], delete 5 (root)
    root = build_tree_from_list([5, 3, 6, 2, 4, None, 7])
    res = fn(root, 5)
    assert is_valid_bst(res)
    assert inorder(res) == [2, 3, 4, 6, 7]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_delete_from_left_skewed_chain(fn):
    # 5 -> 4 -> 3 -> 2 -> 1, delete 3
    root = TreeNode(5, left=TreeNode(4, left=TreeNode(3, left=TreeNode(2, left=TreeNode(1)))))
    res = fn(root, 3)
    assert is_valid_bst(res)
    assert inorder(res) == [1, 2, 4, 5]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_delete_from_right_skewed_chain(fn):
    # 1 -> 2 -> 3 -> 4 -> 5, delete 1 (root)
    root = TreeNode(1, right=TreeNode(2, right=TreeNode(3, right=TreeNode(4, right=TreeNode(5)))))
    res = fn(root, 1)
    assert is_valid_bst(res)
    assert inorder(res) == [2, 3, 4, 5]


# --- Hypothesis Property-Based Tests ---

@given(
    nums=st.lists(st.integers(min_value=-1000, max_value=1000), unique=True, min_size=1, max_size=30),
    data=st.data()
)
def test_delete_existing_node_property(nums, data):
    sorted_nums = sorted(nums)
    key_to_delete = data.draw(st.sampled_from(sorted_nums))
    expected_inorder = [x for x in sorted_nums if x != key_to_delete]

    for fn in SOLUTIONS:
        root = build_bst_from_sorted_list(sorted_nums)
        res = fn(root, key_to_delete)
        assert is_valid_bst(res)
        assert inorder(res) == expected_inorder


@given(
    nums=st.lists(st.integers(min_value=-1000, max_value=1000), unique=True, min_size=1, max_size=30),
    data=st.data()
)
def test_delete_non_existing_node_property(nums, data):
    sorted_nums = sorted(nums)
    absent_key = data.draw(st.integers(min_value=-2000, max_value=2000).filter(lambda x: x not in sorted_nums))

    for fn in SOLUTIONS:
        root = build_bst_from_sorted_list(sorted_nums)
        res = fn(root, absent_key)
        assert is_valid_bst(res)
        assert inorder(res) == sorted_nums
