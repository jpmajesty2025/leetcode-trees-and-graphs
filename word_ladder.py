'''
A transformation sequence from word beginWord to word endWord using a dictionary wordList is a 
sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:

Every adjacent pair of words differs by a single letter.
Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
sk == endWord
Given two words, beginWord and endWord, and a dictionary wordList, return the number of words in the 
shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.
'''


def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    """Return shortest transformation sequence length using Bidirectional BFS."""
    word_set = set(word_list)
    if end_word not in word_set:
        return 0
    if begin_word == end_word:
        return 1

    front: set[str] = {begin_word}
    back: set[str] = {end_word}
    word_set.discard(begin_word)
    word_set.discard(end_word)

    length = 1
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    while front and back:
        # Always expand the smaller frontier to minimize branching
        if len(front) > len(back):
            front, back = back, front

        next_front: set[str] = set()
        length += 1

        for word in front:
            word_chars = list(word)
            for i, original_char in enumerate(word_chars):
                for c in alphabet:
                    if c == original_char:
                        continue
                    word_chars[i] = c
                    candidate = "".join(word_chars)

                    if candidate in back:
                        return length

                    if candidate in word_set:
                        word_set.remove(candidate)  # In-place visited pruning
                        next_front.add(candidate)

                word_chars[i] = original_char

        front = next_front

    return 0


# LeetCode backward compatibility aliases
ladderLength = ladder_length
