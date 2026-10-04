import pytest
from hypothesis import given, strategies as st
from collections import deque
from typing import List

from jump_game_iii import can_reach as can_reach_bfs
from jump_game_iii_dfs import can_reach_dfs

SOLUTIONS = [
    can_reach_bfs,
    can_reach_dfs,
]


# --- Independent Reference Oracle ---

def oracle_can_reach(arr: List[int], start: int) -> bool:
    n = len(arr)
    if not (0 <= start < n):
        return False
    visited = set()
    stack = [start]
    while stack:
        curr = stack.pop()
        if arr[curr] == 0:
            return True
        if curr in visited:
            continue
        visited.add(curr)
        for nxt in (curr + arr[curr], curr - arr[curr]):
            if 0 <= nxt < n and nxt not in visited:
                stack.append(nxt)
    return False


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    arr = [4, 2, 3, 0, 3, 1, 2]
    start = 5
    assert fn(arr, start) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    arr = [4, 2, 3, 0, 3, 1, 2]
    start = 0
    assert fn(arr, start) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    arr = [3, 0, 2, 1, 2]
    start = 2
    assert fn(arr, start) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_element_zero(fn):
    assert fn([0], 0) is True


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_element_nonzero(fn):
    assert fn([5], 0) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_element_cycle_no_zero(fn):
    assert fn([1, 1], 0) is False


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_element_with_zero(fn):
    assert fn([1, 0], 0) is True


# --- Hypothesis Property-Based Tests ---

@st.composite
def jump_game_strategy(draw):
    size = draw(st.integers(min_value=1, max_value=30))
    arr = draw(st.lists(st.integers(min_value=0, max_value=25), min_size=size, max_size=size))
    start = draw(st.integers(min_value=0, max_value=size - 1))
    return arr, start


@given(data=jump_game_strategy())
def test_hypothesis_matches_oracle(data):
    arr, start = data
    expected = oracle_can_reach(arr, start)
    for fn in SOLUTIONS:
        assert fn(arr, start) is expected
