import pytest
from hypothesis import given, strategies as st
from collections import deque
from typing import List

from open_the_lock import open_lock as open_lock_bidirectional
from open_the_lock_bfs import open_lock_bfs

SOLUTIONS = [
    open_lock_bidirectional,
    open_lock_bfs,
]


# --- Independent Reference Oracle ---

def oracle_open_lock(deadends: List[str], target: str) -> int:
    dead_set = set(deadends)
    if '0000' in dead_set or target in dead_set:
        return -1
    if target == '0000':
        return 0

    queue = deque([('0000', 0)])
    visited = {'0000'}

    while queue:
        state, dist = queue.popleft()
        if state == target:
            return dist

        for i in range(4):
            d = int(state[i])
            for delta in (-1, 1):
                nxt_digit = (d + delta) % 10
                nxt_state = state[:i] + str(nxt_digit) + state[i + 1:]
                if nxt_state not in dead_set and nxt_state not in visited:
                    visited.add(nxt_state)
                    queue.append((nxt_state, dist + 1))

    return -1


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_target_is_start(fn):
    assert fn([], "0000") == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_start_in_deadends(fn):
    assert fn(["0000"], "8888") == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_target_in_deadends(fn):
    assert fn(["8888"], "8888") == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    deadends = ["0201", "0101", "0102", "1212", "2002"]
    target = "0202"
    assert fn(deadends, target) == 6


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    deadends = ["8888"]
    target = "0009"
    assert fn(deadends, target) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    deadends = ["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"]
    target = "8888"
    assert fn(deadends, target) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_turn_backward(fn):
    # '0000' -> '0009' takes 1 turn (0 -> 9)
    assert fn([], "0009") == 1
    # '0000' -> '9999' takes 4 turns (all 4 wheels backward by 1)
    assert fn([], "9999") == 4


# --- Hypothesis Property-Based Tests ---

@st.composite
def lock_strategy(draw):
    def random_code():
        return "".join(str(draw(st.integers(min_value=0, max_value=9))) for _ in range(4))

    target = random_code()
    num_deadends = draw(st.integers(min_value=0, max_value=15))
    deadends = [random_code() for _ in range(num_deadends)]
    return deadends, target


@given(data=lock_strategy())
def test_hypothesis_matches_oracle(data):
    deadends, target = data
    expected = oracle_open_lock(deadends, target)
    for fn in SOLUTIONS:
        assert fn(deadends, target) == expected
