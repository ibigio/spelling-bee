import words
import json
from collections import defaultdict


freqs = words.load_freqs()

words = words.load_words()
words = [w for w in words if len(set(w)) <= 7 and len(set(w)) > 3]
words = [w for w in words if w in freqs and freqs[w] >= 0.651036]
unique_sets = set(tuple(sorted(set(w))) for w in words)
print(len(words))


def is_subgram_of(word: str, subgram: str) -> bool:
    return set(subgram).issubset(set(word))


def get_subgrams(word: str, dictionary: list[str]):
    return [s for s in dictionary if len(s) > 3 and is_subgram_of(word, s)]


def get_subgrams_with_letter(word: str, dictionary: list[str], letter: str):
    return [w for w in get_subgrams(word, dictionary) if letter in w]

# def get_subsets_for_sets(sets: list[set[str]]):
#     results = dict()
#     for s in sets:
#         for subset in sets:

# print(','.join(words[100:140]))
# W = words[:200]
# z = ngrams.get_large_batch_ngram_data(W)
# for w in W:
#     print(w, z[w][-1] if w in z else 'None')


# for w in words[:20]:
#     d = ngrams.get_ngram_data(w)
#     print(d[-1])

letters_to_words: dict[tuple[str], set[str]] = defaultdict(set)
for w in words:
    letters_to_words[tuple(sorted(set(w)))].add(w)

valid_sets = [set(s) for s in unique_sets if len(s) == 7]
bags_of_letters = [set(w) for w in letters_to_words.keys()]

ordered_valid_sets = reversed(sorted(valid_sets, key=lambda x: len(
    letters_to_words[tuple(sorted(x))])))

# for w in get_subgrams_with_letter('prognosis', words, 'p'):
#     if len(set(w)) is 7:
#         print(w)
# print(len(get_subgrams_with_letter('excitement', words, 'm')))


def set_to_words(s):
    return list(letters_to_words[tuple(sorted(s))])


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(
                    1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def grouped_led(words):
    acc = float('inf')
    for i in range(len(words)):
        for j in range(len(words) - i - 1):
            j = j + i + 1
            led = levenshteinDistance(words[i], words[j])
            acc = min(led, acc)
    return acc


ordered_valid_sets = sorted(
    ordered_valid_sets, key=lambda x: grouped_led(set_to_words(x)))

for vs in list(ordered_valid_sets):
    if 's' in vs:
        continue
    sub_words = letters_to_words[tuple(sorted(vs))]
    if len(sub_words) != 8:
        continue
    print(vs)
    print(', '.join(sub_words))
    print()

# print(len(valid_sets))
# for i, vs in enumerate(valid_sets):
#     subsets = [w for w in bags_of_letters if w.issubset(vs)]
#     print(f"{i}.", len(subsets), vs)


# print(len(bags_of_letters))


# print(len(valid_sets))
# ordered_sets = sorted(valid_sets, key=lambda s: len(get_subgrams(s, words)))


# for w in list(unique_sets)[:20]:
#     print(f'==={w}=== [{set(w)}]')
#     print(get_subgrams(w, words))
#     print()


# for each set in list A, find the number of subsets present in list B
