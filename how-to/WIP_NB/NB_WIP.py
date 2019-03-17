'''
Naive Bayes Implementation
Sandhya Raman

'''

import numpy as np
import configparser
import pandas as pd
import sys

from io import StringIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text 
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score


'''

Use user input from config.ini file


'''

config = configparser.ConfigParser()
config.read('config.ini')


#Set variables for the vectorizer
if (config['DATASET PROCESSING']['Vectorizer'] == 'count') or (config['DATASET PROCESSING']['Vectorizer'] == 'Count') or (config['DATASET PROCESSING']['Vectorizer'] == 'COUNT'):
	nb_Vect = 'countvect'
elif (config['DATASET PROCESSING']['Vectorizer'] == 'tfidf') or (config['DATASET PROCESSING']['Vectorizer'] == 'Tfidf') or (config['DATASET PROCESSING']['Vectorizer'] == 'TFIDF'):
	nb_Vect = 'tfidf'
else:
	print("Please use the configuration file to choose a valid vectorizer.")
	sys.exit()


#Set variables for stopwords
if config['TEXT PROCESSING'].getboolean('Remove Stopwords') == True:
	nb_Stopwords = text.ENGLISH_STOP_WORDS

else:
	nb_Stopwords = None


#Set varaibles for symbols
if config['TEXT PROCESSING'].getboolean('Keep # and @ Symbols') == True:
	nb_Symbols = r"[^a-zA-Z0-9@#]"

else:
	nb_Symbols = 0


#Set variables for test/train split
values_list = [int(str_val) for str_val in config['DATASET PROCESSING']['Test-Train Split'].split(',')]
if values_list[0] + values_list[1] != 100:
	print("Please use the configuration file to choose a valid test-train split.")
	sys.exit()
else:
	nb_Test = values_list[0]/100
	nb_Train = values_list[1]/100


'''


Other Variables
Not set by user


'''

nb_Min = 1
nb_Max = 3


'''


Prepare the data for the NB algorithm


'''

#Input training data into a dataframe
df = pd.read_csv('All_Positive.csv')
df.head()

#Create a subset of data that includes our text and category because this algorithm will be learning based off of those two data points
col = ['text', 'category']
df = df[col]
df.columns = ['text', 'category']

#Turn categories into numerical IDs
df['category_id'] = df['category'].factorize()[0]

#Convert dataframe to dict
category_id_df = df[['category','category_id']].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'category']].values)

#Create a tfidf vector for each text entry in our data set
if nb_Vect == 'tfidf':
	tfidf = TfidfVectorizer(sublinear_tf=True, min_df=1, norm='l2', encoding='latin-1', ngram_range=(nb_Min,nb_Max), stop_words=nb_Stopwords)
	features = tfidf.fit_transform(df.text).toarray()
else:
	tfidf = CountVectorizer(min_df=1, encoding='latin-1', ngram_range=(nb_Min,nb_Max), stop_words=nb_Stopwords)
	features = tfidf.fit_transform(df.text).toarray()

labels = df.category_id
features.shape

#Correlate words to categories
N = 2
for category, category_id in sorted(category_to_id.items()):
	features_chi2 = chi2(features, labels == category_id)
	indices = np.argsort(features_chi2[0])
	feature_names = np.array(tfidf.get_feature_names())[indices]
	unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
	bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
	#print("# '{}':".format(Category))
  	#print(".Most correlated unigrams:\n.{}".format('\n.'.join(unigrams[-N:])))
  	#print(".Most correlated bigrams:\n . {}".format('\n.'.join(bigrams[-N:])))


'''

Data is used to train the algorithm


'''

#Split data set into training data and testing data for NB algorithm
#train_test_split does shuffle on default
#test_size gets set automatically to compliment the train_size if not specified

X_train, X_test, y_train, y_test = train_test_split(df['text'], df['category'], train_size = nb_Train, test_size = nb_Test, random_state = 0)
if nb_Symbols == 0:
	count_vect = CountVectorizer(min_df=1, encoding='latin-1', ngram_range=(nb_Min,nb_Max), stop_words=nb_Stopwords)
else:
	count_vect = CountVectorizer(min_df=1, encoding='latin-1', ngram_range=(nb_Min,nb_Max), analyzer = 'word', token_pattern = nb_Symbols, stop_words=nb_Stopwords)

X_train_counts = count_vect.fit_transform(X_train)

#CountVectorizer() and TfidfTransformer() is equivalent to TfidfVectorizer()
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)


mlb = MultinomialNB().fit(X_train_tfidf, y_train)
cmlb = MultinomialNB().fit(X_train_counts, y_train)


X_test_counts = count_vect.transform(X_test)
X_test_tfidf = tfidf_transformer.transform(X_test_counts)

y_mlb_predicted = mlb.predict(X_test_tfidf)
y_cmlb_predicted = cmlb.predict(X_test_counts)

if nb_Vect == "tfidf":
	mb_accuracy = accuracy_score(y_test, y_mlb_predicted)
	print("NB Accuracy: ", mb_accuracy)

if nb_Vect == "countvect":
	cmb_accuracy = accuracy_score(y_test, y_cmlb_predicted)
	print("NB Accuracy: ", cmb_accuracy)


'''

Resources


'''
#https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html#sphx-glr-auto-examples-text-plot-document-classification-20newsgroups-py
#https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
#https://datascience.stackexchange.com/questions/29352/sklearn-countvectorizer-token-pattern-skip-token-if-pattern-match
#https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples-649dc1c3f285
#https://stackoverflow.com/questions/26826002/adding-words-to-stop-words-list-in-tfidfvectorizer-in-sklearn
#https://docs.python.org/3/library/configparser.html
#https://stackoverflow.com/questions/44535228/read-a-comma-separated-ini-file-in-python
#https://towardsdatascience.com/machine-learning-nlp-text-classification-using-scikit-learn-python-and-nltk-c52b92a7c73a
#https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f