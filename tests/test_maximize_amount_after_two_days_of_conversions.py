import pytest
from hypothesis import given, strategies as st
from collections import defaultdict, deque
from typing import List

from maximize_amount_after_two_days_of_conversions import max_amount as max_amount_frontier
from maximize_amount_after_two_days_of_conversions_multisource import max_amount_multisource

SOLUTIONS = [
    max_amount_frontier,
    max_amount_multisource,
]


# --- Independent Reference Oracle ---

def oracle_max_amount(
    initial_currency: str,
    pairs1: List[List[str]],
    rates1: List[float],
    pairs2: List[List[str]],
    rates2: List[float],
) -> float:
    def solve_day(start: str, init_val: float, pairs: List[List[str]], rates: List[float]) -> dict[str, float]:
        adj = defaultdict(dict)
        for (u, v), r in zip(pairs, rates):
            adj[u][v] = r
            adj[v][u] = 1.0 / r
        best = {start: init_val}
        q = deque([(start, init_val)])
        while q:
            curr, val = q.popleft()
            for nxt, r in adj[curr].items():
                if nxt not in best or val * r > best[nxt]:
                    best[nxt] = val * r
                    q.append((nxt, val * r))
        return best

    day1 = solve_day(initial_currency, 1.0, pairs1, rates1)
    ans = 1.0
    for cur, val in day1.items():
        day2 = solve_day(cur, val, pairs2, rates2)
        if initial_currency in day2:
            ans = max(ans, day2[initial_currency])
    return ans


# --- Deterministic Pytest Tests ---

@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_1(fn):
    # initialCurrency = "EUR", pairs1 = [["EUR","USD"]], rates1 = [2.0], pairs2 = [["USD","JPY"],["JPY","EUR"]], rates2 = [5.0,0.2]
    # Day 1: EUR -> USD (2.0)
    # Day 2: USD -> JPY (5.0) -> EUR (0.2) = 1.0 * 2.0 * 5.0 * 0.2 = 2.0
    initialCurrency = "EUR"
    pairs1 = [["EUR", "USD"]]
    rates1 = [2.0]
    pairs2 = [["USD", "JPY"], ["JPY", "EUR"]]
    rates2 = [5.0, 0.2]
    expected = 2.0
    assert fn(initialCurrency, pairs1, rates1, pairs2, rates2) == pytest.approx(expected)


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_2(fn):
    # initialCurrency = "NGN", pairs1 = [["NGN","EUR"]], rates1 = [9.0], pairs2 = [["NGN","EUR"]], rates2 = [6.0]
    # Day 1: NGN -> EUR (9.0)
    # Day 2: EUR -> NGN (1 / 6.0) => 9.0 / 6.0 = 1.5
    initialCurrency = "NGN"
    pairs1 = [["NGN", "EUR"]]
    rates1 = [9.0]
    pairs2 = [["NGN", "EUR"]]
    rates2 = [6.0]
    expected = 1.5
    assert fn(initialCurrency, pairs1, rates1, pairs2, rates2) == pytest.approx(expected)


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_leetcode_example_3(fn):
    # initialCurrency = "USD", pairs1 = [["USD","EUR"]], rates1 = [1.0], pairs2 = [["EUR","JPY"]], rates2 = [10.0]
    # Cannot convert back to USD on Day 2 -> best is 1.0 (no conversion)
    initialCurrency = "USD"
    pairs1 = [["USD", "EUR"]]
    rates1 = [1.0]
    pairs2 = [["EUR", "JPY"]]
    rates2 = [10.0]
    expected = 1.0
    assert fn(initialCurrency, pairs1, rates1, pairs2, rates2) == pytest.approx(expected)


@pytest.mark.parametrize("fn", SOLUTIONS)
def test_empty_or_zero_conversions(fn):
    # No conversions better than holding 1.0
    initialCurrency = "USD"
    pairs1 = [["USD", "EUR"]]
    rates1 = [0.5]
    pairs2 = [["USD", "EUR"]]
    rates2 = [2.0]
    # Day 1 EUR: 0.5, Day 2 EUR->USD: 1/2 = 0.5 -> final = 0.25 < 1.0
    expected = 1.0
    assert fn(initialCurrency, pairs1, rates1, pairs2, rates2) == pytest.approx(expected)


# --- Hypothesis Property-Based Tests ---

@st.composite
def currency_system_strategy(draw):
    currencies = ["USD", "EUR", "JPY", "GBP", "CAD", "AUD"]
    initial = draw(st.sampled_from(currencies))

    def make_day_system():
        num_pairs = draw(st.integers(min_value=0, max_value=4))
        # build consistent rates
        vals = {c: draw(st.floats(min_value=0.5, max_value=20.0)) for c in currencies}
        pairs = []
        rates = []
        for _ in range(num_pairs):
            u = draw(st.sampled_from(currencies))
            v = draw(st.sampled_from([c for c in currencies if c != u]))
            pairs.append([u, v])
            rates.append(vals[u] / vals[v])
        return pairs, rates

    p1, r1 = make_day_system()
    p2, r2 = make_day_system()
    return initial, p1, r1, p2, r2


@given(data=currency_system_strategy())
def test_hypothesis_matches_oracle(data):
    initial, p1, r1, p2, r2 = data
    expected = oracle_max_amount(initial, p1, r1, p2, r2)
    for fn in SOLUTIONS:
        res = fn(initial, p1, r1, p2, r2)
        assert res == pytest.approx(expected, rel=1e-4, abs=1e-4)
