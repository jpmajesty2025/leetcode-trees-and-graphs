import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from min_depth_of_binary_tree import min_depth
from min_depth_bfs import min_depth_bfs
from min_depth_iterative import min_depth_iterative

SOLUTIONS = [
    min_depth,
    min_depth_bfs,
    min_depth_iterative,
]


# --- Helper to construct trees from level-order lists ---
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
    # root = [3,9,20,null,null,15,7] -> min depth = 2 (path: 3 -> 9)
    root = build_tree_from_list([3, 9, 20, None, None, 15, 7])
    assert fn(root) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_example_2_skewed_chain(fn):
    # root = [2,null,3,null,4,null,5,null,6] -> min depth = 5
    root = TreeNode(2, right=TreeNode(3, right=TreeNode(4, right=TreeNode(5, right=TreeNode(6)))))
    assert fn(root) == 5


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_left_skewed_chain(fn):
    # 1 -> 2 -> 3 -> 4
    root = TreeNode(1, left=TreeNode(2, left=TreeNode(3, left=TreeNode(4))))
    assert fn(root) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_root_with_single_child(fn):
    # Node 1 has left child 2 only. Min depth is 2, NOT 1 (1 is not a leaf)
    root = TreeNode(1, left=TreeNode(2))
    assert fn(root) == 2

    # Node 1 has right child 2 only. Min depth is 2, NOT 1
    root2 = TreeNode(1, right=TreeNode(2))
    assert fn(root2) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_asymmetric_tree(fn):
    #       1
    #      / \
    #     2   3
    #    /
    #   4
    #  /
    # 5
    # Left leaf is depth 4 (1->2->4->5), Right leaf is depth 2 (1->3) -> min depth is 2
    root = TreeNode(1, left=TreeNode(2, left=TreeNode(4, left=TreeNode(5))), right=TreeNode(3))
    assert fn(root) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_full_binary_tree(fn):
    # Balanced tree of height 3
    root = build_tree_from_list([1, 2, 3, 4, 5, 6, 7])
    assert fn(root) == 3


# --- Hypothesis Property-Based Tests ---

tree_strategy = st.recursive(
    st.none().map(lambda _: None),
    lambda children: st.builds(
        TreeNode,
        val=st.integers(min_value=-1000, max_value=1000),
        left=children,
        right=children,
    ),
    max_leaves=15
)


def oracle_min_depth(node: Optional[TreeNode]) -> int:
    """Independent oracle collecting all root-to-leaf path lengths."""
    if not node:
        return 0
    
    def get_leaf_depths(curr: TreeNode, current_depth: int) -> List[int]:
        if not curr.left and not curr.right:
            return [current_depth]
        depths = []
        if curr.left:
            depths.extend(get_leaf_depths(curr.left, current_depth + 1))
        if curr.right:
            depths.extend(get_leaf_depths(curr.right, current_depth + 1))
        return depths

    return min(get_leaf_depths(node, 1))


@given(tree=tree_strategy)
def test_all_solutions_match_oracle(tree):
    expected = oracle_min_depth(tree)
    for fn in SOLUTIONS:
        assert fn(tree) == expected


@given(tree=tree_strategy)
def test_min_depth_non_negative(tree):
    for fn in SOLUTIONS:
        assert fn(tree) >= 0


@given(val=st.integers(), child=tree_strategy)
def test_single_child_property(val, child):
    """Property: If a tree has only one child, min_depth(root) == 1 + min_depth(child)."""
    if child is not None:
        left_only = TreeNode(val, left=child)
        right_only = TreeNode(val, right=child)
        expected = 1 + oracle_min_depth(child)
        for fn in SOLUTIONS:
            assert fn(left_only) == expected
            assert fn(right_only) == expected
