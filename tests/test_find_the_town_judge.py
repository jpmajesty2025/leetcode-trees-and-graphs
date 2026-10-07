import pytest
from hypothesis import given, strategies as st
from typing import List

from find_the_town_judge import find_judge as find_judge_net_score
from find_the_town_judge_two_arrays import find_judge_two_arrays

SOLUTIONS = [
    find_judge_net_score,
    find_judge_two_arrays,
]


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_single_person_no_trust(fn):
    assert fn(1, []) == 1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_people_one_judge(fn):
    assert fn(2, [[1, 2]]) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_people_no_trust(fn):
    assert fn(2, []) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_two_people_mutual_trust(fn):
    assert fn(2, [[1, 2], [2, 1]]) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    assert fn(2, [[1, 2]]) == 2


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    assert fn(3, [[1, 3], [2, 3]]) == 3


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    # Judge trusts someone -> invalid
    assert fn(3, [[1, 3], [2, 3], [3, 1]]) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_four_people_missing_one_trust(fn):
    # 4 people, but person 1 does not trust 4 -> in_degree of 4 is only 2 (needs 3)
    assert fn(4, [[2, 4], [3, 4]]) == -1


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_star_graph_valid_judge(fn):
    # 5 people, everyone 1..4 trusts 5, 5 trusts nobody
    trust = [[1, 5], [2, 5], [3, 5], [4, 5]]
    assert fn(5, trust) == 5


# --- Hypothesis Property-Based Tests ---

@given(
    n=st.integers(min_value=2, max_value=20),
    data=st.data()
)
def test_planted_judge_property(n, data):
    # Plant a judge J in 1..n
    judge = data.draw(st.integers(min_value=1, max_value=n))

    # All other people trust the judge
    trust_pairs = [[i, judge] for i in range(1, n + 1) if i != judge]

    # Optionally add additional trust relationships among non-judges
    non_judges = [i for i in range(1, n + 1) if i != judge]
    extra_pairs = data.draw(
        st.lists(
            st.tuples(st.sampled_from(non_judges), st.sampled_from(non_judges)).filter(lambda pair: pair[0] != pair[1]),
            unique=True,
            max_size=15
        )
    )
    for u, v in extra_pairs:
        if [u, v] not in trust_pairs:
            trust_pairs.append([u, v])

    for fn in SOLUTIONS:
        assert fn(n, trust_pairs) == judge


@given(
    n=st.integers(min_value=1, max_value=15),
    data=st.data()
)
def test_solutions_consistency_random_graphs(n, data):
    # Generate arbitrary valid trust pairs
    people = list(range(1, n + 1))
    if n > 1:
        trust_pairs = data.draw(
            st.lists(
                st.tuples(st.sampled_from(people), st.sampled_from(people)).filter(lambda pair: pair[0] != pair[1]),
                unique=True,
                max_size=30
            )
        )
        trust = [[u, v] for u, v in trust_pairs]
    else:
        trust = []

    res1 = find_judge_net_score(n, trust)
    res2 = find_judge_two_arrays(n, trust)
    assert res1 == res2
