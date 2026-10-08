import pytest
from hypothesis import given, strategies as st
from typing import List

from satisfiability_of_equality_equations import equations_possible as solve_dsu
from satisfiability_of_equality_equations_dfs import equations_possible_dfs as solve_dfs

SOLUTIONS = [
    solve_dsu,
    solve_dfs,
]


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_direct_contradiction(fn):
    assert fn(["a==b", "b!=a"]) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_redundant_equality(fn):
    assert fn(["b==a", "a==b"]) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_transitive_equality_satisfied(fn):
    assert fn(["a==b", "b==c", "a==c"]) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_transitive_contradiction(fn):
    # a == b and b == c implies a == c, which contradicts c != a
    assert fn(["a==b", "b==c", "c!=a"]) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_reflexive_inequality(fn):
    # Variable cannot be not equal to itself
    assert fn(["a!=a"]) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_disjoint_components_with_inequality(fn):
    # a == b, c == d, a != c -> valid since they are in disjoint components
    assert fn(["a==b", "c==d", "a!=c"]) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_multiple_variables_chain(fn):
    equations = ["a==b", "b==c", "c==d", "d==e", "e==f", "f!=a"]
    assert fn(equations) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_self_equality(fn):
    assert fn(["c==c", "b==d", "x!=z"]) is True


# --- Hypothesis Property-Based Tests ---

@given(
    equations=st.lists(
        st.tuples(
            st.sampled_from(["a", "b", "c", "d", "e"]),
            st.sampled_from(["==", "!="]),
            st.sampled_from(["a", "b", "c", "d", "e"])
        ).map(lambda t: f"{t[0]}{t[1]}{t[2]}"),
        min_size=1,
        max_size=20
    )
)
def test_dsu_dfs_solutions_equivalence(equations):
    res_dsu = solve_dsu(equations)
    res_dfs = solve_dfs(equations)
    assert res_dsu == res_dfs
