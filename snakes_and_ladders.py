'''
You are given an n x n integer matrix board where the cells are labeled from 1 to n^2 in a 
Boustrophedon style starting from the bottom left of the board (i.e. board[n - 1][0]) and 
alternating direction each row.

You start on square 1 of the board. In each move, starting from square curr, choose a destination 
square next with a label in the range [curr + 1, min(curr + 6, n^2)].
If next has a snake or ladder, you must move to the destination of that snake or ladder. 
Otherwise, you move to next.

Return the least number of dice rolls required to reach the square n^2. If it is not possible, return -1.
'''

from collections import deque


def snakes_and_ladders(board: list[list[int]]) -> int:
    """Find least dice rolls to reach square n^2 using flattened 1D array and BFS."""
    n = len(board)
    target = n * n

    # Flatten board to 1D lookup array: index 1 to n^2
    flat_board = [-1] * (target + 1)
    idx = 1
    left_to_right = True

    for r in range(n - 1, -1, -1):
        cols = range(n) if left_to_right else range(n - 1, -1, -1)
        for c in cols:
            flat_board[idx] = board[r][c]
            idx += 1
        left_to_right = not left_to_right

    # BFS traversal
    dist = [-1] * (target + 1)
    dist[1] = 0
    queue: deque[int] = deque([1])

    while queue:
        curr = queue.popleft()
        if curr == target:
            return dist[curr]

        for roll in range(1, 7):
            next_sq = curr + roll
            if next_sq > target:
                break

            dest = flat_board[next_sq] if flat_board[next_sq] != -1 else next_sq

            if dist[dest] == -1:
                dist[dest] = dist[curr] + 1
                queue.append(dest)

    return -1


# LeetCode backward compatibility alias
snakesAndLadders = snakes_and_ladders
