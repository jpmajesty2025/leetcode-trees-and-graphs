'''
You are given an m x n matrix maze (0-indexed) with empty cells (represented as '.') and walls 
(represented as '+'). You are also given the entrance of the maze, where entrance = 
[entrancerow, entrancecol] denotes the row and column of the cell you are initially standing at.

In one step, you can move one cell up, down, left, or right. You cannot step into a cell with a wall, 
and you cannot step outside the maze. Your goal is to find the nearest exit from the entrance. 
An exit is defined as an empty cell that is at the border of the maze. The entrance does not count 
as an exit.

Return the number of steps in the shortest path from the entrance to the nearest exit, or -1 if no 
such path exists.
'''

from collections import deque


def nearest_exit(maze: list[list[str]], entrance: list[int]) -> int:
    """Find the shortest distance to the nearest exit using BFS with in-place visited marking."""
    rows, cols = len(maze), len(maze[0])
    start_r, start_c = entrance[0], entrance[1]

    # Mark entrance as visited in-place
    maze[start_r][start_c] = '+'
    queue: deque[tuple[int, int, int]] = deque([(start_r, start_c, 0)])
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))

    while queue:
        r, c, steps = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == '.':
                # Check for exit immediately at neighbor generation
                if nr == 0 or nr == rows - 1 or nc == 0 or nc == cols - 1:
                    return steps + 1

                # Mark visited and enqueue
                maze[nr][nc] = '+'
                queue.append((nr, nc, steps + 1))

    return -1


# LeetCode backward compatibility aliases
nearest_exit_in_place = nearest_exit
nearestExit = nearest_exit
