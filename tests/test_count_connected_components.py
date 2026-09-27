import pytest
from hypothesis import given, strategies as st
from collections import deque
from typing import List

from count_connected_components import count_components as count_components_dfs
from count_connected_components_bfs import count_components_bfs
from count_connected_components_union_find import count_components_union_find

SOLUTIONS = [
    count_components_dfs,
    count_components_bfs,
    count_components_union_find,
]


# --- Independent Reference Oracle ---

def oracle_count_components(n: int, edges: List[List[int]]) -> int:
    """Independent BFS-based oracle to calculate component count."""
    if n <= 0:
        return 0
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = set()
    components = 0
    for node in range(n):
        if node not in visited:
            components += 1
            visited.add(node)
            queue = deque([node])
            while queue:
                curr = queue.popleft()
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
    return components


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_zero_nodes(fn):
    assert fn(0, []) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_no_edges(fn):
    assert fn(1, []) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_disconnected_nodes(fn):
    assert fn(5, []) == 5


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # n = 5 and edges = [[0, 1], [1, 2], [3, 4]] -> 2
    edges = [[0, 1], [1, 2], [3, 4]]
    assert fn(5, edges) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # n = 5 and edges = [[0, 1], [1, 2], [2, 3], [3, 4]] -> 1
    edges = [[0, 1], [1, 2], [2, 3], [3, 4]]
    assert fn(5, edges) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_cycle_graph(fn):
    # Triangle cycle: 0-1, 1-2, 2-0 plus isolated node 3 -> 2 components
    edges = [[0, 1], [1, 2], [2, 0]]
    assert fn(4, edges) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_star_graph(fn):
    # Center node 0 connected to 1, 2, 3, 4 -> 1 component
    edges = [[0, 1], [0, 2], [0, 3], [0, 4]]
    assert fn(5, edges) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_multiple_disjoint_clusters(fn):
    # Cluster 1: {0,1,2}, Cluster 2: {3,4,5}, Cluster 3: {6}, Cluster 4: {7,8} -> 4 components
    edges = [
        [0, 1], [1, 2], [2, 0],
        [3, 4], [4, 5],
        [7, 8]
    ]
    assert fn(9, edges) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_large_adversarial_graph(fn):
    # 1,000 nodes chain + 500 isolated nodes -> 501 components
    n = 1500
    edges = [[i, i + 1] for i in range(999)]
    assert fn(n, edges) == 501


# --- Hypothesis Property-Based Tests ---

@st.composite
def graph_data(draw):
    n = draw(st.integers(min_value=1, max_value=30))
    all_possible_edges = [(u, v) for u in range(n) for v in range(u + 1, n)]
    if not all_possible_edges:
        selected_edges = []
    else:
        selected_edges = draw(
            st.lists(
                st.sampled_from(all_possible_edges),
                unique=True,
                max_size=min(len(all_possible_edges), 60)
            )
        )
    edges = [[u, v] for u, v in selected_edges]
    return n, edges


@given(data=graph_data())
def test_hypothesis_matches_oracle(data):
    n, edges = data
    expected = oracle_count_components(n, edges)
    for fn in SOLUTIONS:
        assert fn(n, edges) == expected


@given(data=graph_data())
def test_hypothesis_component_bounds(data):
    n, edges = data
    for fn in SOLUTIONS:
        res = fn(n, edges)
        # Components must be between 1 (fully connected) and n (all isolated)
        assert 1 <= res <= n
