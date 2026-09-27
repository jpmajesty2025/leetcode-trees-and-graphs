'''
This module contains an iterative Breadth-First Search (BFS) implementation
to count the number of islands in a 2D grid.
'''

from collections import deque


def number_of_islands_bfs(grid: list[list[str]]) -> int:
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    islands = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and not visited[r][c]:
                islands += 1
                visited[r][c] = True
                queue = deque([(r, c)])

                while queue:
                    curr_r, curr_c = queue.popleft()
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1' and not visited[nr][nc]:
                            visited[nr][nc] = True  # Mark on enqueue to prevent duplicates
                            queue.append((nr, nc))

    return islands


# LeetCode backward compatibility alias
numIslands = number_of_islands_bfs
