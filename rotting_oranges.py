'''
You are given an m x n grid where each cell can have one of three values:
- 0 representing an empty cell,
- 1 representing a fresh orange, or
- 2 representing a rotten orange.

Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a fresh orange. 
If this is impossible, return -1.

Example 1:
Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
Output: 4

Example 2:
Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
Output: -1
Explanation: The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.

Example 3:
Input: grid = [[0,2]]
Output: 0
Explanation: Since there are already no fresh oranges at minute 0, the answer is just 0.

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 10
- grid[i][j] is 0, 1, or 2.
'''

from collections import deque
from typing import List


def oranges_rotting(grid: List[List[int]]) -> int:
    """Calculate the minimum minutes for all fresh oranges to rot using Multi-Source BFS.

    Time Complexity: O(M * N) where M is rows and N is columns.
    Space Complexity: O(M * N) for the BFS queue.
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh_count = 0

    # Seed the queue with all initial rotten oranges and tally fresh oranges
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh_count += 1

    if fresh_count == 0:
        return 0

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    minutes_passed = 0

    # Level-by-level multi-source BFS
    while queue and fresh_count > 0:
        minutes_passed += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2  # Mark rotten in-place
                    fresh_count -= 1
                    queue.append((nr, nc))

    return minutes_passed if fresh_count == 0 else -1


# Backward-compatible alias for LeetCode naming
orangesRotting = oranges_rotting
