"""
Use the requests library to make a get request with the following parameters:

Request URL: https://www.nytbee.com/Bee_20200812.html
Request Method: GET
Status Code: 200
Remote Address: 162.241.225.30:443
Referrer Policy: strict-origin-when-cross-origin

Make sure to set the request headers to the following:

Request Headers
:authority: www.nytbee.com
:method: GET
:path: /Bee_20200812.html
:scheme: https
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: en-US,en;q=0.9
sec-ch-ua: "Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: none
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36
"""

import requests
import json
from bs4 import BeautifulSoup
from functools import cache
from datetime import date, timedelta, datetime

DATE_FORMAT = '%Y%m%d'
HISTORIC_FILE = 'data/historic.json'


@cache
def get_game_html(date: str):
    url = f"https://www.nytbee.com/Bee_{date}.html"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    }
    response = requests.get(url, headers=headers)
    return response.text


def get_valid(date: str):
    text = get_game_html(date)
    soup = BeautifulSoup(text, "html.parser")
    words = soup.select("#main-answer-list > ul > li")
    words = [word.text.strip() for word in words]
    return words


def get_invalid(date: str):
    text = get_game_html(date)
    soup = BeautifulSoup(text, "html.parser")
    words = soup.select("#not_official > div > ul > li")
    words = [word.text.strip() for word in words]
    return words


def gen_dates():
    d = date.today()
    while d >= date(2020, 1, 1):
        yield d.strftime('%Y%m%d')
        d -= timedelta(days=1)

def load_historic():
    with open(HISTORIC_FILE) as f:
        return json.load(f)


def save_historic(j):
    with open(HISTORIC_FILE, mode='w') as f:
        return json.dump(j, f)


def load_new_words():
    historic = load_historic()

    for d in gen_dates():
        datestr = d.format(DATE_FORMAT)
        if datestr in historic:
            continue
        valid, invalid = get_valid(
            datestr), get_invalid(datestr)
        if not valid:
            break
        historic[datestr] = {"valid": valid, "invalid": invalid}
        save_historic(historic)
        print(d)


def stats():
    h = load_historic()
    print(f"Days: {len(h)}")
    print(f"Valid: {sum([len(g['valid']) for g in h.values()])}")
    print(f"Valid: {sum([len(g['invalid']) for g in h.values()])}")
