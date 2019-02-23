"""
WIP, will clean up/refactor
-Emily
"""
import pandas as pd
import re
import unicodedata
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
REMOVE_STOPWORDS = False 	# NOTE: REMOVE_STOPWORDS=True takes more time.
if REMOVE_STOPWORDS:
	import nltk
	nltk.download('stopwords')
	from nltk.corpus import stopwords
from stitch_funcs import stitch

# This can all be done (probably better) using Scikit-learn, but I thought to
# try implementing it myself.
def cleanPunctuation(data):
	for idx, tweet in enumerate(data['tweet']):
		# Normalize text by converting characters like é to e and 
		# changing to all lowercase
		normText = unicodedata.normalize('NFKD', tweet).lower()
		# Replace most punctuation and symbols with a space
		cleanPunc = re.sub(r"[^a-zA-Z0-9'’.,@#]", " ", normText)

		# To-do: Would be interesting to see if there is a difference in 
		# prediction accuracy based on whether or not stopwords are included?
		if REMOVE_STOPWORDS:
			# Standardize apostrophes-- nltk knows what to do with them; nix 
			# periods and commas
			legend = { "’" : "'", "." : None, "," : None }
			cleanerPunc = cleanPunc.translate(str.maketrans(legend))
			# Remove stopwords -- this takes time, so should probably be
			# improved somehow.
			words = cleanerPunc.split()
			goodWords = [w for w in words if not w in stopwords.words("english")]
			data['tweet'][idx] = " ".join(goodWords)

		else:
			# Nix apostrophes, periods, and commas
			legend = { "'": None, "’" : None, "." : None, "," : None }
			cleanerPunc = cleanPunc.translate(str.maketrans(legend))
			data['tweet'][idx] = cleanerPunc


"""
DATA_FOLDER = 'Unit_Test_Files/'
FILES = {
	'Activism': 'activism_test.json',
	'Advertisement': 'ads_test.json',
	'Fitness': 'fitness_test.json',
	'Humor': 'humor_test.json',
	'Political': 'political_test.json',
	'Technology': 'tech_test.json'	
}
"""

DATA_FOLDER = 'Final_Positives/'
FILES = {
	'Activism': 'Activism_Final_Positive.json',
	'Advertisement': 'Ads_Final_Positive.json',
	'Fitness': None, # Need to convert this one from csv to json
	'Humor': 'Humour_Final_Positive.json',
	'Political': 'Political_Final_Positive.json',
	'Technology': 'Tech_Final_Positive.json'
}

combinedData, legend = stitch(DATA_FOLDER, FILES)
print("Category Legend:")
print(legend)
cleanPunctuation(combinedData)
data = pd.DataFrame.from_dict(combinedData)

# Check data
print("\nCOMBINED DATA...")
print("(Qty data items, Qty columns)", data.shape)
print("Column Names: ", data.columns.values)
print(data.head(5))
print(data.tail(5))

# Split dataframe into training and test data (90% goes to training, 10% goes
# to test-- can experiment with proportions)
train, test = train_test_split(data, test_size=0.1, shuffle=True)

print("\nTRAINING DATA...")
print("(Qty data items, Qty columns)", train.shape)
print("Column Names: ", train.columns.values)

print("\nTEST DATA...")
print("(Qty data items, Qty columns)", test.shape)
print("Column Names: ", test.columns.values)

# Transform training data using CountVectorizer.
print("\nTRANSFORMING TEST DATA USING COUNTVECTORIZER...")
count_vect = CountVectorizer(ngram_range=(1,2))
train_x_vect = count_vect.fit_transform(train.tweet)
print("len(train.tweet) =", len(list(train.tweet)))
print("(numDocuments, numUniqueWords):", train_x_vect.shape)

# Save vocabulary to file for later inspection.
# Encountered type errors related to Numpy data types when trying to save to
# file using just json.dump(), so I tried converting to a DataFrame. I still
# got an error, so I used a solution from
# https://stackoverflow.com/questions/17839973/constructing-pandas-dataframe-from-values-in-variables-gives-valueerror-if-usi
# to get the below line.
corpus_df = pd.Series(count_vect.vocabulary_).to_frame()
corpus_df.to_json(path_or_buf='vocabulary.json')

# Check the vocabulary_ built from our training data
print("\nTESTING FEATURE INDICES IN VOCABULARY...")
print("\nSome features that are almost certainly in the corpus...")
found_features = ['trump', 'democrats', 'ad', 'global warming',
					'the president', 'climate']
for feature in found_features:
	feature_index = count_vect.vocabulary_.get(feature)
	if feature_index == None: 
		feature_index = 'Not found'
	print("%s: %s" % (feature, feature_index))

print("\nSome features we know are NOT in the corpus...")
missing_features = ['anboir', 'dkdk tututx', 'riirrrrg']
for feature in missing_features:
	feature_index = count_vect.vocabulary_.get(feature)
	if feature_index == None: 
		feature_index = 'Not found'
	print("%s: %s" % (feature, feature_index))

# Transform test data using CountVectorizer.
test_x_vect = count_vect.transform(test.tweet)

# Initialize Logistic Regression instance. We can test different solvers to see
# which is the most effective on our dataset. I believe we need to use a 
# multiclass='multinomial' setting for our problem per the following:
# https://scikit-learn.org/stable/modules/multiclass.html
LR = LogisticRegression(solver='lbfgs', multi_class='multinomial')
train_y = list(train.category) 	# Not strictly necessary, but I found having x 
								# and y variables helpful
LR.fit(train_x_vect, train_y)

# Predict values for test data
predicted = LR.predict(test_x_vect)

"""
for tweet, category in zip(test.tweet, predicted):
	print('%r => %d: %s' % (tweet, category, legend[category]))
"""

test_y = test.category
score = LR.score(test_x_vect, test_y)
print("\nPercent of Test Tweets Accurately Categorized:", score * 100)

# Sources:
# https://www.kaggle.com/c/word2vec-nlp-tutorial#part-1-for-beginners-bag-of-words
# http://fastml.com/classifying-text-with-bag-of-words-a-tutorial/