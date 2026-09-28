import pytest
from hypothesis import given, strategies as st
from collections import deque
from typing import List

from shortest_path_in_binary_matrix import shortest_path_binary_matrix as shortest_path_bfs
from shortest_path_in_binary_matrix_bidirectional import shortest_path_binary_matrix_bidirectional
from shortest_path_in_binary_matrix_astar import shortest_path_binary_matrix_astar

SOLUTIONS = [
    shortest_path_bfs,
    shortest_path_binary_matrix_bidirectional,
    shortest_path_binary_matrix_astar,
]


# --- Independent Reference Oracle ---

def oracle_shortest_path(grid: List[List[int]]) -> int:
    """Independent standard BFS oracle."""
    if not grid or not grid[0] or grid[0][0] != 0 or grid[-1][-1] != 0:
        return -1
    n = len(grid)
    if n == 1:
        return 1

    visited = set([(0, 0)])
    queue = deque([(0, 0, 1)])
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    while queue:
        r, c, d = queue.popleft()
        if (r, c) == (n - 1, n - 1):
            return d
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, d + 1))
    return -1


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_or_degenerate_grid(fn):
    assert fn([]) == -1
    assert fn([[]]) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_cell_open(fn):
    assert fn([[0]]) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_cell_blocked(fn):
    assert fn([[1]]) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_start_or_goal_blocked(fn):
    assert fn([[1, 0], [0, 0]]) == -1
    assert fn([[0, 0], [0, 1]]) == -1
    assert fn([[1, 0], [0, 1]]) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # [[0,1],[1,0]] -> 2
    assert fn([[0, 1], [1, 0]]) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # [[0,0,0],[1,1,0],[1,1,0]] -> 4
    grid = [
        [0, 0, 0],
        [1, 1, 0],
        [1, 1, 0]
    ]
    assert fn(grid) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    # [[1,0,0],[1,1,0],[1,1,0]] -> -1 (start blocked)
    grid = [
        [1, 0, 0],
        [1, 1, 0],
        [1, 1, 0]
    ]
    assert fn(grid) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_direct_diagonal_path(fn):
    # 4x4 with diagonal 0s -> length 4
    n = 4
    grid = [[0 if i == j else 1 for j in range(n)] for i in range(n)]
    assert fn(grid) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_unreachable_surrounded_goal(fn):
    grid = [
        [0, 0, 0],
        [0, 1, 1],
        [0, 1, 0]
    ]
    assert fn(grid) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_large_open_grid(fn):
    # 10x10 all zeros -> straight diagonal is length 10
    n = 10
    grid = [[0] * n for _ in range(n)]
    assert fn(grid) == 10


# --- Hypothesis Property-Based Tests ---

@st.composite
def binary_square_grids(draw, min_n=1, max_n=10):
    n = draw(st.integers(min_value=min_n, max_value=max_n))
    return draw(
        st.lists(
            st.lists(st.sampled_from([0, 1]), min_size=n, max_size=n),
            min_size=n,
            max_size=n
        )
    )


@given(grid=binary_square_grids())
def test_hypothesis_matches_oracle(grid):
    expected = oracle_shortest_path(grid)
    for fn in SOLUTIONS:
        assert fn(grid) == expected


@given(grid=binary_square_grids())
def test_hypothesis_bounds(grid):
    n = len(grid)
    for fn in SOLUTIONS:
        res = fn(grid)
        if res != -1:
            assert n <= res <= (n * n)
