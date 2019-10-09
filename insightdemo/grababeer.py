import pandas as pd
import os
import pickle
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from operator import itemgetter
import os

# initialize WordNetLemmatizer and get the list of english stop words
stop = set(stopwords.words('english'))
lemma = WordNetLemmatizer()
 
# Load trained LDA model and lem beer words
lda_fp = open("insightdemo/lda_model_beers_14topics_allbeers.pkl", 'rb')
ldamodel = pickle.load(lda_fp)
docs_fp = open("insightdemo/docs_beers.pkl", 'rb')
docs_all = pickle.load(docs_fp)

allbeers = pd.read_csv('insightdemo/beerlist.csv')

# Function to remove stop words from sentences & lemmatize words.
def clean(beer):
	stop_free = " ".join([i for i in beer.lower().split() if i not in stop])
	normalized = " ".join(lemma.lemmatize(word,'v') for word in stop_free.split())
	x = normalized.split()
	y = [s for s in x if len(s) > 2]
	return y

def cluster_similar_documents(corpus, dirname):
	clean_beers = [clean(beer) for beer in corpus]
	test_term = [ldamodel.id2word.doc2bow(beer) for beer in clean_beers]
	beer_topics = ldamodel.get_document_topics(test_term, minimum_probability=0.20)
	for k,topics in enumerate(beer_topics):
		if topics:
			topics.sort(key = itemgetter(1), reverse=True)
			dir_name = dirname + "/" + str(topics[0][0])
			file_name = dir_name + "/" + str(k) + ".txt"
			if not os.path.exists(dir_name):
				os.makedirs(dir_name)
			fp = open(file_name,"w")
			fp.write(beers_test[k] + "\n\n" + str(topics[0][1]) )
			fp.close()
		else:
			if not os.path.exists(dirname + "/unknown"):
				os.makedirs(dirname + "/unknown")
			file_name = dirname + "/unknown/" + str(k) + ".txt"
			fp = open(file_name,"w")
			fp.write(beers_test[k])

def get_related_documents(term, top, corpus):
    clean_docs = [clean(doc) for doc in corpus]
    related_docid = []
    test_term = [ldamodel.id2word.doc2bow(doc) for doc in clean_docs]
    doc_topics = ldamodel.get_document_topics(test_term, minimum_probability=0.30)
    term_topics =  ldamodel.get_term_topics(term, minimum_probability=0.01)
    for k,topics in enumerate(doc_topics):
        if topics:
            topics.sort(key = itemgetter(1), reverse=True)
            try:
                if topics[0][0] == term_topics[0][0]:
                    related_docid.append((k,topics[0][1]))
            except IndexError:
                return print("Too specific or no match! Try again.")
    beerids = []
    related_docid.sort(key = itemgetter(1), reverse=True)
    for j,doc_id in enumerate(related_docid):
        #print(doc_id[1],"\n\n",docs_test[doc_id[0]])
        if j == (top-1):
            break
        beerids.append(doc_id[0])
    if len(beerids) > 0:
        return beerids #doc_id[0]
    else:
        return "Too specific or no match! Try again"

def getbeerrec(keyword):
	try:
		a = get_related_documents(keyword, 10 , docs_all)
	except IndexError:
		return "Too specific or no match! Try again."
	names = []
	breweries = []
	styles = []
	for i in a:
		names.append(allbeers['name'][i])
		breweries.append(allbeers['brewery'][i])
		styles.append(allbeers['style'][i])
	return [names, breweries, styles]