'''
Calculate the maximal network rank of an infrastructure.

Optimized approach: Candidate degree clustering and Pigeonhole Principle edge pruning.
Avoids evaluating all O(V^2) pairs by only inspecting the top-degree vertices.
'''

from typing import List


def maximal_network_rank_optimized(n: int, roads: List[List[int]]) -> int:
    """Calculate maximal network rank in O(V + E) time via degree candidate clustering.

    Time Complexity: O(V + E) average/best time, avoiding O(V^2) pairwise iteration.
    Space Complexity: O(V + E) for adjacency sets and degree tracking.
    """
    if n < 2:
        return 0

    degree = [0] * n
    adj_sets = [set() for _ in range(n)]

    for u, v in roads:
        degree[u] += 1
        degree[v] += 1
        adj_sets[u].add(v)
        adj_sets[v].add(u)

    unique_degrees = sorted(list(set(degree)), reverse=True)
    if not unique_degrees:
        return 0

    max1 = unique_degrees[0]
    max1_nodes = [i for i in range(n) if degree[i] == max1]

    if len(max1_nodes) > 1:
        # If there are 2 or more vertices with the maximum degree max1:
        # The answer is either 2 * max1 (if any pair is disconnected)
        # or 2 * max1 - 1 (if all pairs are directly connected).
        num_pairs = len(max1_nodes) * (len(max1_nodes) - 1) // 2

        # Pigeonhole Principle: If candidate pairs exceed total edges in the graph,
        # at least one pair is guaranteed to be disconnected.
        if num_pairs > len(roads):
            return 2 * max1

        for i in range(len(max1_nodes)):
            u = max1_nodes[i]
            for j in range(i + 1, len(max1_nodes)):
                v = max1_nodes[j]
                if v not in adj_sets[u]:
                    return 2 * max1

        return 2 * max1 - 1
    else:
        # Exactly 1 vertex has the maximum degree max1.
        # It must be paired with a vertex having the second maximum degree max2.
        max2 = unique_degrees[1] if len(unique_degrees) > 1 else 0
        max2_nodes = [i for i in range(n) if degree[i] == max2]

        u = max1_nodes[0]

        # If there are more max2 candidates than edges connected to u,
        # u cannot be connected to all of them.
        if len(max2_nodes) > degree[u]:
            return max1 + max2

        for v in max2_nodes:
            if v not in adj_sets[u]:
                return max1 + max2

        return max1 + max2 - 1
