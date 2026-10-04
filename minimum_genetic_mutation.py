'''
A gene string can be represented by an 8-character long string, with choices from 'A', 'C', 'G', and 'T'.

Suppose we need to investigate a mutation from a gene string startGene to a gene string endGene where 
one mutation is defined as one single character changed in the gene string.

Given the two gene strings startGene and endGene and the gene bank bank, return the minimum number of 
mutations needed to mutate from startGene to endGene. If there is no such a mutation, return -1.
'''


def min_mutation(start_gene: str, end_gene: str, bank: list[str]) -> int:
    """Find minimum mutations using Bidirectional BFS with frontier swapping."""
    if start_gene == end_gene:
        return 0
    bank_set = set(bank)
    if end_gene not in bank_set:
        return -1

    front_frontier: set[str] = {start_gene}
    back_frontier: set[str] = {end_gene}
    visited: set[str] = {start_gene, end_gene}
    steps = 0
    gene_chars = ("A", "C", "G", "T")

    while front_frontier and back_frontier:
        # Always expand the smaller frontier to minimize search space
        if len(front_frontier) > len(back_frontier):
            front_frontier, back_frontier = back_frontier, front_frontier

        next_frontier: set[str] = set()
        steps += 1

        for gene in front_frontier:
            gene_list = list(gene)
            for i, original_char in enumerate(gene_list):
                for ch in gene_chars:
                    if ch == original_char:
                        continue
                    gene_list[i] = ch
                    mutated = "".join(gene_list)

                    if mutated in back_frontier:
                        return steps

                    if mutated in bank_set and mutated not in visited:
                        visited.add(mutated)
                        next_frontier.add(mutated)

                gene_list[i] = original_char

        front_frontier = next_frontier

    return -1


# LeetCode backward compatibility aliases
minMutation = min_mutation
