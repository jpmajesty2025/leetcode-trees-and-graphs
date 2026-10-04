import pytest
from hypothesis import given, strategies as st
from collections import defaultdict
from typing import List

from evaluate_division import calc_equation as calc_equation_uf
from evaluate_division_dfs import calc_equation_dfs

SOLUTIONS = [
    calc_equation_uf,
    calc_equation_dfs,
]


# --- Independent Reference Oracle (BFS Path Search) ---

def oracle_calc_equation(
    equations: List[List[str]], values: List[float], queries: List[List[str]]
) -> List[float]:
    graph = defaultdict(dict)
    for (a, b), val in zip(equations, values):
        graph[a][b] = val
        graph[b][a] = 1.0 / val

    results = []
    for start, end in queries:
        if start not in graph or end not in graph:
            results.append(-1.0)
            continue
        if start == end:
            results.append(1.0)
            continue

        queue = [(start, 1.0)]
        visited = {start}
        found = False

        while queue:
            curr, curr_val = queue.pop(0)
            if curr == end:
                results.append(curr_val)
                found = True
                break

            for nbr, weight in graph[curr].items():
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append((nbr, curr_val * weight))

        if not found:
            results.append(-1.0)

    return results


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # equations = [["a","b"],["b","c"]], values = [2.0,3.0]
    # queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
    # Output: [6.0, 0.5, -1.0, 1.0, -1.0]
    equations = [["a", "b"], ["b", "c"]]
    values = [2.0, 3.0]
    queries = [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]]
    expected = [6.0, 0.5, -1.0, 1.0, -1.0]
    res = fn(equations, values, queries)
    assert res == pytest.approx(expected)


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # equations = [["a","b"],["b","c"],["bc","cd"]], values = [1.5,2.5,5.0]
    # queries = [["a","c"],["c","b"],["bc","cd"],["cd","bc"]]
    equations = [["a", "b"], ["b", "c"], ["bc", "cd"]]
    values = [1.5, 2.5, 5.0]
    queries = [["a", "c"], ["c", "b"], ["bc", "cd"], ["cd", "bc"]]
    expected = [3.75, 0.4, 5.0, 0.2]
    res = fn(equations, values, queries)
    assert res == pytest.approx(expected)


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    # equations = [["a","b"]], values = [0.5]
    # queries = [["a","b"],["b","a"],["a","c"],["x","y"]]
    equations = [["a", "b"]]
    values = [0.5]
    queries = [["a", "b"], ["b", "a"], ["a", "c"], ["x", "y"]]
    expected = [0.5, 2.0, -1.0, -1.0]
    res = fn(equations, values, queries)
    assert res == pytest.approx(expected)


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_disconnected_components(fn):
    # a/b = 2.0, c/d = 3.0 -> a/d = -1.0
    equations = [["a", "b"], ["c", "d"]]
    values = [2.0, 3.0]
    queries = [["a", "d"], ["b", "c"], ["a", "b"], ["c", "d"]]
    expected = [-1.0, -1.0, 2.0, 3.0]
    res = fn(equations, values, queries)
    assert res == pytest.approx(expected)


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_long_chain(fn):
    # a/b=2, b/c=3, c/d=4, d/e=5 -> a/e = 120.0
    equations = [["a", "b"], ["b", "c"], ["c", "d"], ["d", "e"]]
    values = [2.0, 3.0, 4.0, 5.0]
    queries = [["a", "e"], ["e", "a"], ["b", "e"]]
    expected = [120.0, 1.0 / 120.0, 60.0]
    res = fn(equations, values, queries)
    assert res == pytest.approx(expected)


# --- Hypothesis Property-Based Tests ---

@st.composite
def equation_system_strategy(draw):
    var_names = ["a", "b", "c", "d", "e", "f"]
    # Assign consistent ground-truth values to each variable
    var_values = {v: draw(st.floats(min_value=0.5, max_value=50.0)) for v in var_names}

    num_eqs = draw(st.integers(min_value=1, max_value=5))
    equations = []
    values = []
    for _ in range(num_eqs):
        u = draw(st.sampled_from(var_names))
        v = draw(st.sampled_from([x for x in var_names if x != u]))
        equations.append([u, v])
        values.append(var_values[u] / var_values[v])

    num_queries = draw(st.integers(min_value=1, max_value=6))
    queries = []
    for _ in range(num_queries):
        u = draw(st.sampled_from(var_names + ["z"]))
        v = draw(st.sampled_from(var_names + ["w"]))
        queries.append([u, v])

    return equations, values, queries


@given(data=equation_system_strategy())
def test_hypothesis_matches_oracle(data):
    equations, values, queries = data
    expected = oracle_calc_equation(equations, values, queries)
    for fn in SOLUTIONS:
        res = fn(equations, values, queries)
        assert res == pytest.approx(expected, rel=1e-4, abs=1e-4)
