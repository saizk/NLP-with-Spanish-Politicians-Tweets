import spacy
import pandas as pd
from spacy.lang.es.examples import sentences
from gensim.models.phrases import Phrases
from gensim.corpora import Dictionary
from pprint import pprint


def nlp_pipeline(tweets_df: pd.DataFrame, gpu: bool = False):
    if gpu:
        nlp = spacy.load('es_dep_news_trf')
    else:
        nlp = spacy.load('es_core_news_md')

    # nlp.disable_pipe('parser')
    nlp.disable_pipe('ner')

    valid_pos = {'VERB', 'NOUN', 'ADJ', 'PROPN'}

    tweets = tweets_df["Parsed Tweets"]
    # tokens = get_tokens(tweets, nlp, valid_pos)
    # pprint(tokens)

    tweets_lemmas = get_lemmas(tweets, nlp, valid_pos)
    tweets_df["Lemmas"] = tweets_lemmas

    return tweets_df


def get_lemmas(tweets, nlp, valid_pos):
    return [text_preprocessing(nlp, tweet, valid_pos) for tweet in tweets]


def get_tokens(tweets, nlp, valid_pos):
    return [text_tokenizer(nlp, tweet, valid_pos) for tweet in tweets]


def text_preprocessing(nlp, rawtext, valid_pos):
    """
    Implements tokenization, lemmatization and stopword removal from an input raw string
    Returns the lemmatized string where lemmas are joined with a blank space
    """
    doc = nlp(rawtext)
    lemmatized = ' '.join([token.lemma_ for token in doc if
                           (token.is_alpha is True) and (token.pos_ in valid_pos) and (not token.is_stop)])
    return lemmatized


def text_tokenizer(nlp, rawtext, valid_pos):
    doc = nlp(rawtext)
    tokennized = ' '.join([token.text for token in doc if
                           (token.is_alpha is True) and (token.pos_ in valid_pos) and (not token.is_stop)])
    return tokennized
