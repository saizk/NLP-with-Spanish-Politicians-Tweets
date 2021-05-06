import spacy
import pandas as pd
from spacy.lang.es.examples import sentences


" [!] DEBERIAMOS TENER EN ESTE PUNTO YA EL CORPUS EN FORMATO .XML"

gpu = False
if gpu:
    nlp = spacy.load('es_dep_news_trf')
else:
    nlp = spacy.load('en_core_web_sm')


# 1. PRE-PROCESSING PIPELINE

"""
Since we are not interested in the syntactic relationship between words, but in the morphological study
of the content, we deactivate the parser option.
We will keep the Name Entity Recognition, since politicians are likely to mention this type of words.
"""

nlp.disable_pipe('parser')

# We will only keep words whose morphological category is one of these.
# The rest do not provide relevant information
valid_POS = set(['VERB', 'NOUN', 'ADJ', 'PROPN'])


def text_preprocessing(rawtext):
    """
    Implements tokenization, lemmatization and stopword removal from an input raw string
    Returns the lemmatized string where lemmas are joined with a blank space
    """
    doc = nlp(rawtext)
    lemmatized = ' '.join([token.lemma_ for token in doc if
                           (token.is_alpha == True) and (token.pos_ in valid_POS) and (not token.is_stop)])
    return lemmatized


tweets_content = sentences
tweets_lemmas = []

for tweet in tweets_content:
    tweets_lemmas.append(text_preprocessing(tweet))

"""
We have now transformed the raw text of the content of all the tweets into a list
of articles, which themselves contain a collection of the lemmas
"""


"""
[!]  OJO PIOJO GEOFFRENSES: AQUI TENEMOS QUE CALCULAR CUÁNTOS LEMMAS CONTIENE CADA TWEET PARA
HACER UN THRESHOLD MINIMO. NO ES NECESARIO PERO EL PROFE LO HACE Y LE GUSTARÁ.
"""

tweets_df = pd.DataFrame(" [!] dataframe con los lemmas y otros atributos, incluido el nlemmas"
                      "para iterar y poder sacar el threshold")

# lemmas_threshold =
tweets_df = tweets_df[tweets_df['nlemmas']>=lemmas_threshold]





# 2. BAG OF WORDS REPRESENTATION

tweets_corpus = tweets_df.lemmas.tolist()
tweets_corpus = list(set(tweets_corpus))
tweets_corpus = [el.split() for el in tweets_corpus]

# N-GRAM detection and replacement
"""
As we have previously pre-processed the corpus with spacy, a very simple N-Gram detection
will be performed.
"""
phrase_model = Phrases(tweets_corpus, min_count=2, threshold=20)
tweets_corpus = [el for el in phrase_model[tweets_corpus]]

# Token dictionary
token_dic = gensim.corpora.Dictionary(tweets_corpus)

# Filter token dictionary
no_below = 5 #Minimum number of documents to keep a term in the dictionary
no_above = .4 #Maximum proportion of documents in which a term can appear to be kept in the dictionary

# BOW: Transform list of tokens into list of tuples (token id, token # of occurrences)
tweets_corpus_bow = [token_dic.doc2bow(doc) for doc in tweets_corpus]



# 3. INITIAL TOPIC MODEL

