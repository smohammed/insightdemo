import os
import re
import json
import pickle
import nltk
import numpy as np
import pandas as pd
import string
import random
import codecs
from operator import itemgetter
from collections import OrderedDict
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer 


exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
# Load trained LDA model
lda_fp = open("lda_model_beers.pkl", 'rb')
ldamodel = pickle.load(lda_fp)
 
# Load the beers corpus to choose 500 lines for test purpose
docs_fp = open("docs_beers.pkl", 'rb')
docs_all = pickle.load(docs_fp)
docs_test = docs_all[1000:].reset_index(drop=True)


def pre_process(text):
    # lowercase
    text=text.lower()
    #remove tags
    text=re.sub("<!--?.*?-->","",text)
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
    return text

def clean(doc):
    stop = set(stopwords.words('english'))
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    normalized = " ".join(lemma.lemmatize(word,'v') for word in stop_free.split())
    x = normalized.split()
    y = [s for s in x if len(s) > 2]
    return y

def cluster_similar_documents(corpus, dirname):
    clean_docs = [clean(doc) for doc in corpus]
    test_term = [ldamodel.id2word.doc2bow(doc) for doc in clean_docs]
    doc_topics = ldamodel.get_document_topics(test_term, minimum_probability=0.20)
    for k,topics in enumerate(doc_topics):
        if topics:
            topics.sort(key = itemgetter(1), reverse=True)
            dir_name = dirname + "/" + str(topics[0][0])
            file_name = dir_name + "/" + str(k) + ".txt"
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            fp = open(file_name,"w")
            fp.write(docs_test[k] + "\n\n" + str(topics[0][1]) )
            fp.close()
        else:
            if not os.path.exists(dirname + "/unknown"):
                os.makedirs(dirname + "/unknown")
            file_name = dirname + "/unknown/" + str(k) + ".txt"
            fp = open(file_name,"w")
            fp.write(docs_test[k])

def get_related_documents(term, top, corpus):
    clean_docs = [clean(doc) for doc in corpus]
    related_docid = []
    test_term = [ldamodel.id2word.doc2bow(doc) for doc in clean_docs]
    doc_topics = ldamodel.get_document_topics(test_term, minimum_probability=0.30)
    term_topics =  ldamodel.get_term_topics(term, minimum_probability=0.000001)
    for k,topics in enumerate(doc_topics):
        if topics:
            topics.sort(key = itemgetter(1), reverse=True)
            if topics[0][0] == term_topics[0][0]:
                related_docid.append((k,topics[0][1]))
 
    related_docid.sort(key = itemgetter(1), reverse=True)
    for j,doc_id in enumerate(related_docid):
        print('')
        #print(doc_id[1],"\n\n",docs_test[doc_id[0]])
        if j == (top-1):
            break
    return doc_id[0]

def getabeer(keyword):
    beers = pd.read_csv('beerlist.csv')
    beers = beers[:2000]

    beers['words'] = beers['words'].apply(lambda x:pre_process(x))
    for i in range(len(beers)):
        beers['words'][i] = beers['words'][i].split()
        try:
            beers['words'][i] = random.sample(beers['words'][i], 2000)
        except ValueError:
            beers['words'][i] = random.sample(beers['words'][i], len(beers['words'][i]))
        beers['words'][i] = ' '.join(beers['words'][i])

    # initialize WordNetLemmatizer and get the list of english stop words
    stop = set(stopwords.words('english'))
    lemma = WordNetLemmatizer()

    # Get 'top' related documents given a word(term)
    a = get_related_documents(keyword, 1 , docs_test)
    # performs document clustering given a set of documents
    #cluster_similar_documents(docs_test,"root")

    return beers['name'][a+1000]

#getabeer('asdf', 'lager')
