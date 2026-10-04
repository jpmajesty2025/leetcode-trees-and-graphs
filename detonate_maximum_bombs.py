'''
You are given a list of bombs. The range of a bomb is defined as the area where its effect can be felt. 
This area is in the shape of a circle with the center as the location of the bomb.

The bombs are represented by a 0-indexed 2D integer array bombs where bombs[i] = [xi, yi, ri]. xi and yi 
denote the X-coordinate and Y-coordinate of the location of the ith bomb, whereas ri denotes the radius 
of its range.

Return the maximum number of bombs that can be detonated if you are allowed to detonate only one bomb.
'''

from collections import deque


def maximum_detonation(bombs: list[list[int]]) -> int:
    """Determine the maximum number of bombs that can be detonated using integer arithmetic."""
    n = len(bombs)
    if n <= 1:
        return n

    # Build the directed graph using squared radii to avoid floating point sqrt
    graph: list[list[int]] = [[] for _ in range(n)]
    for i in range(n):
        x1, y1, r1 = bombs[i]
        r1_sq = r1 * r1
        for j in range(n):
            if i != j:
                x2, y2, _ = bombs[j]
                dx = x1 - x2
                dy = y1 - y2
                if dx * dx + dy * dy <= r1_sq:
                    graph[i].append(j)

    def bfs(start: int) -> int:
        """Perform BFS to count the number of bombs detonated starting from a given bomb."""
        queue: deque[int] = deque([start])
        visited: set[int] = {start}
        count = 0

        while queue:
            curr = queue.popleft()
            count += 1
            for neighbor in graph[curr]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return count

    max_detonated = 0
    for i in range(n):
        detonated = bfs(i)
        if detonated == n:
            return n  # Early exit: maximum possible detonation achieved
        if detonated > max_detonated:
            max_detonated = detonated

    return max_detonated


# LeetCode backward compatibility aliases
maximumDetonation = maximum_detonation
