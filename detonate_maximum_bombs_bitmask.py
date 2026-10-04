'''
You are given a list of bombs. The range of a bomb is defined as the area where its effect can be felt.

This module implements the bitmask transitive closure approach.
'''


def maximum_detonation_bitmask(bombs: list[list[int]]) -> int:
    """Determine max detonated bombs using bitset transitive closure."""
    n = len(bombs)
    if n <= 1:
        return n

    # reach[i] is an integer bitmask where j-th bit set means bomb i reaches bomb j
    reach = [(1 << i) for i in range(n)]

    for i in range(n):
        x1, y1, r1 = bombs[i]
        r1_sq = r1 * r1
        for j in range(n):
            if i != j:
                x2, y2, _ = bombs[j]
                dx = x1 - x2
                dy = y1 - y2
                if dx * dx + dy * dy <= r1_sq:
                    reach[i] |= (1 << j)

    # Bitwise Floyd-Warshall / Transitive Closure
    for k in range(n):
        k_mask = 1 << k
        for i in range(n):
            if reach[i] & k_mask:
                reach[i] |= reach[k]

    return max(mask.bit_count() for mask in reach)


# Aliases
maximum_detonation = maximum_detonation_bitmask
maximumDetonation = maximum_detonation_bitmask
