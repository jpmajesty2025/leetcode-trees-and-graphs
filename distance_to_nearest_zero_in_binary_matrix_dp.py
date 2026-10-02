'''
Given an m x n binary matrix mat, return the distance of the nearest 0 for each cell.

This module implements the optimal Two-Pass Dynamic Programming approach.
'''


def update_matrix_dp(mat: list[list[int]]) -> list[list[int]]:
    """Calculate distance to nearest 0 using Two-Pass Dynamic Programming."""
    if not mat or not mat[0]:
        return []

    m, n = len(mat), len(mat[0])
    inf = m + n
    dist = [[0 if mat[r][c] == 0 else inf for c in range(n)] for r in range(m)]

    # Pass 1: Top-Left to Bottom-Right (check Top and Left neighbors)
    for r in range(m):
        for c in range(n):
            if dist[r][c] != 0:
                top = dist[r - 1][c] if r > 0 else inf
                left = dist[r][c - 1] if c > 0 else inf
                dist[r][c] = min(top + 1, left + 1)

    # Pass 2: Bottom-Right to Top-Left (check Bottom and Right neighbors)
    for r in range(m - 1, -1, -1):
        for c in range(n - 1, -1, -1):
            if dist[r][c] != 0:
                bottom = dist[r + 1][c] if r < m - 1 else inf
                right = dist[r][c + 1] if c < n - 1 else inf
                dist[r][c] = min(dist[r][c], bottom + 1, right + 1)

    return dist


# Aliases
update_matrix = update_matrix_dp
updateMatrix = update_matrix_dp
