import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor

from .models import get_politicians_twitter_dict
from .parties import PARTIES_TWITTERS, TR_MAIN_PARTIES
from .util import traverse_dict


def wiki_parser():
    url = requests.get("https://es.wikipedia.org/wiki/Anexo:Diputados_de_la_XIV_legislatura_de_Espa%C3%B1a")
    soup = BeautifulSoup(url.text, "lxml")
    table = soup.find("table", {"class": "wikitable sortable"})
    df = pd.DataFrame(pd.read_html(str(table))[0])

    politician_names = df.get("Nombre y apellidos").to_list()
    for idx, pol in enumerate(politician_names):
        surname, name = pol.split(",")
        politician_names[idx] = f"{name} {surname}".strip()

    parties = df.get("Lista.1").to_list()

    politicians = list(zip(politician_names, parties))
    parties = set(parties)

    return politicians, parties


def tweets_parser(df, parameters: dict, session):
    DetectorFactory.seed = 69420  # Seed for the language detector (deterministic)

    parse_hashtag_func, labels_dict = set_parameters(session, parameters)

    # Parallelize parsing tweets
    with ProcessPoolExecutor(max_workers=cpu_count()) as pool:
        futures = [
            pool.submit(
                parse_tweet,
                tweet, parse_hashtag_func,
                mention_replaces=labels_dict
            )
            for tweet in df.text
        ]

    parsed_tweets = []
    for idx, future in enumerate(futures):
        result = future.result()
        if result:
            parsed_tweets.append((df.text[idx], result, df.favs[idx], df.retweets[idx], df.author[idx], df.party[idx]))

    # Create a Pandas Dataframe to store the information of each tweet and its parsed version
    tweets_df = pd.DataFrame(
        parsed_tweets,
        columns=["Original Tweets", "Parsed Tweets", "Likes", "Retweets", "Author", "Party"]
    )
    return tweets_df


def parse_tweet(tweet, parse_hashtag_func, mention_replaces):
    """
    Parallelized function called by ProcessPoolExecutor for parsing tweets
    :param tweet: Politician tweet
    :param parse_hashtag_func: Hashtag parsing function
    :param mention_replaces: Labels dictionary for substituting parties and/or politicians
    :return: Parsed tweet
    """
    tweet = remove_urls(tweet)
    if not is_spanish(tweet):
        return None

    parsed_tweet = []
    for word in tweet.split(" "):
        word = replace_user_in_dict(remove_full_stop_and_commas(word), TR_MAIN_PARTIES, remove_word=False)
        if "@" in word:
            # replace twitter usernames by party or politician names
            word = remove_full_stop_and_commas(remove_at_sign(word)).lower()
            word = replace_user_in_dict(word, mention_replaces, remove_word=True)
        if "#" in word:
            word = parse_hashtag_func(word)
        if word:
            parsed_tweet.append(word)

    return " ".join(parsed_tweet)


def replace_user_in_dict(word, replace_dict, remove_word=True):
    """
    :param word: Tweet word
    :param replace_dict: Politicians and parties dict
    :param remove_word: True if the word is removed when not found in dictionary
    :return: Parsed politician or empty string if politician not found
    """
    replace = '' if remove_word else word
    return replace_dict.get(word, replace)


def is_spanish(text):
    """
    :param text: String of text (whole tweet)
    :return: True if text in Spanish else False
    """
    parsed_text = remove_numbers(remove_symbols(text, add_space=True))
    return detect(parsed_text) == 'es' if parsed_text else False


def set_parameters(session, parameters: dict):
    """
    :param session: SQLAlchemy session
    :param parameters: Dictionary of parameters for the hashtag parsing and party/politician substitution
    :return: Hashtag parsing function and labels dictionary
    """
    politicians_twitters = get_politicians_twitter_dict(session)
    parse_hashtag_func = remove_hashtag_word if parameters["remove_hashtag_word"] else remove_hashtag

    labels_dict = {}
    if parameters["replace_politicians"]:
        labels_dict.update(politicians_twitters)
    if parameters["replace_parties"]:
        labels_dict.update(PARTIES_TWITTERS)

    return parse_hashtag_func, traverse_dict(labels_dict)


def remove_urls(text):
    return re.sub(r'http\S+', '', text.replace('\n', '')).strip()


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
