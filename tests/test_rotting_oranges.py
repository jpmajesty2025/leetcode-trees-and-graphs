import copy
import pytest
from hypothesis import given, strategies as st
from typing import List

from rotting_oranges import oranges_rotting as solve_in_place
from rotting_oranges_immutable import oranges_rotting_immutable as solve_immutable

SOLUTIONS = [
    solve_in_place,
    solve_immutable,
]


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_grid(fn):
    assert fn([]) == 0
    assert fn([[]]) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_empty_cells(fn):
    assert fn([[0, 0], [0, 0]]) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_fresh_no_rotten(fn):
    # Fresh oranges never rot without a source
    assert fn([[1, 1], [1, 1]]) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_rotten(fn):
    assert fn([[2, 2], [2, 2]]) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    grid = [
        [2, 1, 1],
        [1, 1, 0],
        [0, 1, 1]
    ]
    assert fn(copy.deepcopy(grid)) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # Bottom left isolated
    grid = [
        [2, 1, 1],
        [0, 1, 1],
        [1, 0, 1]
    ]
    assert fn(copy.deepcopy(grid)) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    assert fn([[0, 2]]) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_linear_chain(fn):
    assert fn([[2, 1, 1, 1]]) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_multiple_rotten_sources(fn):
    # Two sources meet at the center: [2, 1, 2] -> 1 minute
    assert fn([[2, 1, 2]]) == 1


# --- Hypothesis Property-Based Tests ---

@given(
    rows=st.integers(min_value=1, max_value=8),
    cols=st.integers(min_value=1, max_value=8),
    data=st.data()
)
def test_rotting_solutions_equivalence(rows, cols, data):
    grid = data.draw(
        st.lists(
            st.lists(st.integers(min_value=0, max_value=2), min_size=cols, max_size=cols),
            min_size=rows,
            max_size=rows
        )
    )

    grid_copy1 = copy.deepcopy(grid)
    grid_copy2 = copy.deepcopy(grid)

    res_in_place = solve_in_place(grid_copy1)
    res_immutable = solve_immutable(grid_copy2)

    assert res_in_place == res_immutable
    assert res_in_place >= -1
