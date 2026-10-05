'''
You are given a 2D array of strings equations and an array of real numbers values, 
where equations[i] = [Ai, Bi] and values[i] means that Ai / Bi = values[i].

Determine if there exists a contradiction in the equations. Return true if there is a contradiction, 
or false otherwise.

Note:
When checking if two numbers are equal, check that their absolute difference is less than 10-5.
'''


class WeightedUnionFind:
    """Disjoint Set Union (DSU) with multiplicative edge weights and path compression."""

    def __init__(self) -> None:
        self.parent: dict[str, str] = {}
        self.weight: dict[str, float] = {}  # weight[x] = x / parent[x]

    def find(self, x: str) -> tuple[str, float]:
        """Find the root of x and the cumulative ratio x / root(x)."""
        if x not in self.parent:
            self.parent[x] = x
            self.weight[x] = 1.0
            return x, 1.0

        if self.parent[x] != x:
            root, parent_to_root_ratio = self.find(self.parent[x])
            self.parent[x] = root
            self.weight[x] *= parent_to_root_ratio

        return self.parent[x], self.weight[x]

    def union(self, a: str, b: str, value: float) -> bool:
        """
        Merge relationship a / b = value.
        Returns True if a contradiction is detected, False otherwise.
        """
        root_a, weight_a = self.find(a)  # weight_a = a / root_a
        root_b, weight_b = self.find(b)  # weight_b = b / root_b

        if root_a == root_b:
            # Already connected: verify consistency of a / b
            # a / b = (a / root_a) / (b / root_b) = weight_a / weight_b
            implied_value = weight_a / weight_b
            if abs(implied_value - value) >= 1e-5:
                return True  # Contradiction!
            return False

        # Merge root_a into root_b:
        # a / b = value => (weight_a * root_a) / (weight_b * root_b) = value
        # => root_a / root_b = (value * weight_b) / weight_a
        self.parent[root_a] = root_b
        self.weight[root_a] = (value * weight_b) / weight_a
        return False


def check_contradictions(equations: list[list[str]], values: list[float]) -> bool:
    """Determine if there is a contradiction in equations using Weighted DSU."""
    uf = WeightedUnionFind()

    for (a, b), value in zip(equations, values):
        if uf.union(a, b, value):
            return True

    return False


# LeetCode backward compatibility aliases
checkContradictions = check_contradictions
