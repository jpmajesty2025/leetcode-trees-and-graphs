'''
In a town, there are n people labeled from 1 to n. Return the label of the town judge if they exist, or -1 otherwise.

Two-Array Approach: Explicit in-degree and out-degree counting.
'''

from typing import List


def find_judge_two_arrays(n: int, trust: List[List[int]]) -> int:
    """Find the town judge by tracking in-degree and out-degree separately.

    Time Complexity: O(E + N) where E is the number of trust pairs and N is the population.
    Space Complexity: O(N) auxiliary space for in_degree and out_degree arrays.
    """
    if len(trust) < n - 1:
        return -1

    in_degree = [0] * (n + 1)
    out_degree = [0] * (n + 1)

    for person, trusted in trust:
        out_degree[person] += 1
        in_degree[trusted] += 1

    for i in range(1, n + 1):
        if in_degree[i] == n - 1 and out_degree[i] == 0:
            return i

    return -1
