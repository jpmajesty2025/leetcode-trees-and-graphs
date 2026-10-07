import pytest
from hypothesis import given, strategies as st
from typing import List

from maximal_network_rank import maximal_network_rank as solve_pairwise
from maximal_network_rank_optimized import maximal_network_rank_optimized as solve_optimized

SOLUTIONS = [
    solve_pairwise,
    solve_optimized,
]


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_nodes_disconnected(fn):
    assert fn(2, []) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_nodes_connected(fn):
    assert fn(2, [[0, 1]]) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # n = 4, roads = [[0,1],[0,3],[1,2],[1,3]] -> 4
    assert fn(4, [[0, 1], [0, 3], [1, 2], [1, 3]]) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # n = 5, roads = [[0,1],[0,3],[1,2],[1,3],[2,3],[2,4]] -> 5
    assert fn(5, [[0, 1], [0, 3], [1, 2], [1, 3], [2, 3], [2, 4]]) == 5


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    # n = 8, roads = [[0,1],[1,2],[2,3],[2,4],[5,6],[5,7]] -> 5
    assert fn(8, [[0, 1], [1, 2], [2, 3], [2, 4], [5, 6], [5, 7]]) == 5


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_star_graph(fn):
    # Center node 0 connected to 1, 2, 3, 4
    # Pairs with center: rank = 4 + 1 - 1 = 4. Pairs without center: 1 + 1 = 2
    roads = [[0, 1], [0, 2], [0, 3], [0, 4]]
    assert fn(5, roads) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_complete_graph_k4(fn):
    # Complete graph K4: each degree is 3, any pair connected -> 3 + 3 - 1 = 5
    roads = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
    assert fn(4, roads) == 5


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_disconnected_triangles(fn):
    # Triangle 1: 0-1-2-0 (degrees 2, 2, 2)
    # Triangle 2: 3-4-5-3 (degrees 2, 2, 2)
    # Any pair between triangles: 2 + 2 = 4 (not connected)
    roads = [[0, 1], [1, 2], [2, 0], [3, 4], [4, 5], [5, 3]]
    assert fn(6, roads) == 4


# --- Hypothesis Property-Based Tests ---

@given(
    n=st.integers(min_value=2, max_value=15),
    data=st.data()
)
def test_solutions_consistency_random_graphs(n, data):
    cities = list(range(n))
    roads_tuples = data.draw(
        st.lists(
            st.tuples(st.sampled_from(cities), st.sampled_from(cities))
            .filter(lambda pair: pair[0] != pair[1])
            .map(lambda pair: (min(pair), max(pair))),
            unique=True,
            max_size=30
        )
    )
    roads = [[u, v] for u, v in roads_tuples]

    res_pairwise = solve_pairwise(n, roads)
    res_opt = solve_optimized(n, roads)

    assert res_pairwise == res_opt
