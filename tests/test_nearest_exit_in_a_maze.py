import pytest
from hypothesis import given, strategies as st
from collections import deque
import copy

from nearest_exit_in_a_maze import nearest_exit as nearest_exit_inplace
from nearest_exit_in_a_maze_non_mutating import nearest_exit_non_mutating
from nearest_exit_in_a_maze_bidirectional import nearest_exit_bidirectional

SOLUTIONS = [
    nearest_exit_inplace,
    nearest_exit_non_mutating,
    nearest_exit_bidirectional,
]


# --- Independent Reference Oracle ---

def oracle_nearest_exit(maze: list[list[str]], entrance: list[int]) -> int:
    rows, cols = len(maze), len(maze[0])
    start = (entrance[0], entrance[1])
    queue = deque([(start[0], start[1], 0)])
    visited = {start}

    while queue:
        r, c, steps = queue.popleft()
        if (r, c) != start and (r == 0 or r == rows - 1 or c == 0 or c == cols - 1):
            return steps

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == '.' and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, steps + 1))

    return -1


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # maze = [["+","+",".","+"],[".",".",".","+"],["+","+","+","."]], entrance = [1,2] -> 1
    maze = [
        ["+", "+", ".", "+"],
        [".", ".", ".", "+"],
        ["+", "+", "+", "."]
    ]
    assert fn(copy.deepcopy(maze), [1, 2]) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # maze = [["+","+","+"],[".",".","."],["+","+","+"]], entrance = [1,0] -> 2
    maze = [
        ["+", "+", "+"],
        [".", ".", "."],
        ["+", "+", "+"]
    ]
    assert fn(copy.deepcopy(maze), [1, 0]) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    # maze = [[".","+"]], entrance = [0,0] -> -1
    maze = [[".", "+"]]
    assert fn(copy.deepcopy(maze), [0, 0]) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_entrance_on_border_with_nearby_exit(fn):
    # maze with entrance on top border, and exit on left border
    maze = [
        ["+", ".", "+"],
        [".", ".", "+"],
        ["+", "+", "+"]
    ]
    # entrance is [0, 1], exit is [1, 0] at distance 2
    assert fn(copy.deepcopy(maze), [0, 1]) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_enclosed_entrance(fn):
    maze = [
        ["+", "+", "+"],
        ["+", ".", "+"],
        ["+", "+", "+"]
    ]
    assert fn(copy.deepcopy(maze), [1, 1]) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_exit_far_away(fn):
    maze = [
        ["+", "+", "+", "+", "+"],
        [".", ".", ".", ".", "+"],
        ["+", "+", "+", ".", "+"],
        ["+", "+", "+", ".", "+"],
        ["+", "+", "+", ".", "+"]
    ]
    # Entrance [1, 0], only exit at [4, 3] -> distance 6
    assert fn(copy.deepcopy(maze), [1, 0]) == 6


# --- Hypothesis Property-Based Tests ---

@st.composite
def maze_strategy(draw):
    rows = draw(st.integers(min_value=1, max_value=8))
    cols = draw(st.integers(min_value=1, max_value=8))
    # Fill grid randomly
    maze = [
        [draw(st.sampled_from(['.', '+'])) for _ in range(cols)]
        for _ in range(rows)
    ]
    # Pick entrance
    ent_r = draw(st.integers(min_value=0, max_value=rows - 1))
    ent_c = draw(st.integers(min_value=0, max_value=cols - 1))
    maze[ent_r][ent_c] = '.'
    return maze, [ent_r, ent_c]


@given(data=maze_strategy())
def test_hypothesis_matches_oracle(data):
    maze, entrance = data
    expected = oracle_nearest_exit(maze, entrance)
    for fn in SOLUTIONS:
        assert fn(copy.deepcopy(maze), entrance) == expected
