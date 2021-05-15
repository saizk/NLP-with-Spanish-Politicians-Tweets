import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
from pprint import pprint

from .models import get_politics_twitter_dict
from .parties import MAIN_PARTIES, PARTIES_TWITTERS, TR_MAIN_PARTIES
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


def tweets_parser(df, parameters: dict, session):
    DetectorFactory.seed = 69420  # Seed for the language detector (deterministic)

    parse_func, labels_dict = set_parameters(session, parameters)

    with ProcessPoolExecutor(max_workers=cpu_count()) as pool:
        futures = [
            pool.submit(
                parse_tweet, tweet,
                parse_func, mention_replaces=labels_dict
            )
            for tweet in df.text
        ]

    parsed_tweets = []
    for idx, future in enumerate(futures):
        result = future.result()
        if result:
            parsed_tweets.append((df.text[idx], result, df.favs[idx], df.retweets[idx], df.author[idx], df.party[idx]))

    tweets_df = pd.DataFrame(
        parsed_tweets,
        columns=["Original Tweets", "Parsed Tweets", "Likes", "Retweets", "Author", "Party"]
    )
    return tweets_df


def parse_tweet(tweet, parse_func, mention_replaces):
    tweet = remove_urls(tweet)
    if not is_spanish(tweet):
        return None

    parsed_tweet = []
    for word in tweet.split(" "):
        word = replace_party(remove_full_stop_and_commas(word))
        if "@" in word:
            # replace twitter usernames by party or politician names
            word = remove_full_stop_and_commas(remove_at_sign(word)).lower()
            word = replace_twitter_users(word, mention_replaces)
        if "#" in word:
            word = parse_func(word)
        if word:
            parsed_tweet.append(word)

    return " ".join(parsed_tweet)


def replace_twitter_users(text, replace_dict):
    return replace_dict.get(text, '')


def replace_party(word):
    return TR_MAIN_PARTIES.get(word, word)


def is_spanish(text):
    parsed_text = remove_numbers(remove_symbols(text, add_space=True))
    return detect(parsed_text) == "es" if parsed_text else False


def set_parameters(session, parameters: dict):
    politics_twitters = get_politics_twitter_dict(session)
    parse_func = remove_hashtag_word if parameters["remove_hashtag_word"] else remove_hashtag

    labels_dict = {}
    if parameters["replace_politics"]:
        labels_dict.update(politics_twitters)
    if parameters["replace_parties"]:
        labels_dict.update(PARTIES_TWITTERS)

    return parse_func, traverse_dict(labels_dict)


def remove_urls(text):
    return re.sub(r'http\S+', '', text.replace('\n', "")).strip()


def remove_full_stop_and_commas(text):
    return re.sub(r'[, .]', '', text).strip()


def remove_underscore(text, add_space=False):
    rep = ' ' if add_space else ''
    return re.sub(r'_', rep, text).strip()


def remove_hashtag(text, add_space=True):
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
