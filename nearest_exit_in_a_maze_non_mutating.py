'''
You are given an m x n matrix maze (0-indexed) with empty cells (represented as '.') and walls 
(represented as '+'). You are also given the entrance of the maze.

This module preserves the input matrix without mutation using an auxiliary 2D boolean grid.
'''

from collections import deque


def nearest_exit_non_mutating(maze: list[list[str]], entrance: list[int]) -> int:
    """Find the shortest distance to nearest exit preserving the input matrix."""
    rows, cols = len(maze), len(maze[0])
    start_r, start_c = entrance[0], entrance[1]

    visited = [[False] * cols for _ in range(rows)]
    visited[start_r][start_c] = True
    queue: deque[tuple[int, int, int]] = deque([(start_r, start_c, 0)])
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))

    while queue:
        r, c, steps = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == '.' and not visited[nr][nc]:
                if nr == 0 or nr == rows - 1 or nc == 0 or nc == cols - 1:
                    return steps + 1

                visited[nr][nc] = True
                queue.append((nr, nc, steps + 1))

    return -1


# Aliases
nearest_exit = nearest_exit_non_mutating
nearestExit = nearest_exit_non_mutating
