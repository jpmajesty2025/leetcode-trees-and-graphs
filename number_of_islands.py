'''
This module contains a function to count the number of islands in a given 2D grid. 
An island is defined as a group of adjacent land cells (represented by '1') surrounded by water 
cells (represented by '0'). The function uses Depth-First Search (DFS) to explore and mark visited land cells.
'''


def number_of_islands(grid: list[list[str]]) -> int:
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    ans = 0

    def dfs(r: int, c: int) -> None:
        visited[r][c] = True
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1' and not visited[nr][nc]:
                dfs(nr, nc)

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1' and not visited[i][j]:
                ans += 1
                dfs(i, j)

    return ans


# LeetCode backward compatibility alias
numIslands = number_of_islands
