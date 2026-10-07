import pytest
from hypothesis import given, strategies as st
from typing import List

from island_perimeter import island_perimeter as solve_iterative
from island_perimeter_dfs import island_perimeter_dfs as solve_dfs

SOLUTIONS = [
    solve_iterative,
    solve_dfs,
]


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_grid(fn):
    assert fn([]) == 0
    assert fn([[]]) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_cell_land(fn):
    assert fn([[1]]) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_cell_water(fn):
    assert fn([[0]]) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_cells_horizontal(fn):
    assert fn([[1, 1]]) == 6


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_cells_vertical(fn):
    assert fn([[1], [1]]) == 6


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_by_two_block(fn):
    # 4 cells * 4 = 16. Shared edges = 4. Perimeter = 16 - 8 = 8
    assert fn([[1, 1], [1, 1]]) == 8


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    grid = [
        [0, 1, 0, 0],
        [1, 1, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0]
    ]
    assert fn(grid) == 16


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    assert fn([[1]]) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    assert fn([[1, 0]]) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_cross_shape(fn):
    # Center (1, 1) and 4 neighbors (0,1), (2,1), (1,0), (1,2)
    # Total cells = 5. Shared edges = 4. Perimeter = 5*4 - 2*4 = 12
    grid = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]
    assert fn(grid) == 12


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_u_shape(fn):
    # 3x3 U-shape (all 1s except top-middle (0,1) and center (1,1))
    grid = [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
    # 7 land cells.
    # Shared edges: (0,0)-(1,0), (1,0)-(2,0), (2,0)-(2,1), (2,1)-(2,2), (2,2)-(1,2), (1,2)-(0,2) = 6 shared edges
    # Perimeter = 7 * 4 - 6 * 2 = 28 - 12 = 16
    assert fn(grid) == 16


# --- Hypothesis Property-Based Tests ---

@given(
    rows=st.integers(min_value=2, max_value=10),
    cols=st.integers(min_value=2, max_value=10),
    num_steps=st.integers(min_value=1, max_value=20),
    data=st.data()
)
def test_connected_island_equivalence(rows, cols, num_steps, data):
    # Generate a guaranteed connected island via random walk
    grid = [[0] * cols for _ in range(rows)]
    r = data.draw(st.integers(min_value=0, max_value=rows - 1))
    c = data.draw(st.integers(min_value=0, max_value=cols - 1))
    grid[r][c] = 1

    curr_r, curr_c = r, c
    for _ in range(num_steps):
        move = data.draw(st.sampled_from([(-1, 0), (1, 0), (0, -1), (0, 1)]))
        nr, nc = curr_r + move[0], curr_c + move[1]
        if 0 <= nr < rows and 0 <= nc < cols:
            grid[nr][nc] = 1
            curr_r, curr_c = nr, nc

    res_iterative = solve_iterative(grid)
    res_dfs = solve_dfs(grid)

    assert res_iterative == res_dfs
    assert res_iterative >= 4  # Any non-empty island has perimeter >= 4
