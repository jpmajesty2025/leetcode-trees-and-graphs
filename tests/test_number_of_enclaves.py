import copy
import pytest
from hypothesis import given, strategies as st
from typing import List

from number_of_enclaves import num_enclaves as solve_dfs
from number_of_enclaves_bfs import num_enclaves_bfs as solve_bfs

SOLUTIONS = [
    solve_dfs,
    solve_bfs,
]


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_grid(fn):
    assert fn([]) == 0
    assert fn([[]]) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_water(fn):
    grid = [[0, 0], [0, 0]]
    assert fn(copy.deepcopy(grid)) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_land(fn):
    grid = [[1, 1], [1, 1]]
    assert fn(copy.deepcopy(grid)) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_enclave_in_center(fn):
    grid = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    assert fn(copy.deepcopy(grid)) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    grid = [
        [0, 0, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]
    assert fn(copy.deepcopy(grid)) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    grid = [
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ]
    assert fn(copy.deepcopy(grid)) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_multiple_isolated_enclaves(fn):
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    assert fn(copy.deepcopy(grid)) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_diagonal_isolation(fn):
    # Diagonals do not connect (4-directional only)
    grid = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]
    # Center (1,1) is enclosed by 0s orthogonally
    assert fn(copy.deepcopy(grid)) == 1


# --- Hypothesis Property-Based Tests ---

@given(
    rows=st.integers(min_value=1, max_value=12),
    cols=st.integers(min_value=1, max_value=12),
    data=st.data()
)
def test_dfs_bfs_equivalence(rows, cols, data):
    grid = data.draw(
        st.lists(
            st.lists(st.integers(min_value=0, max_value=1), min_size=cols, max_size=cols),
            min_size=rows,
            max_size=rows
        )
    )
    grid_copy1 = copy.deepcopy(grid)
    grid_copy2 = copy.deepcopy(grid)

    res_dfs = solve_dfs(grid_copy1)
    res_bfs = solve_bfs(grid_copy2)

    assert res_dfs == res_bfs
    assert res_dfs >= 0
