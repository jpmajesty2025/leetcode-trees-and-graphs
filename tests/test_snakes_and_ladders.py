import pytest
from hypothesis import given, strategies as st
from collections import deque
from typing import List

from snakes_and_ladders import snakes_and_ladders as snakes_1d
from snakes_and_ladders_2d import snakes_and_ladders_2d

SOLUTIONS = [
    snakes_1d,
    snakes_and_ladders_2d,
]


# --- Independent Reference Oracle ---

def oracle_snakes_and_ladders(board: List[List[int]]) -> int:
    n = len(board)
    target = n * n

    def get_pos(s: int) -> tuple[int, int]:
        r, c = divmod(s - 1, n)
        row = n - 1 - r
        col = c if (r % 2 == 0) else (n - 1 - c)
        return row, col

    visited = {1}
    queue = deque([(1, 0)])

    while queue:
        curr, rolls = queue.popleft()
        if curr == target:
            return rolls

        for roll in range(1, 7):
            nxt = curr + roll
            if nxt > target:
                break
            r, c = get_pos(nxt)
            dest = board[r][c] if board[r][c] != -1 else nxt
            if dest not in visited:
                visited.add(dest)
                queue.append((dest, rolls + 1))

    return -1


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # Standard LeetCode 6x6 board -> 4 rolls
    board = [
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, 35, -1, -1, 13, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, 15, -1, -1, -1, -1]
    ]
    assert fn(board) == 4


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # 2x2 board: [[-1, -1], [-1, 3]] -> 1 roll (from 1, roll 1 lands on 2 which takes ladder to 3)
    board = [
        [-1, -1],
        [-1, 3]
    ]
    assert fn(board) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_direct_roll_to_end(fn):
    # 2x2 board without snakes/ladders: [[-1, -1], [-1, -1]] -> 1 roll to reach 4 (rolls 1 to 4)
    board = [
        [-1, -1],
        [-1, -1]
    ]
    assert fn(board) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_unreachable_board(fn):
    # 3x3 board where cells 2..7 all have snakes leading back to 1
    # Squares 1..3: board[2] = [-1, 1, 1]
    # Squares 4..6: board[1] = [1, 1, 1]
    # Squares 7..9: board[0] = [1, -1, -1]
    board = [
        [1, -1, -1],
        [1, 1, 1],
        [-1, 1, 1]
    ]
    assert fn(board) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_snake_cycle_avoidance(fn):
    # Cycle between 2 -> 5 and 5 -> 2
    board = [
        [-1, -1, -1],
        [-1, -1, -1],
        [-1, 5, -1]  # square 2 jumps to 5
    ]
    board[1][1] = 2  # square 5 jumps to 2
    # Should not infinite loop and reach 9
    assert fn(board) >= 1


# --- Hypothesis Property-Based Tests ---

@st.composite
def random_board_strategy(draw):
    n = draw(st.integers(min_value=2, max_value=6))
    target = n * n
    # Start with empty board
    board = [[-1] * n for _ in range(n)]

    def set_board_val(sq: int, val: int):
        r, c = divmod(sq - 1, n)
        row = n - 1 - r
        col = c if (r % 2 == 0) else (n - 1 - c)
        board[row][col] = val

    # Add random snakes and ladders on squares 2 to target-1
    for sq in range(2, target):
        if draw(st.booleans()):
            dest = draw(st.integers(min_value=1, max_value=target))
            if dest != sq:
                set_board_val(sq, dest)

    return board


@given(board=random_board_strategy())
def test_hypothesis_matches_oracle(board):
    expected = oracle_snakes_and_ladders(board)
    for fn in SOLUTIONS:
        assert fn(board) == expected
