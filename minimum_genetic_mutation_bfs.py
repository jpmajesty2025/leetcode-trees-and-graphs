'''
A gene string can be represented by an 8-character long string, with choices from 'A', 'C', 'G', and 'T'.

This module implements standard level-order BFS.
'''

from collections import deque


def min_mutation_bfs(start_gene: str, end_gene: str, bank: list[str]) -> int:
    """Find minimum mutations using standard level-order BFS."""
    if start_gene == end_gene:
        return 0
    bank_set = set(bank)
    if end_gene not in bank_set:
        return -1

    queue = deque([(start_gene, 0)])
    visited = {start_gene}
    gene_chars = ("A", "C", "G", "T")

    while queue:
        curr, mutations = queue.popleft()
        if curr == end_gene:
            return mutations

        curr_chars = list(curr)
        for i, original_char in enumerate(curr_chars):
            for ch in gene_chars:
                if ch == original_char:
                    continue
                curr_chars[i] = ch
                mutated = "".join(curr_chars)

                if mutated in bank_set and mutated not in visited:
                    visited.add(mutated)
                    queue.append((mutated, mutations + 1))

            curr_chars[i] = original_char

    return -1


# Aliases
min_mutation = min_mutation_bfs
minMutation = min_mutation_bfs
