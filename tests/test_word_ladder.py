import pytest
from hypothesis import given, strategies as st
from collections import deque
from typing import List

from word_ladder import ladder_length as ladder_length_bidirectional
from word_ladder_bfs import ladder_length_bfs

SOLUTIONS = [
    ladder_length_bidirectional,
    ladder_length_bfs,
]


# --- Independent Reference Oracle ---

def oracle_ladder_length(begin_word: str, end_word: str, word_list: List[str]) -> int:
    word_set = set(word_list)
    if end_word not in word_set:
        return 0

    def diff_by_one(w1: str, w2: str) -> bool:
        return sum(c1 != c2 for c1, c2 in zip(w1, w2)) == 1

    queue = deque([(begin_word, 1)])
    visited = {begin_word}
    while queue:
        curr, steps = queue.popleft()
        if curr == end_word:
            return steps
        for w in word_list:
            if w not in visited and diff_by_one(curr, w):
                visited.add(w)
                queue.append((w, steps + 1))
    return 0


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    begin = "hit"
    end = "cog"
    word_list = ["hot", "dot", "dog", "lot", "log", "cog"]
    assert fn(begin, end, word_list) == 5


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    begin = "hit"
    end = "cog"
    word_list = ["hot", "dot", "dog", "lot", "log"]
    assert fn(begin, end, word_list) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_step(fn):
    begin = "hot"
    end = "dot"
    word_list = ["dot"]
    assert fn(begin, end, word_list) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_begin_in_word_list(fn):
    begin = "hot"
    end = "dog"
    word_list = ["hot", "dot", "dog"]
    assert fn(begin, end, word_list) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_unreachable_word(fn):
    begin = "cat"
    end = "dog"
    word_list = ["cot", "dot", "cog", "log"]  # dog not in wordList
    assert fn(begin, end, word_list) == 0


# --- Hypothesis Property-Based Tests ---

@st.composite
def word_ladder_strategy(draw):
    chars = ["a", "b", "c", "d", "e"]
    word_len = 3

    def make_word():
        return "".join(draw(st.lists(st.sampled_from(chars), min_size=word_len, max_size=word_len)))

    begin = make_word()
    end = make_word()
    size = draw(st.integers(min_value=0, max_value=15))
    words = [make_word() for _ in range(size)]
    if draw(st.booleans()) and size > 0:
        words[0] = end

    return begin, end, list(set(words))


@given(data=word_ladder_strategy())
def test_hypothesis_matches_oracle(data):
    begin, end, words = data
    expected = oracle_ladder_length(begin, end, words)
    for fn in SOLUTIONS:
        assert fn(begin, end, words) == expected
