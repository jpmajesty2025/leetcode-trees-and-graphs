'''
This module contains an iterative Depth-First Search (DFS) implementation using
an explicit stack to count the number of islands in a 2D grid safely without recursion limits.
'''


def num_islands_iterative(grid: list[list[str]]) -> int:
    if not grid or not grid[0]:
        return 0

    m = len(grid)
    n = len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    seen = set()
    ans = 0

    def valid(row: int, col: int) -> bool:
        return 0 <= row < m and 0 <= col < n and grid[row][col] == "1"

    def dfs(start_row: int, start_col: int) -> None:
        stack = [(start_row, start_col)]
        while stack:
            row, col = stack.pop()
            for dr, dc in directions:
                next_row, next_col = row + dr, col + dc
                if valid(next_row, next_col) and (next_row, next_col) not in seen:
                    seen.add((next_row, next_col))
                    stack.append((next_row, next_col))

    for row in range(m):
        for col in range(n):
            if grid[row][col] == "1" and (row, col) not in seen:
                ans += 1
                seen.add((row, col))
                dfs(row, col)

    return ans


# Aliases
number_of_islands_iterative_dfs = num_islands_iterative
numIslands = num_islands_iterative
