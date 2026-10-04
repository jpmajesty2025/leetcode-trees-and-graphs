'''
You are given a string initialCurrency, and you start with 1.0 of initialCurrency.

You are also given four arrays with currency pairs (strings) and rates (real numbers):
pairs1, rates1 for Day 1
pairs2, rates2 for Day 2

Return the maximum amount of initialCurrency you can have after performing any number of 
conversions on both days in order.
'''

from collections import defaultdict, deque


def max_amount(
    initial_currency: str,
    pairs1: list[list[str]],
    rates1: list[float],
    pairs2: list[list[str]],
    rates2: list[float],
) -> float:
    """Find max amount of initialCurrency after 2 days of conversions using 2-stage BFS."""

    def get_rates_from_source(
        start_currency: str, pairs: list[list[str]], rates: list[float]
    ) -> dict[str, float]:
        graph = defaultdict(dict)
        for (u, v), rate in zip(pairs, rates):
            graph[u][v] = rate
            graph[v][u] = 1.0 / rate

        max_rates = {start_currency: 1.0}
        queue = deque([(start_currency, 1.0)])

        while queue:
            curr, amount = queue.popleft()
            for nbr, rate in graph[curr].items():
                new_amount = amount * rate
                if nbr not in max_rates or new_amount > max_rates[nbr]:
                    max_rates[nbr] = new_amount
                    queue.append((nbr, new_amount))

        return max_rates

    # Day 1: Max conversion rate from initial_currency to every reachable currency
    day1_rates = get_rates_from_source(initial_currency, pairs1, rates1)

    # Day 2: Rates from initial_currency to every reachable currency on Day 2
    day2_rates = get_rates_from_source(initial_currency, pairs2, rates2)

    # Maximize: Day 1 hold * Day 2 return rate (1 / day2_rates[currency])
    best = 1.0
    for currency, day1_amount in day1_rates.items():
        if currency in day2_rates:
            final_amount = day1_amount / day2_rates[currency]
            if final_amount > best:
                best = final_amount

    return best


# LeetCode backward compatibility aliases
maxAmount = max_amount
