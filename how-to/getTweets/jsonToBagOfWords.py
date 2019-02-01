"""
Turn data.json into a vectorized array of words, also known as a Bag of Words
Cord Meados 2019
"""

import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

# Load the data to a pandas dataframe object
df = pd.read_json('data.json', orient='values')

# Get some basic info, like an example row and the column headers
"""
print("\nFirst Row:")
print(df.head(1))
print("\n Column Headers:")
print(df.columns.values)
"""

# separate the text column for now.
textData = df['text']

# create a vectorizer and start preparing the data.
vectorizer = CountVectorizer()
vectorizer.fit(textData) # .fit() finds every unique word to create a word array
# print(vectorizer.vocabulary_) # getting a look at the data. Debug.
vector = vectorizer.transform(textData)
print(vector.shape)
print(type(vector))
print(vector.toarray())


# https://stackoverflow.com/questions/48806010/bag-of-words-with-json-array
# https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
# https://machinelearningmastery.com/prepare-text-data-machine-learning-scikit-learn/