import pytest
from hypothesis import given, strategies as st
from collections import deque
from typing import List

from max_area_of_island import max_area_of_island as max_area_dfs
from max_area_of_island_bfs import max_area_of_island_bfs
from max_area_of_island_union_find import max_area_of_island_union_find

SOLUTIONS = [
    max_area_dfs,
    max_area_of_island_bfs,
    max_area_of_island_union_find,
]


# --- Independent Reference Oracle ---

def oracle_max_area_of_island(grid: List[List[int]]) -> int:
    """Independent BFS-based oracle to compute max island area."""
    if not grid or not grid[0]:
        return 0
    m, n = len(grid), len(grid[0])
    visited = set()
    max_area = 0

    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1 and (r, c) not in visited:
                visited.add((r, c))
                queue = deque([(r, c)])
                area = 0
                while queue:
                    cr, cc = queue.popleft()
                    area += 1
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                max_area = max(max_area, area)

    return max_area


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_grids(fn):
    assert fn([]) == 0
    assert fn([[]]) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_cell(fn):
    assert fn([[0]]) == 0
    assert fn([[1]]) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_water(fn):
    grid = [
        [0, 0, 0],
        [0, 0, 0]
    ]
    assert fn(grid) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_land(fn):
    grid = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    assert fn(grid) == 9


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    grid = [
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
    ]
    assert fn(grid) == 6


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    grid = [[0, 0, 0, 0, 0, 0, 0, 0]]
    assert fn(grid) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_diagonal_isolated_islands(fn):
    # Diagonals do not connect -> max area is 1
    grid = [
        [1, 0],
        [0, 1]
    ]
    assert fn(grid) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_donut_lake_island(fn):
    # Ring of 8 land cells surrounding water cell
    grid = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
    assert fn(grid) == 8


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_l_shaped_island(fn):
    grid = [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1]
    ]
    assert fn(grid) == 5


# --- Hypothesis Property-Based Tests ---

@st.composite
def binary_int_grids(draw, min_rows=1, max_rows=15, min_cols=1, max_cols=15):
    rows = draw(st.integers(min_value=min_rows, max_value=max_rows))
    cols = draw(st.integers(min_value=min_cols, max_value=max_cols))
    return draw(
        st.lists(
            st.lists(st.sampled_from([0, 1]), min_size=cols, max_size=cols),
            min_size=rows,
            max_size=rows
        )
    )


@given(grid=binary_int_grids())
def test_hypothesis_matches_oracle(grid):
    expected = oracle_max_area_of_island(grid)
    for fn in SOLUTIONS:
        assert fn(grid) == expected


@given(grid=binary_int_grids())
def test_hypothesis_area_bounds(grid):
    m = len(grid)
    n = len(grid[0])
    total_cells = m * n
    for fn in SOLUTIONS:
        res = fn(grid)
        assert 0 <= res <= total_cells
