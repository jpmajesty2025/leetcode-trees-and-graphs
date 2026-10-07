import pytest
from hypothesis import given, strategies as st
from typing import List

from time_needed_to_inform_all_employees import num_of_minutes as solve_bfs
from time_needed_to_inform_all_employees_memo import num_of_minutes_memo as solve_memo

SOLUTIONS = [
    solve_bfs,
    solve_memo,
]


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_employee(fn):
    assert fn(1, 0, [-1], [0]) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_star_hierarchy_leetcode_ex2(fn):
    n = 6
    headID = 2
    manager = [2, 2, -1, 2, 2, 2]
    informTime = [0, 0, 1, 0, 0, 0]
    assert fn(n, headID, manager, informTime) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_linear_chain(fn):
    # Chain: 0 -> 1 -> 2 -> 3
    n = 4
    headID = 0
    manager = [-1, 0, 1, 2]
    informTime = [2, 3, 4, 0]
    assert fn(n, headID, manager, informTime) == 9


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_balanced_hierarchy_with_different_branch_times(fn):
    # Head: 0 (informTime = 10)
    # Left child: 1 (informTime = 5), right child: 2 (informTime = 20)
    # Subordinates of 1: 3 (informTime = 0)
    # Subordinates of 2: 4 (informTime = 0)
    # Branch 1: 10 + 5 = 15. Branch 2: 10 + 20 = 30.
    n = 5
    headID = 0
    manager = [-1, 0, 0, 1, 2]
    informTime = [10, 5, 20, 0, 0]
    assert fn(n, headID, manager, informTime) == 30


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_zero_inform_times(fn):
    n = 3
    headID = 1
    manager = [1, -1, 1]
    informTime = [0, 0, 0]
    assert fn(n, headID, manager, informTime) == 0


# --- Hypothesis Property-Based Tests ---

@given(
    n=st.integers(min_value=2, max_value=30),
    data=st.data()
)
def test_tree_solutions_equivalence(n, data):
    # Generate a valid tree rooted at a random headID
    nodes = list(range(n))
    # Create random tree hierarchy by incrementally attaching nodes
    headID = data.draw(st.integers(min_value=0, max_value=n - 1))
    manager = [0] * n
    manager[headID] = -1

    available_managers = [headID]
    unattached = [i for i in range(n) if i != headID]

    while unattached:
        node = unattached.pop()
        parent = data.draw(st.sampled_from(available_managers))
        manager[node] = parent
        available_managers.append(node)

    # Generate inform times (leaves can have 0, internal nodes can have non-zero)
    informTime = [data.draw(st.integers(min_value=0, max_value=50)) for _ in range(n)]

    res_bfs = solve_bfs(n, headID, manager, informTime)
    res_memo = solve_memo(n, headID, manager, informTime)

    assert res_bfs == res_memo
    assert res_bfs >= 0
