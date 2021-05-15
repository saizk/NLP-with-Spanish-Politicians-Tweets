import spacy
import pandas as pd


class NLPPipeline(object):

    def_pos = {'VERB', 'NOUN', 'ADJ', 'PROPN'}

    def __init__(self, tweets: pd.Series, valid_pos: set = None, parameters: dict = None, gpu: bool = False):

        if gpu:
            self.nlp = spacy.load('es_dep_news_trf')
        else:
            self.nlp = spacy.load('es_core_news_md')

        if parameters["disable_parser"]:
            self.nlp.disable_pipe('parser')
        if parameters["disable_ner"]:
            self.nlp.disable_pipe('ner')

        self.tweets = tweets
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