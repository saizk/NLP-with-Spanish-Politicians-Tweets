


##################################################################################################################
#                           LDA                                                                                 #
##################################################################################################################
# Linux installation for MALLET, I need it in Windows
# !wget http://mallet.cs.umass.edu/dist/mallet-2.0.8.zip
# !unzip mallet-2.0.8.zip

# Setting shit for Java
# os.environ['MALLET_HOME'] = 'mallet-2.0.8'
# mallet_path = 'mallet-2.0.8/bin/mallet' # you should NOT need to change this


# After having obtained the BOW mycorpus_bow, we use it to compute LDA
# from gensim.models.wrappers import LdaMallet
# ldamallet = LdaMallet(mallet_path, corpus=train_corpus_bow, num_topics=20, id2word=D, alpha=5, iterations=100)

# Once we have the LDA vectors ldamallet
# train_vecs = []
#EJEMPLO DE CODIGO PARA PODER SACAR EL DATASET PARA CLASIFICATION
# for i in range(len(my_dataframe)):
#     top_topics = ldamallet.get_document_topics(train_corpus[i], minimum_probability=0.0)
#     lda_topics_vector = [top_topics[i][1] for i in range(number_of_topics)]
#     lda_topics_vector.extend([my_dataframe.iloc[i].favs])  # count of favs
#     lda_topics_vector.extend([len(my_dataframe.iloc[i].retweets)])  # count of retweets
#     train_vecs.append(topic_vec)


# train_vecs = [------------------------------LDA VECTOR----------------------------------------------------, FAVS ,  RTS, LABEL]
# train_vecs = [0.00012,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334, 0.5132, 0.1401289, ... , 19822, 2197, PSOE ]
# train_vecs = [0.00012,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334, 0.5132, 0.1401289, ... , 19822, 2197, PSOE ]
# train_vecs = [0.00012,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334, 0.5132, 0.1401289, ... , 19822, 2197, PSOE ]
# train_vecs = [0.00012,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334, 0.5132, 0.1401289, ... , 19822, 2197, PSOE ]
# train_vecs = [0.00012,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334, 0.5132, 0.1401289, ... , 19822, 2197, PSOE ]


##################################################################################################################
#                          TFIDF                                                                                 #
##################################################################################################################

# After having obtained the BOW mycorpus_bow, we use it to compute TFIDF
# from gensim.corpora import Dictionary
# from gensim import models
#
# D = Dictionary(docs)
# corpus_bow = [D.doc2bow(doc) for doc in docs]
#
# tfidf = models.TfidfModel(corpus_bow)
# corpus_tfidf = tfidf[corpus_bow]

# train_vecs = [------------------------------TFIDF VECTOR----------------------------------------------------, FAVS ,  RTS, LABEL]
# train_vecs = [0.00012,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334, 0.5132, 0.1401289, ... ,   19822, 2197, PSOE ]
# train_vecs = [0.00012,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334, 0.5132, 0.1401289, ... ,   19822, 2197, PSOE ]
# train_vecs = [0.00012,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334, 0.5132, 0.1401289, ... ,   19822, 2197, PSOE ]
# train_vecs = [0.00012,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334, 0.5132, 0.1401289, ... ,   19822, 2197, PSOE ]
# train_vecs = [0.00012,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334,0.0033334, 0.5132, 0.1401289, ... ,   19822, 2197, PSOE ]

