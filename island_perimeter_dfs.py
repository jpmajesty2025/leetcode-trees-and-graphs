'''
Determine the perimeter of an island using Depth-First Search (DFS).
'''

from typing import List


def island_perimeter_dfs(grid: List[List[int]]) -> int:
    """Calculate the perimeter of the island using DFS traversal.

    Time Complexity: O(R * C) in worst case (bounded by island size K).
    Space Complexity: O(K) for recursion call stack where K is the number of land cells.
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]

    def dfs(r: int, c: int) -> int:
        # If out of bounds or water, this contributes 1 unit to the perimeter
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == 0:
            return 1

        # If already visited land, contributes 0 to perimeter
        if visited[r][c]:
            return 0

        visited[r][c] = True

        # Explore all 4 orthogonal directions
        return (
            dfs(r - 1, c) +
            dfs(r + 1, c) +
            dfs(r, c - 1) +
            dfs(r, c + 1)
        )

    # Start DFS from the first land cell found
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                return dfs(r, c)

    return 0
