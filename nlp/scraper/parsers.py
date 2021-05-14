import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from langdetect import detect
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor

from .parties import PARTIES


def wiki_parser():
    url = requests.get("https://es.wikipedia.org/wiki/Anexo:Diputados_de_la_XIV_legislatura_de_Espa%C3%B1a")
    soup = BeautifulSoup(url.text, "lxml")
    table = soup.find("table", {"class": "wikitable sortable"})
    df = pd.DataFrame(pd.read_html(str(table))[0])

    politics_names = df.get("Nombre y apellidos").to_list()
    for idx, pol in enumerate(politics_names):
        surname, name = pol.split(",")
        politics_names[idx] = f"{name} {surname}".strip()

    parties = df.get("Lista.1").to_list()

    politics = list(zip(politics_names, parties))
    parties = set(parties)

    return politics, parties


def tweets_parser(df):
    with ProcessPoolExecutor(max_workers=cpu_count()) as pool:
        futures = [pool.submit(parse_tweet, tweet) for tweet in df.text]

    parsed_tweets = []
    for future in futures:
        result = future.result()
        if result:
            parsed_tweets.append(result)

    return parsed_tweets


def parse_tweet(tweet):
    if not is_spanish(tweet):
        return None

    parsed_tweet = []
    for word in tweet.split(" "):
        if "@" in word:
            user = remove_symbols(word).lower()
            word = parse_political_party(user) or user.capitalize()
        parsed_tweet.append(
            remove_underscore(remove_hashtag(word))
        )
    return " ".join(parsed_tweet)


def parse_political_party(text):
    for party, accounts in PARTIES.items():
        if text in map(str.lower, accounts):
            return party


def is_spanish(text):
    parsed_text = remove_numbers(remove_symbols(text, add_space=True))
    return detect(parsed_text) == "es" if parsed_text else False


def remove_urls(text):
    return re.sub(r'http\S+', '', text.replace('\n', "")).strip()


def remove_underscore(text, add_space=False):
    rep = ' ' if add_space else ''
    return re.sub(r'_', rep, text).strip()


def remove_hashtag(text, add_space=False):
    rep = ' ' if add_space else ''
    return re.sub(r'#', rep, text).strip()


def remove_hashtag_word(text):
    return re.sub(r'#\S+', '', text).strip()


def remove_at_sign(text, add_space=False):
    rep = ' ' if add_space else ''
    return re.sub(r'@', rep, text).strip()


def remove_user_mention(text):
    return re.sub(r'@\S+', '', text).strip()


def remove_numbers(text):
    return re.sub(r'[0-9]', '', text).strip()


def remove_symbols(text, add_space=False):
    rep = ' ' if add_space else ''
    return re.sub(r'[^\w]', rep, text).strip()


# def make_second_letter_capital(user_mention):
#     return user_mention[:1] + chr(ord(user_mention[1]) - 32*(ord(user_mention[1]) >= 97) + user_mention[2:])
