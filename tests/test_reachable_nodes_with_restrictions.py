import pytest
from hypothesis import given, strategies as st
from collections import deque
from typing import List

from reachable_nodes_with_restrictions import reachable_nodes as reachable_nodes_bfs
from reachable_nodes_with_restrictions_dfs import reachable_nodes_dfs
from reachable_nodes_with_restrictions_union_find import reachable_nodes_union_find

SOLUTIONS = [
    reachable_nodes_bfs,
    reachable_nodes_dfs,
    reachable_nodes_union_find,
]


# --- Independent Reference Oracle ---

def oracle_reachable_nodes(n: int, edges: List[List[int]], restricted: List[int]) -> int:
    """Independent BFS-based oracle."""
    if n <= 0:
        return 0
    restricted_set = set(restricted)
    if 0 in restricted_set:
        return 0

    adj = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = {0}
    queue = deque([0])
    count = 0

    while queue:
        curr = queue.popleft()
        count += 1
        for neighbor in adj[curr]:
            if neighbor not in visited and neighbor not in restricted_set:
                visited.add(neighbor)
                queue.append(neighbor)

    return count


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_zero_nodes(fn):
    assert fn(0, [], []) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node_tree(fn):
    assert fn(1, [], []) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_no_restricted_nodes(fn):
    edges = [[0, 1], [0, 2], [0, 3]]
    assert fn(4, edges, []) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # n = 7, edges = [[0,1],[1,2],[3,1],[4,0],[0,5],[5,6]], restricted = [4,5] -> 4
    edges = [[0, 1], [1, 2], [3, 1], [4, 0], [0, 5], [5, 6]]
    restricted = [4, 5]
    assert fn(7, edges, restricted) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # n = 7, edges = [[0,1],[0,2],[0,5],[0,4],[3,2],[6,5]], restricted = [4,2,1] -> 3
    edges = [[0, 1], [0, 2], [0, 5], [0, 4], [3, 2], [6, 5]]
    restricted = [4, 2, 1]
    assert fn(7, edges, restricted) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_neighbors_restricted(fn):
    # Node 0 connected to 1, 2, 3; all 1, 2, 3 restricted -> 1
    edges = [[0, 1], [0, 2], [0, 3]]
    restricted = [1, 2, 3]
    assert fn(4, edges, restricted) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_linear_chain_blocked_in_middle(fn):
    # 0 - 1 - 2 - 3 - 4 with 2 restricted -> {0, 1} reachable = 2
    edges = [[0, 1], [1, 2], [2, 3], [3, 4]]
    restricted = [2]
    assert fn(5, edges, restricted) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_linear_chain_blocked_at_end(fn):
    # 0 - 1 - 2 - 3 - 4 with 4 restricted -> {0, 1, 2, 3} reachable = 4
    edges = [[0, 1], [1, 2], [2, 3], [3, 4]]
    restricted = [4]
    assert fn(5, edges, restricted) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_deep_adversarial_tree(fn):
    # 1,000 node linear chain with node 500 restricted -> 500 reachable
    n = 1000
    edges = [[i, i + 1] for i in range(n - 1)]
    restricted = [500]
    assert fn(n, edges, restricted) == 500


# --- Hypothesis Property-Based Tests ---

@st.composite
def tree_with_restrictions(draw, min_nodes=1, max_nodes=25):
    """Generates a random valid tree with random restricted subsets excluding node 0."""
    n = draw(st.integers(min_value=min_nodes, max_value=max_nodes))
    if n == 1:
        return n, [], []

    edges = []
    for i in range(1, n):
        parent = draw(st.integers(min_value=0, max_value=i - 1))
        edges.append([parent, i])

    other_nodes = list(range(1, n))
    restricted = draw(
        st.lists(
            st.sampled_from(other_nodes),
            unique=True,
            max_size=len(other_nodes)
        )
    )
    return n, edges, restricted


@given(data=tree_with_restrictions())
def test_hypothesis_matches_oracle(data):
    n, edges, restricted = data
    expected = oracle_reachable_nodes(n, edges, restricted)
    for fn in SOLUTIONS:
        assert fn(n, edges, restricted) == expected


@given(data=tree_with_restrictions())
def test_hypothesis_bounds(data):
    n, edges, restricted = data
    for fn in SOLUTIONS:
        res = fn(n, edges, restricted)
        assert 1 <= res <= (n - len(restricted))
