import spacy
import pandas as pd


class NLPTokenizer(object):

    def_pos = {'VERB', 'NOUN', 'ADJ', 'PROPN'}

    def __init__(self, raw_tweets: pd.DataFrame, valid_pos: set = None,
                 gpu: bool = False, disable_parser: bool = False, disable_ner: bool = False):

        if gpu:
            self.nlp = spacy.load('es_dep_news_trf')
        else:
            self.nlp = spacy.load('es_core_news_md')
        if disable_parser:
            self.nlp.disable_pipe('parser')
        if disable_ner:
            self.nlp.disable_pipe('ner')

        self.raw_tweets = raw_tweets
        self.tweets = self.raw_tweets["Parsed Tweets"]
        self.valid_pos = valid_pos if valid_pos else self.def_pos

    def get_lemmas(self):
        return [self.text_preprocessing(tweet) for tweet in self.tweets]

    def get_tokens(self):
        return [self.text_tokenizer(tweet) for tweet in self.tweets]

    def text_preprocessing(self, rawtext):
        """
        Implements tokenization, lemmatization and stopword removal from an input raw string
        Returns the lemmatized string where lemmas are joined with a blank space
        """
        doc = self.nlp(rawtext)
        lemmatized = ' '.join([token.lemma_ for token in doc if
                               (token.is_alpha is True) and (token.pos_ in self.valid_pos) and (not token.is_stop)])
        return lemmatized

    def text_tokenizer(self, rawtext):
        doc = self.nlp(rawtext)
        tokennized = ' '.join([token.text for token in doc if
                               (token.is_alpha is True) and (token.pos_ in self.valid_pos) and (not token.is_stop)])
        return tokennized
