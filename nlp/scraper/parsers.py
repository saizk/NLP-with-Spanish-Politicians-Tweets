import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
from pprint import pprint

from .util import traverse_dict


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


def tweets_parser(df, labels_dict):
    DetectorFactory.seed = 69420  # Seed for the language detector (deterministic)
    traversed_dict = traverse_dict(labels_dict)
    with ProcessPoolExecutor(max_workers=cpu_count()) as pool:
        futures = [
            pool.submit(parse_tweet, tweet, mention_replaces=traversed_dict) for tweet in df.text
        ]

    parsed_tweets = []
    for idx, future in enumerate(futures):
        result = future.result()
        if result:
            parsed_tweets.append((df.text[idx], result, df.author[idx], df.party[idx]))

    tweets_df = pd.DataFrame(parsed_tweets, columns=["Original Tweets", "Parsed Tweets", "Author", "Party"])
    return tweets_df


def parse_tweet(tweet, mention_replaces):
    tweet = remove_urls(tweet)
    if not is_spanish(tweet):
        return None

    parsed_tweet = []
    for word in tweet.split(" "):
        if "@" in word:
            user = remove_symbols(word).lower()
            word = parse_political_party_or_politician(user, mention_replaces)
        if word:
            parsed_tweet.append(
                remove_underscore(remove_hashtag(word))
            )
    return " ".join(parsed_tweet)


def parse_political_party_or_politician(text, replace_dict):
    return replace_dict.get(text, None)


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
