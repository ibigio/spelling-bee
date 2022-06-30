import json
from os import read

FREQS_FILE = 'data/pruned.json'


def load_freqs_json(filepath: str):
    with open(filepath) as f:
        return json.load(f)


def binary_search():
    freqs = load_freqs_json(FREQS_FILE)
    freqs_list = sorted([(float(v), k) for k, v in freqs.items()])
    low = 0
    high = len(freqs_list)

    rate = 0.8

    while True:
        mid = int((low + high) / 2)
        word = freqs_list[mid]

        a = input(f'Do you know the word {word[1]}? [y/n]: ')
        if a == 'y':
            high -= int((high - mid) * rate)
        if a == 'n':
            low += int((mid - low) * rate)

        print(word)


binary_search()

# 1.529003
# 0.651036
