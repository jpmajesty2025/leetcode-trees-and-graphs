'''
You have a lock in front of you with 4 circular wheels. Each wheel has 10 slots.

This module implements standard unidirectional Queue BFS with push-time termination.
'''

from collections import deque


def open_lock_bfs(deadends: list[str], target: str) -> int:
    """Find minimum turns to open lock using standard single-source BFS."""
    dead_set = set(deadends)
    if '0000' in dead_set or target in dead_set:
        return -1
    if target == '0000':
        return 0

    queue: deque[tuple[str, int]] = deque([('0000', 0)])
    visited: set[str] = {'0000'}

    while queue:
        state, turns = queue.popleft()

        for i in range(4):
            digit = int(state[i])
            for move in (-1, 1):
                new_digit = (digit + move) % 10
                new_state = state[:i] + str(new_digit) + state[i + 1:]

                if new_state == target:
                    return turns + 1

                if new_state not in dead_set and new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, turns + 1))

    return -1


# Aliases
open_lock = open_lock_bfs
openLock = open_lock_bfs
