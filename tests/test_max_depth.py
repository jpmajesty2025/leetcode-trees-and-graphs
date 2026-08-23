import pytest
from hypothesis import given, strategies as st
from typing import Optional

from tree_node import TreeNode
from max_depth_of_binary_tree import max_depth, max_depth_iterative, max_depth_bfs

SOLUTIONS = [max_depth, max_depth_iterative, max_depth_bfs]


# --- Helper to construct trees from LeetCode-style level order lists ---
def build_tree_from_list(values: list) -> Optional[TreeNode]:
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
def test_example_tree(fn):
    # [3, 9, 20, None, None, 15, 7]
    root = build_tree_from_list([3, 9, 20, None, None, 15, 7])
    assert fn(root) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_example_skewed_right(fn):
    # [1, None, 2]
    root = build_tree_from_list([1, None, 2])
    assert fn(root) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_left_skewed_chain(fn):
    # 5 -> 4 -> 3 -> 2 -> 1
    root = TreeNode(5, left=TreeNode(4, left=TreeNode(3, left=TreeNode(2, left=TreeNode(1)))))
    assert fn(root) == 5


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_zigzag_tree(fn):
    # 1 -> right: 2 -> left: 3 -> right: 4
    root = TreeNode(1, right=TreeNode(2, left=TreeNode(3, right=TreeNode(4))))
    assert fn(root) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_full_binary_tree(fn):
    # Depth 3 full binary tree: 7 nodes
    root = build_tree_from_list([1, 2, 3, 4, 5, 6, 7])
    assert fn(root) == 3


# --- Hypothesis Property-Based Tests ---

# Recursive generator for binary trees
tree_strategy = st.recursive(
    st.none().map(lambda _: None),
    lambda children: st.builds(TreeNode, val=st.integers(), left=children, right=children),
    max_leaves=25
)


@given(tree=tree_strategy)
def test_all_solutions_equivalent(tree):
    r_res = max_depth(tree)
    i_res = max_depth_iterative(tree)
    b_res = max_depth_bfs(tree)
    assert r_res == i_res == b_res


@given(tree=tree_strategy)
def test_depth_non_negative(tree):
    assert max_depth(tree) >= 0
    assert (max_depth(tree) == 0) == (tree is None)


@given(tree=tree_strategy)
def test_depth_recursive_step_invariant(tree):
    if tree is None:
        assert max_depth(tree) == 0
    else:
        left_d = max_depth(tree.left)
        right_d = max_depth(tree.right)
        assert max_depth(tree) == 1 + max(left_d, right_d)
