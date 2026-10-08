'''
Determine satisfiability of equality equations using Graph DFS Connected Components (Coloring).
'''

from typing import List


def equations_possible_dfs(equations: List[str]) -> bool:
    """Determine satisfiability of equations using DFS connected components.

    Time Complexity: O(N + 26) = O(N) where N is len(equations).
    Space Complexity: O(26) = O(1) auxiliary space for adjacency list and color array.
    """
    adj = [[] for _ in range(26)]

    def char_idx(c: str) -> int:
        return ord(c) - ord('a')

    # Build graph of equality edges
    for eq in equations:
        if eq[1] == '=':
            u, v = char_idx(eq[0]), char_idx(eq[3])
            adj[u].append(v)
            adj[v].append(u)

    # Color connected components
    colors = [-1] * 26
    current_color = 0

    for i in range(26):
        if colors[i] == -1:
            stack = [i]
            colors[i] = current_color
            while stack:
                node = stack.pop()
                for neighbor in adj[node]:
                    if colors[neighbor] == -1:
                        colors[neighbor] = current_color
                        stack.append(neighbor)
            current_color += 1

    # Check inequality constraints
    for eq in equations:
        if eq[1] == '!':
            u, v = char_idx(eq[0]), char_idx(eq[3])
            # If two variables share the same color, they are in the same equality component
            if colors[u] == colors[v]:
                return False

    return True
