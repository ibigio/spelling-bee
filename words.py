import json

WORDS_FILE = 'data/words.txt'
FREQS_FILE = 'data/word_freqs.json'
VALIDITIES_FILE = 'data/word_validities.json'


def load_words() -> list[str]:
    with open(WORDS_FILE) as f:
        words = [w.strip().lower() for w in f]
        return [w for w in words if len(w) > 3 and len(set(w)) <= 7 and 's' not in w]


def load_freqs() -> dict[str, float]:
    with open(FREQS_FILE) as f:
        j = json.load(f)
        return {k: float(v) for k, v in j.items()}


def load_validities() -> dict[str, float]:
    with open(VALIDITIES_FILE) as f:
        j = json.load(f)
        return {k: float(v) for k, v in j.items()}
