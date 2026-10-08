'''
Find all ancestors of each node in a DAG using Topological Sort (Kahn's Algorithm) and Set Propagation.
'''

from collections import deque
from typing import List


def get_ancestors_topo(n: int, edges: List[List[int]]) -> List[List[int]]:
    """Find ancestors via topological sorting and set union propagation.

    Time Complexity: O(V * E + V^2 log V) where V = n and E = len(edges).
    Space Complexity: O(V^2 + E) for ancestor sets and adjacency list.
    """
    adj = [[] for _ in range(n)]
    in_degree = [0] * n

    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    queue = deque([i for i in range(n) if in_degree[i] == 0])
    ancestor_sets = [set() for _ in range(n)]

    while queue:
        curr = queue.popleft()
        for child in adj[curr]:
            # child inherits all ancestors of curr, plus curr itself
            ancestor_sets[child].add(curr)
            ancestor_sets[child].update(ancestor_sets[curr])

            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.append(child)

    return [sorted(list(anc_set)) for anc_set in ancestor_sets]
