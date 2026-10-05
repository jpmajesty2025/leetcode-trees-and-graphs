'''
Determine if there exists a contradiction in equations using Connected Components BFS.
'''

from collections import defaultdict, deque


def check_contradictions_bfs(
    equations: list[list[str]], values: list[float]
) -> bool:
    """Check for contradictions in equations using incremental BFS component valuation."""
    graph: dict[str, dict[str, float]] = defaultdict(dict)

    # Check for direct duplicates/contradictions or validate on insertion
    for (a, b), value in zip(equations, values):
        if a == b:
            if abs(value - 1.0) >= 1e-5:
                return True
            continue

        if b in graph[a]:
            if abs(graph[a][b] - value) >= 1e-5:
                return True
            continue

        # Check if path already exists between a and b
        # Find ratio a / b in existing graph
        queue: deque[tuple[str, float]] = deque([(a, 1.0)])
        visited: set[str] = {a}
        found_ratio: float | None = None

        while queue:
            curr, ratio = queue.popleft()
            if curr == b:
                found_ratio = ratio
                break

            for nxt, weight in graph[curr].items():
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, ratio * weight))

        if found_ratio is not None:
            if abs(found_ratio - value) >= 1e-5:
                return True  # Contradiction with existing path
        else:
            # Add edge to graph
            graph[a][b] = value
            graph[b][a] = 1.0 / value

    return False


# Aliases
check_contradictions = check_contradictions_bfs
checkContradictions = check_contradictions_bfs
