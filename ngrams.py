import requests
import json

URL = 'https://books.google.com/ngrams/graph'


def get_batch_ngram_data(words: list[str]) -> dict[str, list[str]]:
    results = dict()
    url = URL
    params = {
        'content': ','.join(words),
        'year_start': '1800',
        'year_end': '2019',
        'corpus': '26',
    }
    r = requests.get(url, params=params)

    # ugly html parsing of the ngram timeseries
    chunks = r.text.split('\n')
    relevant = list(filter(lambda x: 'ngrams.data' in x, chunks))
    if not relevant:
        print(r)
        exit()
        return dict()
    json_str = relevant[0].strip()[14:-1]
    j = json.loads(json_str)

    for data in j:
        results[data['ngram']] = data['timeseries']

    return results


def get_large_batch_ngram_data(many_words: list[str], batch_size=10) -> dict[str, list[str]]:
    results = dict()

    words_left = many_words.copy()

    while words_left:
        print(len(words_left), 'words left')
        batch = words_left[:batch_size]
        batch_results = get_batch_ngram_data(batch)

        if not batch_results:
            words_left = words_left[batch_size:]
            continue

        for word in batch_results:
            words_left.remove(word)
            results[word] = batch_results[word]

    return results


def get_ngram_data(word: str) -> list[str]:
    return get_batch_ngram_data([word])[word]
