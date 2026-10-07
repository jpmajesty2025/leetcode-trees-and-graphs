'''
You are given an m x n binary matrix grid, where 0 represents a sea cell and 1 represents a land cell.

A move consists of walking from one land cell to another adjacent (4-directionally) land cell or 
walking off the boundary of the grid.

Return the number of land cells in grid for which we cannot walk off the boundary of the grid in 
any number of moves.

Example 1:
Input: grid = [[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]]
Output: 3
Explanation: There are three 1s that are enclosed by 0s, and one 1 that isn't because it's on the boundary.

Example 2:
Input: grid = [[0,1,1,0],[0,0,1,0],[0,0,1,0],[0,0,0,0]]
Output: 0
Explanation: All 1s are either on the boundary or can reach the boundary.

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 500
- grid[i][j] is either 0 or 1.
'''

from typing import List


def num_enclaves(grid: List[List[int]]) -> int:
    """Count land cells that cannot reach the grid boundary via in-place boundary flood fill.

    Time Complexity: O(M * N) where M is the number of rows and N is the number of columns.
    Space Complexity: O(M * N) for the recursion stack in the worst case.
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])

    def dfs(r: int, c: int) -> None:
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != 1:
            return
        grid[r][c] = 0  # Flood-fill boundary-connected land with sea (0)
        dfs(r - 1, c)
        dfs(r + 1, c)
        dfs(r, c - 1)
        dfs(r, c + 1)

    # Flood-fill from top and bottom boundaries
    for c in range(cols):
        if grid[0][c] == 1:
            dfs(0, c)
        if grid[rows - 1][c] == 1:
            dfs(rows - 1, c)

    # Flood-fill from left and right boundaries
    for r in range(rows):
        if grid[r][0] == 1:
            dfs(r, 0)
        if grid[r][cols - 1] == 1:
            dfs(r, cols - 1)

    # Count all remaining unreached land cells
    enclave_count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                enclave_count += 1

    return enclave_count
