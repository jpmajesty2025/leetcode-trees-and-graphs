'''
Given an n x n binary matrix grid, return the length of the shortest clear path in the matrix. 
If there is no clear path, return -1.

This module implements A* Search guided by the 8-directional Chebyshev distance heuristic.
'''

import heapq


def shortest_path_binary_matrix_astar(grid: list[list[int]]) -> int:
    """Find the shortest clear path in a binary matrix using A* search with Chebyshev distance."""
    if not grid or not grid[0] or grid[0][0] == 1 or grid[-1][-1] == 1:
        return -1

    n = len(grid)
    if n == 1:
        return 1

    def heuristic(r: int, c: int) -> int:
        return max(n - 1 - r, n - 1 - c)  # Chebyshev distance

    pq = [(1 + heuristic(0, 0), 1, 0, 0)]  # (f, g, r, c)
    best_g = {(0, 0): 1}

    directions = (
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    )

    while pq:
        f, g, r, c = heapq.heappop(pq)

        if (r, c) == (n - 1, n - 1):
            return g

        if g > best_g.get((r, c), float('inf')):
            continue

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                ng = g + 1
                if ng < best_g.get((nr, nc), float('inf')):
                    best_g[(nr, nc)] = ng
                    heapq.heappush(pq, (ng + heuristic(nr, nc), ng, nr, nc))

    return -1


# Aliases
shortest_path_binary_matrix = shortest_path_binary_matrix_astar
shortestPathBinaryMatrix = shortest_path_binary_matrix_astar
