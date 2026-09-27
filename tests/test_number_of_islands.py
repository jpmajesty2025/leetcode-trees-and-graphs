import pytest
from hypothesis import given, strategies as st
from collections import deque
from typing import List

from number_of_islands import number_of_islands
from number_of_islands_bfs import number_of_islands_bfs
from number_of_islands_union_find import number_of_islands_union_find
from number_of_islands_iterative_dfs import num_islands_iterative

SOLUTIONS = [
    number_of_islands,
    number_of_islands_bfs,
    number_of_islands_union_find,
    num_islands_iterative,
]


# --- Independent Reference Oracle ---

def oracle_number_of_islands(grid: List[List[str]]) -> int:
    """Independent BFS oracle calculating connected components."""
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                count += 1
                visited.add((r, c))
                queue = deque([(r, c)])
                while queue:
                    cr, cc = queue.popleft()
                    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1' and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
    return count


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_grids(fn):
    assert fn([]) == 0
    assert fn([[]]) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_cell(fn):
    assert fn([["0"]]) == 0
    assert fn([["1"]]) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_water(fn):
    grid = [
        ["0", "0", "0"],
        ["0", "0", "0"],
        ["0", "0", "0"]
    ]
    assert fn(grid) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_land(fn):
    grid = [
        ["1", "1", "1"],
        ["1", "1", "1"],
        ["1", "1", "1"]
    ]
    assert fn(grid) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    grid = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"]
    ]
    assert fn(grid) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"]
    ]
    assert fn(grid) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_diagonal_islands_are_disconnected(fn):
    grid = [
        ["1", "0"],
        ["0", "1"]
    ]
    assert fn(grid) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_donut_island_with_internal_lake(fn):
    grid = [
        ["1", "1", "1"],
        ["1", "0", "1"],
        ["1", "1", "1"]
    ]
    assert fn(grid) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_checkerboard_pattern(fn):
    grid = [
        ["1", "0", "1"],
        ["0", "1", "0"],
        ["1", "0", "1"]
    ]
    assert fn(grid) == 5


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_serpentine_island(fn):
    grid = [
        ["1", "1", "1", "1"],
        ["0", "0", "0", "1"],
        ["1", "1", "1", "1"],
        ["1", "0", "0", "0"],
        ["1", "1", "1", "1"]
    ]
    assert fn(grid) == 1


# --- Hypothesis Property-Based Tests ---

@st.composite
def binary_grids(draw, min_rows=1, max_rows=15, min_cols=1, max_cols=15):
    rows = draw(st.integers(min_value=min_rows, max_value=max_rows))
    cols = draw(st.integers(min_value=min_cols, max_value=max_cols))
    return draw(
        st.lists(
            st.lists(st.sampled_from(["0", "1"]), min_size=cols, max_size=cols),
            min_size=rows,
            max_size=rows
        )
    )


@given(grid=binary_grids())
def test_hypothesis_matches_oracle(grid):
    expected = oracle_number_of_islands(grid)
    for fn in SOLUTIONS:
        assert fn(grid) == expected


@given(grid=binary_grids())
def test_hypothesis_island_count_bounds(grid):
    rows = len(grid)
    cols = len(grid[0])
    total_cells = rows * cols
    max_possible = (total_cells + 1) // 2
    for fn in SOLUTIONS:
        res = fn(grid)
        assert 0 <= res <= max_possible
