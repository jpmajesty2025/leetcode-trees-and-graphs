'''
You are given an m x n matrix maze (0-indexed) with empty cells (represented as '.') and walls 
(represented as '+'). You are also given the entrance of the maze.

This module implements a Bidirectional BFS meeting in the middle.
'''

from collections import deque


def nearest_exit_bidirectional(maze: list[list[str]], entrance: list[int]) -> int:
    """Find shortest path to exit using bidirectional BFS meeting in the middle."""
    rows, cols = len(maze), len(maze[0])
    start = (entrance[0], entrance[1])

    # Find all candidate boundary exits
    exits: set[tuple[int, int]] = set()
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == '.' and (r, c) != start:
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    exits.add((r, c))

    if not exits:
        return -1

    forward_visited: dict[tuple[int, int], int] = {start: 0}
    backward_visited: dict[tuple[int, int], int] = {exit_pos: 0 for exit_pos in exits}

    forward_queue: deque[tuple[int, int]] = deque([start])
    backward_queue: deque[tuple[int, int]] = deque(list(exits))

    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))

    while forward_queue and backward_queue:
        # Expand smaller wavefront
        if len(forward_queue) <= len(backward_queue):
            curr_q, curr_vis, opp_vis = forward_queue, forward_visited, backward_visited
        else:
            curr_q, curr_vis, opp_vis = backward_queue, backward_visited, forward_visited

        for _ in range(len(curr_q)):
            r, c = curr_q.popleft()
            curr_dist = curr_vis[(r, c)]

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == '.':
                    if (nr, nc) in opp_vis:
                        return curr_dist + 1 + opp_vis[(nr, nc)]
                    if (nr, nc) not in curr_vis:
                        curr_vis[(nr, nc)] = curr_dist + 1
                        curr_q.append((nr, nc))

    return -1


# Aliases
nearest_exit = nearest_exit_bidirectional
nearestExit = nearest_exit_bidirectional
