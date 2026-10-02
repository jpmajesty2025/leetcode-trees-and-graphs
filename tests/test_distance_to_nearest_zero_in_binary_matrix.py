import pytest
from hypothesis import given, strategies as st
from collections import deque
from typing import List

from distance_to_nearest_zero_in_binary_matrix import update_matrix as update_matrix_bfs
from distance_to_nearest_zero_in_binary_matrix_dp import update_matrix_dp

SOLUTIONS = [
    update_matrix_bfs,
    update_matrix_dp,
]


# --- Independent Reference Oracle (Naive Multi-Source BFS) ---

def oracle_update_matrix(mat: List[List[int]]) -> List[List[int]]:
    if not mat or not mat[0]:
        return []
    m, n = len(mat), len(mat[0])
    res = [[0 if mat[r][c] == 0 else -1 for c in range(n)] for r in range(m)]
    queue = deque([(r, c) for r in range(m) for c in range(n) if mat[r][c] == 0])

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and res[nr][nc] == -1:
                res[nr][nc] = res[r][c] + 1
                queue.append((nr, nc))
    return res


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_matrix(fn):
    assert fn([]) == []
    assert fn([[]]) == []


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_zero(fn):
    assert fn([[0]]) == [[0]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_all_zeros(fn):
    mat = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    expected = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    assert fn(mat) == expected


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    mat = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    expected = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    assert fn(mat) == expected


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    mat = [
        [0, 0, 0],
        [0, 1, 0],
        [1, 1, 1]
    ]
    expected = [
        [0, 0, 0],
        [0, 1, 0],
        [1, 2, 1]
    ]
    assert fn(mat) == expected


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_corner_zero(fn):
    # Only top-left is 0
    mat = [
        [0, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    expected = [
        [0, 1, 2],
        [1, 2, 3],
        [2, 3, 4]
    ]
    assert fn(mat) == expected


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_bottom_right_zero(fn):
    # Only bottom-right is 0
    mat = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 0]
    ]
    expected = [
        [4, 3, 2],
        [3, 2, 1],
        [2, 1, 0]
    ]
    assert fn(mat) == expected


# --- Hypothesis Property-Based Tests ---

@st.composite
def binary_matrix_strategy(draw):
    m = draw(st.integers(min_value=1, max_value=10))
    n = draw(st.integers(min_value=1, max_value=10))
    # Matrix of 1s
    mat = [[1] * n for _ in range(m)]
    # Place at least one zero
    zero_r = draw(st.integers(min_value=0, max_value=m - 1))
    zero_c = draw(st.integers(min_value=0, max_value=n - 1))
    mat[zero_r][zero_c] = 0
    # Randomly fill other cells
    for r in range(m):
        for c in range(n):
            if (r, c) != (zero_r, zero_c):
                mat[r][c] = draw(st.integers(min_value=0, max_value=1))
    return mat


@given(mat=binary_matrix_strategy())
def test_hypothesis_matches_oracle(mat):
    expected = oracle_update_matrix(mat)
    for fn in SOLUTIONS:
        assert fn(mat) == expected
