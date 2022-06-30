from scipy.sparse.construct import rand
import words
from dataclasses import dataclass
from string import ascii_lowercase
from collections import defaultdict
import random


WORDS = words.load_words()
FREQS = words.load_freqs()
VALIDITIES = words.load_validities()

# WORDS = [w for w in WORDS if VALIDITIES[w] > 0.5]

THRESHOLD = 0.5


class LetterSet(set):
    def __init__(self, string=None):
        if string:
            super().__init__(set(string))
        else:
            super().__init__()

    def __hash__(self):
        return hash(tuple(sorted(self)))


LSETS = list(set(LetterSet(w) for w in WORDS))

LSET_TO_WORDS: dict[LetterSet, set[str]] = defaultdict(set)
for w in WORDS:
    LSET_TO_WORDS[LetterSet(w)].add(w)


def generate_game(lset: LetterSet):
    return set(ls for ls in LSETS if ls.issubset(lset))


def print_random_game():
    # not even an actual word lol
    letters = random.choice([''.join(lset)
                            for lset in LSETS if len(lset) == 7])
    print_game(letters)


def print_game(word: str):
    words = set()
    for lset in generate_game(LetterSet(word)):
        words |= LSET_TO_WORDS[lset]

    words = sorted(words, key=lambda x: (len(x), x))
    pangrams = [w for w in words if len(set(w)) == 7]
    words = list(set(words) - set(pangrams))

    valid_pangrams = [w for w in pangrams if VALIDITIES[w] >= THRESHOLD]
    invalid_pangrams = [w for w in pangrams if VALIDITIES[w] < THRESHOLD]
    valid = [w for w in words if VALIDITIES[w] >= THRESHOLD]
    invalid = [w for w in words if VALIDITIES[w] < THRESHOLD]

    print(f'Valid [{len(valid)}]:')
    print(valid_pangrams)
    print(valid)
    # for w in valid:
    #     print(w)
    print()

    print(f'Invalid [{len(invalid)}]:')
    print(invalid_pangrams)
    print(invalid)
    # for w in invalid:
    #     print(w)


def subsets(words: list[str]):
    lsets = list(set(LetterSet(w) for w in words))
    letter_to_sets: dict[str, set[LetterSet]] = defaultdict(set)

    # Map each letter to the sets that contain that letter
    for c in ascii_lowercase:
        for lset in lsets:
            if c in lset:
                letter_to_sets[c].add(lset)

    all_games: dict[LetterSet, set(LetterSet)] = dict()

    for i, lset7 in enumerate([x for x in lsets if len(x) == 7]):
        if i % 100 == 0:
            print(f'{i}.', lset7)
        all_games[lset7] = set(lset for lset in lsets if lset.issubset(lset7))
    return all_games
