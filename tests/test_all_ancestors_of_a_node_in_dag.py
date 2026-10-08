import pytest
from hypothesis import given, strategies as st
from typing import List

from all_ancestors_of_a_node_in_dag import get_ancestors as solve_forward_dfs
from all_ancestors_of_a_node_in_dag_topo import get_ancestors_topo as solve_topo

SOLUTIONS = [
    solve_forward_dfs,
    solve_topo,
]


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_node(fn):
    assert fn(1, []) == [[]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_disconnected_nodes(fn):
    assert fn(3, []) == [[], [], []]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_linear_chain(fn):
    # 0 -> 1 -> 2
    n = 3
    edges = [[0, 1], [1, 2]]
    assert fn(n, edges) == [[], [0], [0, 1]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_diamond_dag(fn):
    # 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3
    n = 4
    edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
    assert fn(n, edges) == [[], [0], [0], [0, 1, 2]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    n = 8
    edges = [[0, 3], [0, 4], [1, 3], [2, 4], [2, 7], [3, 5], [3, 6], [3, 7], [4, 6]]
    expected = [[], [], [], [0, 1], [0, 2], [0, 1, 3], [0, 1, 2, 3, 4], [0, 1, 2, 3]]
    assert fn(n, edges) == expected


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    n = 5
    edges = [
        [0, 1], [0, 2], [0, 3], [0, 4],
        [1, 2], [1, 3], [1, 4],
        [2, 3], [2, 4],
        [3, 4]
    ]
    expected = [[], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3]]
    assert fn(n, edges) == expected


# --- Hypothesis Property-Based Tests ---

@given(
    n=st.integers(min_value=1, max_value=20),
    data=st.data()
)
def test_dag_solutions_equivalence(n, data):
    # Generate guaranteed DAG by enforcing u < v for all edges
    edges_tuples = data.draw(
        st.lists(
            st.tuples(st.integers(min_value=0, max_value=n - 1), st.integers(min_value=0, max_value=n - 1))
            .filter(lambda pair: pair[0] < pair[1]),
            unique=True,
            max_size=30
        )
    )
    edges = [[u, v] for u, v in edges_tuples]

    res_dfs = solve_forward_dfs(n, edges)
    res_topo = solve_topo(n, edges)

    assert res_dfs == res_topo

    # Verify every ancestor list is strictly sorted and unique
    for ancs in res_dfs:
        assert ancs == sorted(ancs)
        assert len(ancs) == len(set(ancs))
