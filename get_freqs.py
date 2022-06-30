import requests
import time
import json
import datetime

WORDS_FILE = 'data/words.txt'
FREQS_FILE = 'data/word_freqs.json'

_wait = 0.5


def get_freq(term):
    response = None
    while True:
        try:
            response = requests.get(
                f'https://api.datamuse.com/words?sp={term}&md=f&max=1').json()
        except:
            print('Could not get response. Sleep and retry...')
            time.sleep(_wait)
            continue
        break
    freq = 0.0 if len(response) == 0 else float(response[0]['tags'][0][2:])
    return freq


def get_some_freqs(term) -> dict:
    response = None
    while True:
        try:
            response = requests.get(
                f'https://api.datamuse.com/words?sp={term}&md=f').json()
        except:
            print('Could not get response. Sleep and retry...')
            time.sleep(_wait)
            continue
        break
    new_freqs = {r['word']: r['tags'][0][2:] for r in response}
    if term not in new_freqs:
        new_freqs[term] = 0
    return new_freqs


def load_words(filepath: str):
    with open(filepath) as f:
        return list([w.strip().lower() for w in f])


def load_freqs_json(filepath: str):
    with open(filepath) as f:
        return json.load(f)


def prioritize_pangrams(words: list[str]):
    pangrams = [w for w in words if len(set(w)) == 7]
    rest = list(set(words) - set(pangrams))
    prioritized = pangrams + rest
    assert(len(prioritized) == len(words))
    return prioritized


def try_find_first_pangram(words):
    for w in words:
        if len(set(w)) == 7:
            return w
    return words[0]


def load_and_save_all_freqs():
    freqs: dict = load_freqs_json(FREQS_FILE)
    words = load_words(WORDS_FILE)
    word_set = set(words)
    remaining = list(sorted(set(words) - freqs.keys()))
    times = []
    quant_updates = []

    while remaining:
        start = time.time()
        word = try_find_first_pangram(remaining)
        print('===', word)
        new_freqs = get_some_freqs(word)
        if not new_freqs:
            print('NO FREQS FOR', word)
            continue

        new_freqs = {k: v for k, v in new_freqs.items() if k in word_set}

        # add new freqs
        for maybe_new_word in new_freqs:
            freqs[maybe_new_word] = new_freqs[maybe_new_word]
        save_freqs(FREQS_FILE, freqs)

        new_remaning = list(sorted(set(remaining) - new_freqs.keys()))
        num_updated = len(remaining) - len(new_remaning)
        print

        # update stats
        times.append(time.time() - start)
        # intervals = [t - start for t in times]
        quant_updates.append(num_updated)

        # update remaining
        for new_word in set(remaining) - set(new_remaning):
            print(new_word)
        remaining = new_remaning

        # print stats
        avg_len = 100
        moving_avg = sum(times[-avg_len:])/sum(quant_updates[-avg_len:])
        seconds_remaining = moving_avg * len(remaining)
        print(len(remaining), '...', str(
            datetime.timedelta(seconds=seconds_remaining)))

    # for i, word in enumerate(words):
    #     freq = get_freq(word)
    #     freqs[word] = freq
    #     print(f'{i}/{len(words)}', word)
    #     seconds = ((time.time() - start) / (i + 1)) * (len(words) - i)
    #     print(str(datetime.timedelta(seconds=seconds)))
    #     save_freqs(FREQS_FILE, freqs)


def save_freqs(filename, freqs):
    with open(filename, mode='w') as f:
        json.dump(freqs, f)


load_and_save_all_freqs()
