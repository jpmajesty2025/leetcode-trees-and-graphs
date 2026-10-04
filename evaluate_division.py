'''
You are given an array of variable pairs equations and an array of real numbers values, 
where equations[i] = [Ai, Bi] and values[i] represent the equation Ai / Bi = values[i]. 
Each Ai or Bi is a string that represents a single variable.

You are also given some queries, where queries[j] = [Cj, Dj] represents the jth query where 
you must find the answer for Cj / Dj = ?.

Return the answers to all queries. If a single answer cannot be determined, return -1.0.
'''


def calc_equation(
    equations: list[list[str]], values: list[float], queries: list[list[str]]
) -> list[float]:
    """Evaluate division queries in O(1) amortized time per query using Weighted Union-Find."""
    parent: dict[str, str] = {}
    weight: dict[str, float] = {}  # weight[x] represents x / parent[x]

    def find(x: str) -> str:
        if x not in parent:
            parent[x] = x
            weight[x] = 1.0
            return x
        if parent[x] != x:
            orig_parent = parent[x]
            parent[x] = find(orig_parent)
            weight[x] *= weight[orig_parent]
        return parent[x]

    def union(a: str, b: str, val: float) -> None:
        root_a = find(a)
        root_b = find(b)
        if root_a != root_b:
            parent[root_a] = root_b
            # a = root_a * weight[a], b = root_b * weight[b]
            # a / b = val => (root_a * weight[a]) / (root_b * weight[b]) = val
            # => root_a / root_b = (weight[b] * val) / weight[a]
            weight[root_a] = (weight[b] * val) / weight[a]

    # Build DSU from equations
    for (a, b), val in zip(equations, values):
        union(a, b, val)

    results: list[float] = []
    for c, d in queries:
        if c not in parent or d not in parent:
            results.append(-1.0)
        else:
            root_c = find(c)
            root_d = find(d)
            if root_c != root_d:
                results.append(-1.0)
            else:
                # c / d = (c / root) / (d / root) = weight[c] / weight[d]
                results.append(weight[c] / weight[d])

    return results


# LeetCode backward compatibility aliases
calc_equation_union_find = calc_equation
calcEquation = calc_equation
