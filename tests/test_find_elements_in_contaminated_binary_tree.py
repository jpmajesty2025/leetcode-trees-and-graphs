import pytest
from hypothesis import given, strategies as st
from typing import Optional, List

from tree_node import TreeNode
from find_elements_in_contaminated_binary_tree import FindElements as FindElementsDFS
from find_elements_in_contaminated_binary_tree_bfs import FindElementsBFS
from find_elements_in_contaminated_binary_tree_binary_path import FindElementsBinaryPath

CLASSES = [
    FindElementsDFS,
    FindElementsBFS,
    FindElementsBinaryPath,
]


# --- Helper to build contaminated tree from structure list ---

def build_contaminated_tree(structure: List[Optional[int]]) -> Optional[TreeNode]:
    """Builds a binary tree where all present nodes have val = -1."""
    if not structure or structure[0] is None:
        return None
    root = TreeNode(-1)
    queue = [root]
    i = 1
    while queue and i < len(structure):
        curr = queue.pop(0)
        if i < len(structure) and structure[i] is not None:
            curr.left = TreeNode(-1)
            queue.append(curr.left)
        i += 1
        if i < len(structure) and structure[i] is not None:
            curr.right = TreeNode(-1)
            queue.append(curr.right)
        i += 1
    return root


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("cls", CLASSES)
def test_empty_tree(cls):
    fe = cls(None)
    assert fe.find(0) is False
    assert fe.find(1) is False


@pytest.mark.parametrize("cls", CLASSES)
def test_single_root_node(cls):
    root = TreeNode(-1)
    fe = cls(root)
    assert fe.find(0) is True
    assert fe.find(1) is False
    assert fe.find(2) is False


@pytest.mark.parametrize("cls", CLASSES)
def test_leetcode_example_1(cls):
    # [-1, null, -1] -> root=0, right=2
    root = TreeNode(-1, right=TreeNode(-1))
    fe = cls(root)
    assert fe.find(1) is False
    assert fe.find(2) is True


@pytest.mark.parametrize("cls", CLASSES)
def test_leetcode_example_2(cls):
    # [-1, -1, -1, -1, -1]
    root = build_contaminated_tree([-1, -1, -1, -1, -1])
    fe = cls(root)
    assert fe.find(1) is True
    assert fe.find(3) is True
    assert fe.find(5) is False


@pytest.mark.parametrize("cls", CLASSES)
def test_leetcode_example_3(cls):
    # [-1, null, -1, -1, null, -1]
    root = TreeNode(-1, right=TreeNode(-1, left=TreeNode(-1, left=TreeNode(-1))))
    fe = cls(root)
    assert fe.find(2) is True
    assert fe.find(3) is False
    assert fe.find(4) is False
    assert fe.find(5) is True


@pytest.mark.parametrize("cls", CLASSES)
def test_left_skewed_chain(cls):
    # 0 -> 1 -> 3 -> 7 -> 15
    root = TreeNode(-1, left=TreeNode(-1, left=TreeNode(-1, left=TreeNode(-1, left=TreeNode(-1)))))
    fe = cls(root)
    for val in [0, 1, 3, 7, 15]:
        assert fe.find(val) is True
    for val in [2, 4, 5, 6, 8, 14, 16]:
        assert fe.find(val) is False


# --- Hypothesis Property-Based Tests ---

tree_structure_strategy = st.recursive(
    st.just(TreeNode(-1)),
    lambda children: st.builds(
        TreeNode,
        val=st.just(-1),
        left=st.one_of(st.none(), children),
        right=st.one_of(st.none(), children),
    ),
    max_leaves=15
)


@given(tree=tree_structure_strategy)
def test_hypothesis_root_always_contains_zero(tree):
    for cls in CLASSES:
        fe = cls(tree)
        assert fe.find(0) is True


@given(tree=tree_structure_strategy)
def test_hypothesis_negative_values_not_found(tree):
    for cls in CLASSES:
        fe = cls(tree)
        assert fe.find(-1) is False
        assert fe.find(-100) is False
