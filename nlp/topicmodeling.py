import spacy
import pandas as pd
from spacy.lang.es.examples import sentences
from gensim.models.phrases import Phrases
from gensim.corpora import Dictionary
from sklearn.model_selection import train_test_split
from pprint import pprint


def nlp_pipeline(tweets: list, gpu: bool = False):
    if gpu:
        nlp = spacy.load('es_dep_news_trf')
    else:
        nlp = spacy.load('es_core_news_md')

    # nlp.disable_pipe('parser')
    nlp.disable_pipe('ner')

    valid_pos = set(['VERB', 'NOUN', 'ADJ', 'PROPN'])

    train, test = train_test_split(tweets, train_size=.2)

    tweets = train
    tokens = get_tokens(tweets, nlp, valid_pos)
    pprint(tokens)

    tweets_lemmas = get_lemmas(tweets, nlp, valid_pos)
    pprint(tweets_lemmas)
    tweets_df = pd.DataFrame(tweets, tweets_lemmas)
    print(tweets_df)
    # lemmas_threshold =
    # tweets_df = tweets_df[tweets_df['nlemmas'] >= lemmas_threshold]


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


# 2. BAG OF WORDS REPRESENTATION
#
# tweets_corpus = tweets_df.lemmas.tolist()
# tweets_corpus = list(set(tweets_corpus))
# tweets_corpus = [el.split() for el in tweets_corpus]
#
# # N-GRAM detection and replacement
# """
# As we have previously pre-processed the corpus with spacy, a very simple N-Gram detection
# will be performed.
# """
#
# phrase_model = Phrases(tweets_corpus, min_count=2, threshold=20)
# tweets_corpus = [el for el in phrase_model[tweets_corpus]]
#
# # Token dictionary
#
# token_dic = Dictionary(tweets_corpus)
#
# # Filter token dictionary
# no_below = 5  # Minimum number of documents to keep a term in the dictionary
# no_above = .4  # Maximum proportion of documents in which a term can appear to be kept in the dictionary
#
# # BOW: Transform list of tokens into list of tuples (token id, token # of occurrences)
# tweets_corpus_bow = [token_dic.doc2bow(doc) for doc in tweets_corpus]
#
# # 3. INITIAL TOPIC MODEL
