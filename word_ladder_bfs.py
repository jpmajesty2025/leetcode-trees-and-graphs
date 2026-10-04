'''
Given two words, beginWord and endWord, and a dictionary wordList, return the number of words in the 
shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.

This module implements standard single-source deque BFS.
'''

from collections import deque


def ladder_length_bfs(
    begin_word: str, end_word: str, word_list: list[str]
) -> int:
    """Return shortest transformation sequence length using standard deque BFS."""
    word_set = set(word_list)
    if end_word not in word_set:
        return 0
    if begin_word == end_word:
        return 1

    queue: deque[tuple[str, int]] = deque([(begin_word, 1)])
    word_set.discard(begin_word)
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    while queue:
        curr_word, steps = queue.popleft()
        if curr_word == end_word:
            return steps

        curr_chars = list(curr_word)
        for i, original_char in enumerate(curr_chars):
            for c in alphabet:
                if c == original_char:
                    continue
                curr_chars[i] = c
                candidate = "".join(curr_chars)

                if candidate in word_set:
                    word_set.remove(candidate)
                    queue.append((candidate, steps + 1))

            curr_chars[i] = original_char

    return 0


# Aliases
ladder_length = ladder_length_bfs
ladderLength = ladder_length_bfs
