import pytest
from hypothesis import given, strategies as st
from collections import deque
from typing import List

from minimum_genetic_mutation import min_mutation as min_mutation_bidirectional
from minimum_genetic_mutation_bfs import min_mutation_bfs

SOLUTIONS = [
    min_mutation_bidirectional,
    min_mutation_bfs,
]


# --- Independent Reference Oracle ---

def oracle_min_mutation(start_gene: str, end_gene: str, bank: List[str]) -> int:
    if start_gene == end_gene:
        return 0
    bank_set = set(bank)
    if end_gene not in bank_set:
        return -1

    def diff_by_one(s1: str, s2: str) -> bool:
        return sum(c1 != c2 for c1, c2 in zip(s1, s2)) == 1

    queue = deque([(start_gene, 0)])
    visited = {start_gene}
    while queue:
        curr, dist = queue.popleft()
        if curr == end_gene:
            return dist
        for word in bank:
            if word not in visited and diff_by_one(curr, word):
                visited.add(word)
                queue.append((word, dist + 1))
    return -1


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    start = "AACCGGTT"
    end = "AACCGGTA"
    bank = ["AACCGGTA"]
    assert fn(start, end, bank) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    start = "AACCGGTT"
    end = "AAACGGTA"
    bank = ["AACCGGTA", "AACCGCTA", "AAACGGTA"]
    assert fn(start, end, bank) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    start = "AAAAACCC"
    end = "AACCCCCC"
    bank = ["AAAACCCC", "AAACCCCC", "AACCCCCC"]
    assert fn(start, end, bank) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_end_not_in_bank(fn):
    start = "AACCGGTT"
    end = "AACCGGTA"
    bank = ["AACCGGTC"]
    assert fn(start, end, bank) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_identical_start_and_end(fn):
    start = "AACCGGTT"
    end = "AACCGGTT"
    bank = ["AACCGGTT"]
    assert fn(start, end, bank) == 0


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_disconnected_path(fn):
    start = "AACCGGTT"
    end = "TTTTTTTT"
    bank = ["AACCGGTA", "AACCGGAA", "TTTTTTTT"]
    assert fn(start, end, bank) == -1


# --- Hypothesis Property-Based Tests ---

@st.composite
def gene_system_strategy(draw):
    chars = ["A", "C", "G", "T"]
    
    def random_gene():
        return "".join(draw(st.lists(st.sampled_from(chars), min_size=8, max_size=8)))

    start = random_gene()
    end = random_gene()
    bank_size = draw(st.integers(min_value=0, max_value=20))
    bank = [random_gene() for _ in range(bank_size)]
    if draw(st.booleans()) and bank_size > 0:
        bank[0] = end  # Ensure end is in bank in some cases

    return start, end, list(set(bank))


@given(data=gene_system_strategy())
def test_hypothesis_matches_oracle(data):
    start, end, bank = data
    expected = oracle_min_mutation(start, end, bank)
    for fn in SOLUTIONS:
        assert fn(start, end, bank) == expected
