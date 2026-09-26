import pytest
from hypothesis import given, strategies as st
from collections import deque
from typing import List

from number_of_provinces import number_of_provinces
from number_of_provinces_bfs import number_of_provinces_bfs
from number_of_provinces_union_find import number_of_provinces_union_find

SOLUTIONS = [
    number_of_provinces,
    number_of_provinces_bfs,
    number_of_provinces_union_find,
]


# --- Independent Reference Oracle ---

def oracle_number_of_provinces(matrix: List[List[int]]) -> int:
    """Independent BFS-based oracle to compute connected components."""
    n = len(matrix)
    if n == 0:
        return 0
    visited = set()
    count = 0
    for node in range(n):
        if node not in visited:
            count += 1
            visited.add(node)
            queue = deque([node])
            while queue:
                curr = queue.popleft()
                for neighbor in range(n):
                    if matrix[curr][neighbor] == 1 and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
    return count


# --- Deterministic Pytest Test Cases ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_matrix(fn):
    assert fn([]) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_city(fn):
    assert fn([[1]]) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_disconnected_cities(fn):
    assert fn([
        [1, 0],
        [0, 1]
    ]) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_connected_cities(fn):
    assert fn([
        [1, 1],
        [1, 1]
    ]) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # Cities 0 & 1 connected, city 2 isolated -> 2 provinces
    matrix = [
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 1]
    ]
    assert fn(matrix) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # All 3 cities disconnected -> 3 provinces
    matrix = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]
    assert fn(matrix) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_fully_connected_clique(fn):
    n = 5
    matrix = [[1] * n for _ in range(n)]
    assert fn(matrix) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_linear_chain(fn):
    # 0 - 1 - 2 - 3 - 4 -> 1 province
    n = 5
    matrix = [[1 if i == j or abs(i - j) == 1 else 0 for j in range(n)] for i in range(n)]
    assert fn(matrix) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_star_graph(fn):
    # Center node 0 connected to 1, 2, 3, 4 -> 1 province
    n = 5
    matrix = [[1 if i == 0 or j == 0 or i == j else 0 for j in range(n)] for i in range(n)]
    assert fn(matrix) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_multiple_disjoint_components(fn):
    # Group A: {0, 1, 2}, Group B: {3, 4}, Group C: {5} -> 3 provinces
    matrix = [
        [1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1],
    ]
    assert fn(matrix) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_large_disconnected_adversarial(fn):
    # 200 isolated nodes -> 200 provinces
    n = 200
    matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    assert fn(matrix) == 200


# --- Hypothesis Property-Based Tests ---

@st.composite
def symmetric_adjacency_matrices(draw, min_n=1, max_n=25):
    """Generates valid symmetric n x n binary adjacency matrices with 1 on diagonal."""
    n = draw(st.integers(min_value=min_n, max_value=max_n))
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 1
        for j in range(i + 1, n):
            val = draw(st.integers(min_value=0, max_value=1))
            matrix[i][j] = val
            matrix[j][i] = val
    return matrix


@given(matrix=symmetric_adjacency_matrices())
def test_hypothesis_matches_oracle(matrix):
    expected = oracle_number_of_provinces(matrix)
    for fn in SOLUTIONS:
        assert fn(matrix) == expected


@given(matrix=symmetric_adjacency_matrices())
def test_hypothesis_component_count_bounds(matrix):
    n = len(matrix)
    for fn in SOLUTIONS:
        res = fn(matrix)
        assert 1 <= res <= n
