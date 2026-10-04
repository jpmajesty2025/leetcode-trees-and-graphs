'''
You are given a string initialCurrency, and you start with 1.0 of initialCurrency.

This module implements the multi-source Day 2 BFS approach.
'''

from collections import defaultdict, deque


def max_amount_multisource(
    initial_currency: str,
    pairs1: list[list[str]],
    rates1: list[float],
    pairs2: list[list[str]],
    rates2: list[float],
) -> float:
    """Find max amount by seeding Day 2 BFS with Day 1 balances."""
    # Day 1 Graph
    graph1: defaultdict[str, dict[str, float]] = defaultdict(dict)
    for (u, v), rate in zip(pairs1, rates1):
        graph1[u][v] = rate
        graph1[v][u] = 1.0 / rate

    day1_balances = {initial_currency: 1.0}
    q1 = deque([(initial_currency, 1.0)])
    while q1:
        curr, bal = q1.popleft()
        for nbr, r in graph1[curr].items():
            new_bal = bal * r
            if nbr not in day1_balances or new_bal > day1_balances[nbr]:
                day1_balances[nbr] = new_bal
                q1.append((nbr, new_bal))

    # Day 2 Graph
    graph2: defaultdict[str, dict[str, float]] = defaultdict(dict)
    for (u, v), rate in zip(pairs2, rates2):
        graph2[u][v] = rate
        graph2[v][u] = 1.0 / rate

    # Seed Day 2 with all Day 1 balances
    day2_balances = dict(day1_balances)
    q2 = deque(day1_balances.items())
    while q2:
        curr, bal = q2.popleft()
        for nbr, r in graph2[curr].items():
            new_bal = bal * r
            if nbr not in day2_balances or new_bal > day2_balances[nbr]:
                day2_balances[nbr] = new_bal
                q2.append((nbr, new_bal))

    return day2_balances.get(initial_currency, 1.0)


# Aliases
max_amount = max_amount_multisource
maxAmount = max_amount_multisource
