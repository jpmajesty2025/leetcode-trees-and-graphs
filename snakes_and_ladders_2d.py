'''
You are given an n x n integer matrix board where the cells are labeled from 1 to n^2 in a 
Boustrophedon style.

This module calculates coordinates on-the-fly without 1D pre-flattening.
'''

from collections import deque


def snakes_and_ladders_2d(board: list[list[int]]) -> int:
    """Find least dice rolls using on-the-fly 2D Boustrophedon coordinate conversion."""
    n = len(board)
    target = n * n

    def get_coords(square: int) -> tuple[int, int]:
        r, c = divmod(square - 1, n)
        row = n - 1 - r
        col = c if (r % 2 == 0) else (n - 1 - c)
        return row, col

    visited = {1}
    queue: deque[tuple[int, int]] = deque([(1, 0)])  # (square, rolls)

    while queue:
        curr, rolls = queue.popleft()
        if curr == target:
            return rolls

        for roll in range(1, 7):
            next_sq = curr + roll
            if next_sq > target:
                break

            r, c = get_coords(next_sq)
            dest = board[r][c] if board[r][c] != -1 else next_sq

            if dest not in visited:
                visited.add(dest)
                queue.append((dest, rolls + 1))

    return -1


# Aliases
snakes_and_ladders = snakes_and_ladders_2d
snakesAndLadders = snakes_and_ladders_2d
