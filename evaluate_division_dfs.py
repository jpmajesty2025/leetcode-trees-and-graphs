'''
You are given an array of variable pairs equations and an array of real numbers values, 
where equations[i] = [Ai, Bi] and values[i] represent the equation Ai / Bi = values[i]. 

This module implements the graph traversal DFS approach.
'''

from collections import defaultdict


def calc_equation_dfs(
    equations: list[list[str]], values: list[float], queries: list[list[str]]
) -> list[float]:
    """Evaluate division queries using graph adjacency list and DFS path multiplication."""
    graph: defaultdict[str, dict[str, float]] = defaultdict(dict)
    for (a, b), val in zip(equations, values):
        graph[a][b] = val
        graph[b][a] = 1.0 / val

    def dfs(curr: str, target: str, visited: set[str]) -> float:
        if curr not in graph or target not in graph:
            return -1.0
        if curr == target:
            return 1.0
        visited.add(curr)
        for neighbor, weight in graph[curr].items():
            if neighbor not in visited:
                res = dfs(neighbor, target, visited)
                if res != -1.0:
                    return res * weight
        return -1.0

    return [dfs(c, d, set()) for c, d in queries]


# Aliases
calc_equation = calc_equation_dfs
calcEquation = calc_equation_dfs
