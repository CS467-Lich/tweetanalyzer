from io import StringIO
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

#Get input from user so they can interact with the NB algorithm
print("This algorithm will categorize a Twitter tweet into one of the following categories: advertisement, comedy, politics, environmentalism, fitness, and technology. Test by typing in a scentence.")
tweettext = input("Your tweet: ")

#Input training data into a dataframe
df = pd.read_csv('All_Positive.csv')
df.head()

#Create a subset of data that includes our text and category because this algorithm will be learning based off of those two data points
col = ['text', 'category']
df = df[col]
df.columns = ['text', 'category']

#Turn categories into numerical IDs
#pandas.factorize(values, sort=False, order=None, na_sentinel=-1, size_hint=None)
df['category_id'] = df['category'].factorize()[0]

#Convert dataframe to dict
category_id_df = df[['category','category_id']].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'category']].values)

#Create a tfidf vector for each text entry in our data set

#class sklearn.feature_extraction.text.TfidfVectorizer(input=’content’, encoding=’utf-8’, decode_error=’strict’, strip_accents=None, lowercase=True, 
#preprocessor=None, tokenizer=None, analyzer=’word’, stop_words=None, token_pattern=’(?u)\b\w\w+\b’, ngram_range=(1, 1), max_df=1.0, min_df=1, max_features=None, 
#vocabulary=None, binary=False, dtype=<class ‘numpy.float64’>, norm=’l2’, use_idf=True, smooth_idf=True, sublinear_tf=False)

#source: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=1, norm='l2', encoding='latin-1', ngram_range=(1,2), stop_words='english')

features = tfidf.fit_transform(df.text).toarray()
labels = df.category_id

#########
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
  	#print("  . Most correlated bigrams:\n . {}".format('\n.'.join(bigrams[-N:])))

#Split data set into training data and testing data for NB algorithm
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['category'], random_state = 0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

clf = MultinomialNB().fit(X_train_tfidf, y_train)

#print(clf.predict(count_vect.transform(["I feel like I need to work on my core strength."])))
print(clf.predict(count_vect.transform([tweettext])))


#Resources
#https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html#sphx-glr-auto-examples-text-plot-document-classification-20newsgroups-py
