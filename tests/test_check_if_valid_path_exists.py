import pytest
from hypothesis import given, strategies as st
from collections import deque
from typing import List

from check_if_valid_path_exists import valid_path as valid_path_dfs
from check_if_valid_path_exists_bfs import valid_path_bfs
from check_if_valid_path_exists_union_find import valid_path_union_find

SOLUTIONS = [
    valid_path_dfs,
    valid_path_bfs,
    valid_path_union_find,
]


# --- Independent Reference Oracle ---

def oracle_valid_path(n: int, edges: List[List[int]], source: int, destination: int) -> bool:
    """Independent BFS-based oracle with visited set."""
    if source == destination:
        return True
    adj = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = {source}
    queue = deque([source])
    while queue:
        curr = queue.popleft()
        if curr == destination:
            return True
        for neighbor in adj[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return False


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_same_source_and_destination(fn):
    assert fn(1, [], 0, 0) is True
    assert fn(5, [[0, 1], [1, 2]], 3, 3) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_no_edges_disconnected(fn):
    assert fn(2, [], 0, 1) is False
    assert fn(10, [], 2, 7) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_direct_edge(fn):
    assert fn(2, [[0, 1]], 0, 1) is True
    assert fn(2, [[0, 1]], 1, 0) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # n = 3, edges = [[0,1],[1,2],[2,0]], source = 0, destination = 2 -> True
    edges = [[0, 1], [1, 2], [2, 0]]
    assert fn(3, edges, 0, 2) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # n = 6, edges = [[0,1],[0,2],[3,5],[5,4],[4,3]], source = 0, destination = 5 -> False
    edges = [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]]
    assert fn(6, edges, 0, 5) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_linear_chain(fn):
    # 0 - 1 - 2 - 3 - 4
    edges = [[0, 1], [1, 2], [2, 3], [3, 4]]
    assert fn(5, edges, 0, 4) is True
    assert fn(5, edges, 4, 0) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_star_graph(fn):
    # Center node 0 connected to 1, 2, 3, 4, 5
    edges = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5]]
    assert fn(6, edges, 1, 5) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_multiple_disjoint_components(fn):
    # Comp 1: 0-1-2, Comp 2: 3-4, Comp 3: 5
    edges = [[0, 1], [1, 2], [3, 4]]
    assert fn(6, edges, 0, 2) is True
    assert fn(6, edges, 3, 4) is True
    assert fn(6, edges, 0, 3) is False
    assert fn(6, edges, 2, 5) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_large_adversarial_graph(fn):
    # Long chain of 2,000 nodes
    n = 2000
    edges = [[i, i + 1] for i in range(n - 1)]
    assert fn(n, edges, 0, n - 1) is True
    assert fn(n, edges, n - 1, 0) is True


# --- Hypothesis Property-Based Tests ---

@st.composite
def graph_with_source_dest(draw):
    n = draw(st.integers(min_value=1, max_value=25))
    source = draw(st.integers(min_value=0, max_value=n - 1))
    destination = draw(st.integers(min_value=0, max_value=n - 1))

    all_possible_edges = [(u, v) for u in range(n) for v in range(u + 1, n)]
    if not all_possible_edges:
        selected_edges = []
    else:
        selected_edges = draw(
            st.lists(
                st.sampled_from(all_possible_edges),
                unique=True,
                max_size=min(len(all_possible_edges), 50)
            )
        )
    edges = [[u, v] for u, v in selected_edges]
    return n, edges, source, destination


@given(data=graph_with_source_dest())
def test_hypothesis_matches_oracle(data):
    n, edges, source, destination = data
    expected = oracle_valid_path(n, edges, source, destination)
    for fn in SOLUTIONS:
        assert fn(n, edges, source, destination) == expected
