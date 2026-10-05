import pytest
from hypothesis import given, strategies as st
from typing import List

from check_for_contradictions_in_equations import check_contradictions as check_contradictions_dsu
from check_for_contradictions_in_equations_bfs import check_contradictions_bfs

SOLUTIONS = [
    check_contradictions_dsu,
    check_contradictions_bfs,
]


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    equations = [["a", "b"], ["b", "c"], ["a", "c"]]
    values = [3.0, 0.5, 1.5]
    assert fn(equations, values) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    equations = [["le", "et"], ["co", "de"], ["et", "co"], ["code", "et"]]
    values = [2.0, 5.0, 0.5, 0.5]
    # No contradiction between the first 3, code and et is independent variable name
    assert fn(equations, values) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_direct_contradiction(fn):
    equations = [["a", "b"], ["b", "c"], ["a", "c"]]
    values = [2.0, 3.0, 5.0]  # a/c should be 6.0, not 5.0
    assert fn(equations, values) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_same_variable_contradiction(fn):
    equations = [["a", "a"]]
    values = [2.0]
    assert fn(equations, values) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_same_variable_consistent(fn):
    equations = [["a", "a"]]
    values = [1.0]
    assert fn(equations, values) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_disconnected_components(fn):
    equations = [["a", "b"], ["c", "d"]]
    values = [2.0, 3.0]
    assert fn(equations, values) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_input(fn):
    assert fn([], []) is False


# --- Hypothesis Property-Based Tests ---

@st.composite
def consistent_system_strategy(draw):
    var_names = ["a", "b", "c", "d", "e", "f"]
    valuations = {v: draw(st.floats(min_value=1.0, max_value=20.0)) for v in var_names}
    
    num_equations = draw(st.integers(min_value=1, max_value=10))
    equations: List[List[str]] = []
    values: List[float] = []

    for _ in range(num_equations):
        u = draw(st.sampled_from(var_names))
        v = draw(st.sampled_from(var_names))
        equations.append([u, v])
        values.append(valuations[u] / valuations[v])

    corrupt = draw(st.booleans())
    if corrupt and equations:
        corrupt_idx = draw(st.integers(min_value=0, max_value=len(equations) - 1))
        values[corrupt_idx] *= 2.0  # Introduce contradiction

    return equations, values, corrupt


@given(data=consistent_system_strategy())
def test_hypothesis_dsu_vs_bfs_equivalence(data):
    equations, values, _ = data
    dsu_result = check_contradictions_dsu(equations, values)
    bfs_result = check_contradictions_bfs(equations, values)
    assert dsu_result == bfs_result
