import pytest
import copy
from hypothesis import given, strategies as st
from collections import deque
from typing import List

from flood_fill import flood_fill as flood_fill_dfs
from flood_fill_bfs import flood_fill_bfs
from flood_fill_iterative_dfs import flood_fill_iterative_dfs

SOLUTIONS = [
    flood_fill_dfs,
    flood_fill_bfs,
    flood_fill_iterative_dfs,
]


# --- Independent Reference Oracle ---

def oracle_flood_fill(image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
    """Independent BFS-based oracle operating on a copy."""
    img = copy.deepcopy(image)
    orig = img[sr][sc]
    if orig == color:
        return img
    rows, cols = len(img), len(img[0])
    img[sr][sc] = color
    q = deque([(sr, sc)])
    while q:
        r, c = q.popleft()
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and img[nr][nc] == orig:
                img[nr][nc] = color
                q.append((nr, nc))
    return img


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_same_color_no_op(fn):
    image = [[1, 1], [1, 1]]
    result = fn(copy.deepcopy(image), 0, 0, 1)
    assert result == [[1, 1], [1, 1]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_pixel(fn):
    assert fn([[0]], 0, 0, 2) == [[2]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    image = [
        [1, 1, 1],
        [1, 1, 0],
        [1, 0, 1]
    ]
    expected = [
        [2, 2, 2],
        [2, 2, 0],
        [2, 0, 1]
    ]
    assert fn(copy.deepcopy(image), 1, 1, 2) == expected


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    image = [[0, 0, 0], [0, 0, 0]]
    assert fn(copy.deepcopy(image), 0, 0, 0) == [[0, 0, 0], [0, 0, 0]]


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_diagonals_are_not_connected(fn):
    image = [
        [1, 0],
        [0, 1]
    ]
    expected = [
        [2, 0],
        [0, 1]
    ]
    assert fn(copy.deepcopy(image), 0, 0, 2) == expected


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_donut_boundary_island(fn):
    image = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
    expected = [
        [3, 3, 3],
        [3, 0, 3],
        [3, 3, 3]
    ]
    assert fn(copy.deepcopy(image), 0, 0, 3) == expected


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_deep_serpentine_fill(fn):
    image = [
        [1, 1, 1, 1],
        [0, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 1, 1, 1]
    ]
    expected = [
        [2, 2, 2, 2],
        [0, 0, 0, 2],
        [2, 2, 2, 2],
        [2, 0, 0, 0],
        [2, 2, 2, 2]
    ]
    assert fn(copy.deepcopy(image), 0, 0, 2) == expected


# --- Hypothesis Property-Based Tests ---

@st.composite
def image_with_start_and_color(draw, min_dim=1, max_dim=12):
    rows = draw(st.integers(min_value=min_dim, max_value=max_dim))
    cols = draw(st.integers(min_value=min_dim, max_value=max_dim))
    image = draw(
        st.lists(
            st.lists(st.integers(min_value=0, max_value=4), min_size=cols, max_size=cols),
            min_size=rows,
            max_size=rows
        )
    )
    sr = draw(st.integers(min_value=0, max_value=rows - 1))
    sc = draw(st.integers(min_value=0, max_value=cols - 1))
    new_color = draw(st.integers(min_value=0, max_value=4))
    return image, sr, sc, new_color


@given(data=image_with_start_and_color())
def test_hypothesis_matches_oracle(data):
    image, sr, sc, new_color = data
    expected = oracle_flood_fill(image, sr, sc, new_color)
    for fn in SOLUTIONS:
        result = fn(copy.deepcopy(image), sr, sc, new_color)
        assert result == expected


@given(data=image_with_start_and_color())
def test_hypothesis_starting_pixel_has_new_color(data):
    image, sr, sc, new_color = data
    for fn in SOLUTIONS:
        res = fn(copy.deepcopy(image), sr, sc, new_color)
        assert res[sr][sc] == new_color
