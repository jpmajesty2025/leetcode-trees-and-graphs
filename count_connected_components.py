'''
You have a graph of n nodes. You are given an integer n and an array edges where edges[i] = [ai, bi] 
indicates that there is an edge between ai and bi in the graph.

Return the number of connected components in the graph.
'''


def count_components(n: int, edges: list[list[int]]) -> int:
    """Count the number of connected components in an undirected graph using iterative DFS."""
    if n <= 0:
        return 0

    # Build adjacency list using fixed-size lists
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n
    components = 0

    for i in range(n):
        if not visited[i]:
            components += 1
            visited[i] = True
            stack = [i]

            while stack:
                curr = stack.pop()
                for neighbor in graph[curr]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        stack.append(neighbor)

    return components


# LeetCode backward compatibility aliases
count_components_dfs = count_components
countComponents = count_components
