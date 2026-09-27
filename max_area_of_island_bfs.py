'''
You are given an m x n binary matrix grid. An island is a group of 1's (representing land) connected 
4-directionally (horizontal or vertical, not diagonally.) You may assume all four edges of the grid are surrounded by water.

The area of an island is the number of cells with a value 1 in the island.

Return the maximum area of an island in grid. If there is no island, return 0.
'''

from collections import deque


def max_area_of_island_bfs(grid: list[list[int]]) -> int:
    """Find the maximum area of an island in a binary matrix using iterative BFS."""
    if not grid or not grid[0]:
        return 0

    m, n = len(grid), len(grid[0])
    visited = [[False] * n for _ in range(m)]
    max_area = 0

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1 and not visited[i][j]:
                visited[i][j] = True
                queue = deque([(i, j)])
                current_area = 0

                while queue:
                    r, c = queue.popleft()
                    current_area += 1
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1 and not visited[nr][nc]:
                            visited[nr][nc] = True
                            queue.append((nr, nc))

                max_area = max(max_area, current_area)

    return max_area


# Aliases
max_area_of_island = max_area_of_island_bfs
maxAreaOfIsland = max_area_of_island_bfs
