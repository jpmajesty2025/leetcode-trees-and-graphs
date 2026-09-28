'''
Given an n x n binary matrix grid, return the length of the shortest clear path in the matrix. 
If there is no clear path, return -1.

This module implements Bidirectional BFS expanding simultaneously from (0, 0) and (n-1, n-1).
'''

from collections import deque


def shortest_path_binary_matrix_bidirectional(grid: list[list[int]]) -> int:
    """Find the shortest path using Bidirectional BFS expanding from start and goal."""
    if not grid or not grid[0] or grid[0][0] == 1 or grid[-1][-1] == 1:
        return -1

    n = len(grid)
    if n == 1:
        return 1

    dist_start = {(0, 0): 1}
    dist_goal = {(n - 1, n - 1): 1}

    q_start = deque([(0, 0)])
    q_goal = deque([(n - 1, n - 1)])

    directions = (
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    )

    while q_start and q_goal:
        # Always expand the smaller frontier
        if len(q_start) > len(q_goal):
            q_start, q_goal = q_goal, q_start
            dist_start, dist_goal = dist_goal, dist_start

        for _ in range(len(q_start)):
            r, c = q_start.popleft()
            d = dist_start[(r, c)]

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    if (nr, nc) in dist_goal:
                        return d + dist_goal[(nr, nc)]
                    if (nr, nc) not in dist_start:
                        dist_start[(nr, nc)] = d + 1
                        q_start.append((nr, nc))

    return -1


# Aliases
shortest_path_binary_matrix = shortest_path_binary_matrix_bidirectional
shortestPathBinaryMatrix = shortest_path_binary_matrix_bidirectional
