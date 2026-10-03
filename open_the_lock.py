'''
You have a lock in front of you with 4 circular wheels. Each wheel has 10 slots: 
'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'. The wheels can rotate freely and wrap around: 
for example we can turn '9' to be '0', or '0' to be '9'. Each move consists of turning one wheel one slot.

The lock initially starts at '0000', a string representing the state of the 4 wheels.

You are given a list of deadends dead ends, meaning if the lock displays any of these codes, 
the wheels of the lock will stop turning and you will be unable to open it.

Given a target representing the value of the wheels that will unlock the lock, return the minimum 
total number of turns required to open the lock, or -1 if it is impossible.
'''


def open_lock(deadends: list[str], target: str) -> int:
    """Find the minimum number of turns to open the lock using Bidirectional Set BFS."""
    dead_set = set(deadends)
    if '0000' in dead_set or target in dead_set:
        return -1
    if target == '0000':
        return 0

    forward: set[str] = {'0000'}
    backward: set[str] = {target}
    visited: set[str] = {'0000', target}
    turns = 0

    while forward and backward:
        # Always expand the smaller frontier to minimize branching
        if len(forward) > len(backward):
            forward, backward = backward, forward

        next_level: set[str] = set()
        turns += 1

        for state in forward:
            for i in range(4):
                digit = int(state[i])
                for move in (-1, 1):
                    new_digit = (digit + move) % 10
                    new_state = state[:i] + str(new_digit) + state[i + 1:]

                    if new_state in backward:
                        return turns
                    if new_state not in dead_set and new_state not in visited:
                        visited.add(new_state)
                        next_level.add(new_state)

        forward = next_level

    return -1


# LeetCode backward compatibility aliases
open_lock_bidirectional = open_lock
openLock = open_lock
