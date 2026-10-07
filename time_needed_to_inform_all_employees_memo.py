'''
Calculate the time needed to inform all employees via bottom-up path memoization.
Avoids constructing an adjacency list by tracing parent manager pointers directly.
'''

from typing import List


def num_of_minutes_memo(n: int, headID: int, manager: List[int], informTime: List[int]) -> int:
    """Calculate the maximum notification time using bottom-up memoization.

    Time Complexity: O(N) since each node's path to headID is computed at most once.
    Space Complexity: O(N) for the memoization array and temporary path stack.
    """
    if n <= 1:
        return 0

    # memo[i] stores the total time when employee i receives the news
    memo = [-1] * n
    memo[headID] = 0

    max_time = 0
    for i in range(n):
        curr = i
        path = []

        # Climb up the manager tree until reaching a resolved ancestor
        while memo[curr] == -1:
            path.append(curr)
            curr = manager[curr]

        # Propagate time downwards along the traversed path (path compression)
        accum_time = memo[curr]
        for node in reversed(path):
            accum_time += informTime[manager[node]]
            memo[node] = accum_time

        if memo[i] > max_time:
            max_time = memo[i]

    return max_time
