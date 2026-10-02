import pytest
from hypothesis import given, strategies as st
from typing import Optional, List
from collections import deque, defaultdict

from tree_node import TreeNode
from all_nodes_distance_k_in_binary_tree import distance_k as distance_k_bfs
from all_nodes_distance_k_in_binary_tree_dfs import distance_k_dfs
from all_nodes_distance_k_in_binary_tree_graph import distance_k_graph

SOLUTIONS = [
    distance_k_bfs,
    distance_k_dfs,
    distance_k_graph,
]


# --- Helpers ---

def build_tree_from_list(values: List[Optional[int]]) -> Optional[TreeNode]:
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        curr = queue.pop(0)
        if i < len(values) and values[i] is not None:
            curr.left = TreeNode(values[i])
            queue.append(curr.left)
        i += 1
        if i < len(values) and values[i] is not None:
            curr.right = TreeNode(values[i])
            queue.append(curr.right)
        i += 1
    return root


def find_node(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    if not root:
        return None
    if root.val == val:
        return root
    return find_node(root.left, val) or find_node(root.right, val)


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_k_equals_zero(fn):
    # Tree: [1, 2, 3], target=2, k=0 -> [2]
    root = build_tree_from_list([1, 2, 3])
    target = find_node(root, 2)
    assert fn(root, target, 0) == [2]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # root = [3,5,1,6,2,0,8,null,null,7,4], target = 5, k = 2
    # Output: [7, 4, 1] (in any order)
    root = build_tree_from_list([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    target = find_node(root, 5)
    assert set(fn(root, target, 2)) == {7, 4, 1}


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # root = [1], target = 1, k = 3 -> []
    root = TreeNode(1)
    assert fn(root, root, 3) == []


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_linear_chain_from_leaf(fn):
    # 1 -> 2 -> 3 -> 4 -> 5, target=5, k=2 -> [3]
    root = TreeNode(1, left=TreeNode(2, left=TreeNode(3, left=TreeNode(4, left=TreeNode(5)))))
    target = find_node(root, 5)
    assert fn(root, target, 2) == [3]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_linear_chain_from_middle(fn):
    # 1 -> 2 -> 3 -> 4 -> 5, target=3, k=2 -> [1, 5]
    root = TreeNode(1, left=TreeNode(2, left=TreeNode(3, left=TreeNode(4, left=TreeNode(5)))))
    target = find_node(root, 3)
    assert set(fn(root, target, 2)) == {1, 5}


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_target_at_root(fn):
    # root=[0,1,2,3,4,5,6], target=0, k=2 -> [3,4,5,6]
    root = build_tree_from_list([0, 1, 2, 3, 4, 5, 6])
    assert set(fn(root, root, 2)) == {3, 4, 5, 6}


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_target_not_present_or_none(fn):
    assert fn(None, TreeNode(1), 2) == []
