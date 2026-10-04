import pytest
from hypothesis import given, strategies as st
from collections import deque
from typing import List

from detonate_maximum_bombs import maximum_detonation as max_detonation_bfs
from detonate_maximum_bombs_bitmask import maximum_detonation_bitmask as max_detonation_bitmask

SOLUTIONS = [
    max_detonation_bfs,
    max_detonation_bitmask,
]


# --- Independent Reference Oracle ---

def oracle_maximum_detonation(bombs: List[List[int]]) -> int:
    n = len(bombs)
    if n <= 1:
        return n
    
    # Simple direct DFS
    adj = [[] for _ in range(n)]
    for i in range(n):
        x1, y1, r1 = bombs[i]
        for j in range(n):
            if i != j:
                x2, y2, _ = bombs[j]
                if (x1 - x2) ** 2 + (y1 - y2) ** 2 <= r1 ** 2:
                    adj[i].append(j)

    ans = 0
    for i in range(n):
        visited = set()
        stack = [i]
        visited.add(i)
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    stack.append(v)
        ans = max(ans, len(visited))
    return ans


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    bombs = [[2, 1, 3], [6, 1, 4]]
    assert fn(bombs) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    bombs = [[1, 1, 5], [10, 10, 5]]
    assert fn(bombs) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    bombs = [[1, 2, 3], [2, 3, 1], [3, 4, 2], [4, 5, 3], [5, 6, 4]]
    assert fn(bombs) == 5


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_bomb(fn):
    assert fn([[0, 0, 10]]) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_asymmetric_detonation(fn):
    # Bomb 0 covers Bomb 1, but Bomb 1 does not cover Bomb 0
    bombs = [[0, 0, 10], [0, 5, 1]]
    assert fn(bombs) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_disconnected_clusters(fn):
    # Two disjoint pairs
    bombs = [
        [0, 0, 1], [0, 1, 1],       # Cluster A (size 2)
        [100, 100, 1], [100, 101, 1] # Cluster B (size 2)
    ]
    assert fn(bombs) == 2


# --- Hypothesis Property-Based Tests ---

@st.composite
def bomb_strategy(draw):
    size = draw(st.integers(min_value=1, max_value=12))
    bombs = []
    for _ in range(size):
        x = draw(st.integers(min_value=-50, max_value=50))
        y = draw(st.integers(min_value=-50, max_value=50))
        r = draw(st.integers(min_value=1, max_value=60))
        bombs.append([x, y, r])
    return bombs


@given(bombs=bomb_strategy())
def test_hypothesis_matches_oracle(bombs):
    expected = oracle_maximum_detonation(bombs)
    for fn in SOLUTIONS:
        assert fn(bombs) == expected
