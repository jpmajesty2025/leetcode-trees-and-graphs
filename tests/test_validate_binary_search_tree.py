import pytest
from hypothesis import given, strategies as st
from typing import Optional, List
import copy

from tree_node import TreeNode
from validate_binary_search_tree import is_valid_bst
from validate_binary_search_tree_iterative import is_valid_bst_iterative

SOLUTIONS = [
    is_valid_bst,
    is_valid_bst_iterative,
]


def build_tree_from_list(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Helper to build a binary tree from level-order list representation with None for empty children."""
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
    assert fn(None) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    assert fn(TreeNode(0)) is True
    assert fn(TreeNode(-42)) is True
    assert fn(TreeNode(2147483647)) is True
    assert fn(TreeNode(-2147483648)) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_valid_two_nodes(fn):
    # Root with smaller left child
    root_left = TreeNode(2, left=TreeNode(1))
    assert fn(root_left) is True

    # Root with larger right child
    root_right = TreeNode(2, right=TreeNode(3))
    assert fn(root_right) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_invalid_two_nodes(fn):
    # Left child greater than root
    root_invalid_left = TreeNode(1, left=TreeNode(2))
    assert fn(root_invalid_left) is False

    # Right child less than root
    root_invalid_right = TreeNode(3, right=TreeNode(2))
    assert fn(root_invalid_right) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_duplicate_values(fn):
    # Duplicate in left child
    root_dup_left = TreeNode(2, left=TreeNode(2))
    assert fn(root_dup_left) is False

    # Duplicate in right child
    root_dup_right = TreeNode(2, right=TreeNode(2))
    assert fn(root_dup_right) is False

    # All identical nodes [1, 1, 1]
    root_all_dup = build_tree_from_list([1, 1, 1])
    assert fn(root_all_dup) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_examples(fn):
    # Example 1: [2, 1, 3] -> True
    tree1 = build_tree_from_list([2, 1, 3])
    assert fn(tree1) is True

    # Example 2: [5, 1, 4, None, None, 3, 6] -> False
    tree2 = build_tree_from_list([5, 1, 4, None, None, 3, 6])
    assert fn(tree2) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_subtle_subtree_ancestor_violations(fn):
    # Node in right subtree is smaller than root: [5, 4, 6, None, None, 3, 7] (3 < 5 violates root bound)
    tree1 = build_tree_from_list([5, 4, 6, None, None, 3, 7])
    assert fn(tree1) is False

    # Node in left subtree is greater than root: [10, 5, 15, 2, 12, None, None] (12 > 10 violates root bound)
    tree2 = build_tree_from_list([10, 5, 15, 2, 12, None, None])
    assert fn(tree2) is False

    # Deep right descendant in left subtree violates root bound: [10, 5, 15, None, 11] (11 > 10)
    tree3 = build_tree_from_list([10, 5, 15, None, 11])
    assert fn(tree3) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_skewed_chains(fn):
    # Strictly decreasing left-skewed: 5 -> 4 -> 3 -> 2 -> 1 (Valid)
    valid_left = TreeNode(5, left=TreeNode(4, left=TreeNode(3, left=TreeNode(2, left=TreeNode(1)))))
    assert fn(valid_left) is True

    # Left-skewed with duplicate: 5 -> 4 -> 4 -> 2 -> 1 (Invalid)
    invalid_left_dup = TreeNode(5, left=TreeNode(4, left=TreeNode(4, left=TreeNode(2, left=TreeNode(1)))))
    assert fn(invalid_left_dup) is False

    # Strictly increasing right-skewed: 1 -> 2 -> 3 -> 4 -> 5 (Valid)
    valid_right = TreeNode(1, right=TreeNode(2, right=TreeNode(3, right=TreeNode(4, right=TreeNode(5)))))
    assert fn(valid_right) is True

    # Right-skewed with decrease: 1 -> 2 -> 4 -> 3 -> 5 (Invalid)
    invalid_right_order = TreeNode(1, right=TreeNode(2, right=TreeNode(4, right=TreeNode(3, right=TreeNode(5)))))
    assert fn(invalid_right_order) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_negative_values(fn):
    # Valid BST with negative and zero values: [-10, -20, 0, -30, -15]
    valid_neg = build_tree_from_list([-10, -20, 0, -30, -15])
    assert fn(valid_neg) is True

    # Invalid BST with negative values: [-10, -5, 0] (-5 > -10 in left subtree)
    invalid_neg = build_tree_from_list([-10, -5, 0])
    assert fn(invalid_neg) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_32_bit_integer_limits(fn):
    min_int = -2147483648
    max_int = 2147483647

    # Valid BST spanning min to max int
    root = TreeNode(0, left=TreeNode(min_int), right=TreeNode(max_int))
    assert fn(root) is True

    # Invalid due to equal boundary at min int
    root_dup_min = TreeNode(min_int, left=TreeNode(min_int))
    assert fn(root_dup_min) is False


# --- Hypothesis Property-Based Tests ---

def sorted_list_to_bst(arr: List[int]) -> Optional[TreeNode]:
    """Helper to convert a sorted array of unique ints to a balanced BST."""
    if not arr:
        return None
    mid = len(arr) // 2
    root = TreeNode(arr[mid])
    root.left = sorted_list_to_bst(arr[:mid])
    root.right = sorted_list_to_bst(arr[mid + 1:])
    return root


def oracle_is_valid_bst(root: Optional[TreeNode]) -> bool:
    """Independent oracle that performs in-order traversal and verifies strict monotonic increase."""
    if not root:
        return True

    values: List[int] = []

    def in_order(node: Optional[TreeNode]):
        if not node:
            return
        in_order(node.left)
        values.append(node.val)
        in_order(node.right)

    in_order(root)
    return all(values[i] < values[i + 1] for i in range(len(values) - 1))


bst_strategy = st.lists(
    st.integers(min_value=-10000, max_value=10000),
    unique=True,
    max_size=50
).map(sorted).map(sorted_list_to_bst)


@given(tree=bst_strategy)
def test_valid_bst_hypothesis(tree):
    expected = oracle_is_valid_bst(tree)
    assert expected is True
    for fn in SOLUTIONS:
        assert fn(tree) is True


@given(
    values=st.lists(
        st.integers(min_value=-1000, max_value=1000),
        min_size=2,
        max_size=30,
        unique=True
    )
)
def test_corrupted_bst_hypothesis(values):
    sorted_vals = sorted(values)
    # Corrupt by swapping first and last element (guaranteed out of order since min_size >= 2 and unique)
    corrupted_vals = list(sorted_vals)
    corrupted_vals[0], corrupted_vals[-1] = corrupted_vals[-1], corrupted_vals[0]

    # Build tree with structure identical to BST but with corrupted values
    def build_corrupted_tree(arr: List[int]) -> Optional[TreeNode]:
        if not arr:
            return None
        mid = len(arr) // 2
        root = TreeNode(arr[mid])
        root.left = build_corrupted_tree(arr[:mid])
        root.right = build_corrupted_tree(arr[mid + 1:])
        return root

    corrupted_tree = build_corrupted_tree(corrupted_vals)
    expected = oracle_is_valid_bst(corrupted_tree)
    for fn in SOLUTIONS:
        assert fn(corrupted_tree) == expected
