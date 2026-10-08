'''
You are given an array of strings equations that represent relationships between variables where each 
string equations[i] is of length 4 and takes one of two different forms: "xi==yi" or "xi!=yi". Here, 
xi and yi are lowercase letters (not necessarily different) that represent one-letter variable names.

Return true if it is possible to assign integers to variable names so as to satisfy all the given 
equations, or false otherwise.

Example 1:
Input: equations = ["a==b","b!=a"]
Output: false
Explanation: If we assign say, a = 1 and b = 1, then the first equation is satisfied, but not the second.
There is no way to assign the variables to satisfy both equations.

Example 2:
Input: equations = ["b==a","a==b"]
Output: true
Explanation: We could assign a = 1 and b = 1 to satisfy both equations.

Constraints:
- 1 <= equations.length <= 500
- equations[i].length == 4
- equations[i][0] and equations[i][3] are lowercase letters.
- equations[i][1] is either '=' or '!'.
- equations[i][2] is '='.
'''

from typing import List


def equations_possible(equations: List[str]) -> bool:
    """Determine satisfiability of equality equations using Union-Find (Disjoint Set Union).

    Time Complexity: O(N * alpha(26)) = O(N) where N is len(equations).
    Space Complexity: O(1) auxiliary space (fixed 26-element array for alphabet letters).
    """
    # 26 lowercase English letters 'a' through 'z'
    parent = list(range(26))

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x: int, y: int) -> None:
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_x] = root_y

    def char_idx(c: str) -> int:
        return ord(c) - ord('a')

    # Pass 1: Union equivalence classes for all "==" equations
    for eq in equations:
        if eq[1] == '=':
            union(char_idx(eq[0]), char_idx(eq[3]))

    # Pass 2: Verify that "!=" relations do not contradict existing equivalence classes
    for eq in equations:
        if eq[1] == '!':
            if find(char_idx(eq[0])) == find(char_idx(eq[3])):
                return False

    return True


# Backward-compatible alias for LeetCode naming
equationsPossible = equations_possible
