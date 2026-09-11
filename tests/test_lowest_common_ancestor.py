import pytest
from hypothesis import given, strategies as st
from typing import Optional, List, Dict, Tuple, Set

from tree_node import TreeNode
from lowest_common_ancestor_of_binary_tree import lowest_common_ancestor
from lowest_common_ancestor_iterative import lowest_common_ancestor_iterative

SOLUTIONS = [
    lowest_common_ancestor,
    lowest_common_ancestor_iterative,
]


# --- Helper to construct trees and return a map of val -> TreeNode ---
def build_tree_with_map(values: List[Optional[int]]) -> Tuple[Optional[TreeNode], Dict[int, TreeNode]]:
    if not values or values[0] is None:
        return None, {}
    root = TreeNode(values[0])
    node_map = {values[0]: root}
    queue = [root]
    i = 1
    while queue and i < len(values):
        current = queue.pop(0)
        if i < len(values) and values[i] is not None:
            val = values[i]
            current.left = TreeNode(val)
            node_map[val] = current.left
            queue.append(current.left)
        i += 1
        if i < len(values) and values[i] is not None:
            val = values[i]
            current.right = TreeNode(val)
            node_map[val] = current.right
            queue.append(current.right)
        i += 1
    return root, node_map


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_example_1_lca_is_root(fn):
    # root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1 -> LCA is 3
    root, nodes = build_tree_with_map([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    p = nodes[5]
    q = nodes[1]
    assert fn(root, p, q) is nodes[3]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_example_2_lca_is_ancestor_node(fn):
    # root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4 -> LCA is 5
    root, nodes = build_tree_with_map([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    p = nodes[5]
    q = nodes[4]
    assert fn(root, p, q) is nodes[5]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_example_3_two_node_tree(fn):
    # root = [1,2], p = 1, q = 2 -> LCA is 1
    root, nodes = build_tree_with_map([1, 2])
    p = nodes[1]
    q = nodes[2]
    assert fn(root, p, q) is nodes[1]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_deep_cousin_nodes(fn):
    # root = [3,5,1,6,2,0,8,null,null,7,4], p = 7, q = 8 -> LCA is 3
    root, nodes = build_tree_with_map([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    p = nodes[7]
    q = nodes[8]
    assert fn(root, p, q) is nodes[3]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_siblings_on_right_subtree(fn):
    # root = [3,5,1,6,2,0,8,null,null,7,4], p = 0, q = 8 -> LCA is 1
    root, nodes = build_tree_with_map([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    p = nodes[0]
    q = nodes[8]
    assert fn(root, p, q) is nodes[1]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_skewed_chain(fn):
    # 1 -> 2 -> 3 -> 4 -> 5
    node5 = TreeNode(5)
    node4 = TreeNode(4, left=node5)
    node3 = TreeNode(3, left=node4)
    node2 = TreeNode(2, left=node3)
    root = TreeNode(1, left=node2)
    
    assert fn(root, node3, node5) is node3
    assert fn(root, node2, node4) is node2
    assert fn(root, node1:=root, node5) is root


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_none_inputs(fn):
    root = TreeNode(1)
    p = TreeNode(2)
    assert fn(None, p, p) is None
    assert fn(root, None, p) is None
    assert fn(root, p, None) is None


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_node_is_same_as_other(fn):
    # p and q are the same node
    root = TreeNode(1, left=TreeNode(2))
    p = root.left
    assert fn(root, p, p) is p


def test_iterative_node_not_in_tree():
    # Specific edge case: target node does not exist in tree
    root = TreeNode(1, left=TreeNode(2))
    orphan = TreeNode(99)
    assert lowest_common_ancestor_iterative(root, root.left, orphan) is None


# --- Hypothesis Property-Based Tests ---

from typing import Tuple, Set

def collect_all_nodes(node: Optional[TreeNode]) -> List[TreeNode]:
    if not node:
        return []
    return [node] + collect_all_nodes(node.left) + collect_all_nodes(node.right)


def find_path_from_root(root: Optional[TreeNode], target: TreeNode) -> Optional[List[TreeNode]]:
    """Oracle helper: finds path from root to target node."""
    if not root:
        return None
    if root is target:
        return [root]
    
    left_path = find_path_from_root(root.left, target)
    if left_path is not None:
        return [root] + left_path
        
    right_path = find_path_from_root(root.right, target)
    if right_path is not None:
        return [root] + right_path
        
    return None


def oracle_lca(root: TreeNode, p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """Independent oracle: computes intersection of root-to-node paths."""
    path_p = find_path_from_root(root, p)
    path_q = find_path_from_root(root, q)
    if not path_p or not path_q:
        return None
    
    lca = None
    for n1, n2 in zip(path_p, path_q):
        if n1 is n2:
            lca = n1
        else:
            break
    return lca


# Strategy for generating binary trees with unique node values
unique_tree_strategy = st.recursive(
    st.integers(min_value=-1000, max_value=1000).map(lambda v: TreeNode(v)),
    lambda children: st.builds(
        TreeNode,
        val=st.integers(min_value=-1000, max_value=1000),
        left=st.one_of(st.none(), children),
        right=st.one_of(st.none(), children),
    ),
    max_leaves=12
)


@given(tree=unique_tree_strategy, data=st.data())
def test_lca_matches_oracle_and_symmetry(tree, data):
    nodes = collect_all_nodes(tree)
    if len(nodes) < 2:
        return
    
    p = data.draw(st.sampled_from(nodes))
    remaining = [n for n in nodes if n is not p]
    q = data.draw(st.sampled_from(remaining))
    
    expected = oracle_lca(tree, p, q)
    
    for fn in SOLUTIONS:
        result_pq = fn(tree, p, q)
        result_qp = fn(tree, q, p)
        # Symmetry property
        assert result_pq is result_qp
        # Correctness vs independent oracle
        assert result_pq is expected
