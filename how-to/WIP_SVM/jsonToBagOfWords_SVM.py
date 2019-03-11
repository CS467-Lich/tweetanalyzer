"""
Turn data.json into a vectorized array of words, also known as a Bag of Words
Cord Meados 2019
"""

import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

def jsonToBagOfWords_SVM(filepath):
    # Load the data to a pandas dataframe object
    df = pd.read_json(filepath, orient='values')

    # separate the text column for now.
    textData = df['text']

    # create a vectorizer and start preparing the data.
    vectorizer = CountVectorizer(strip_accents='ascii', ngram_range=(1,2)) #playing around with ngram - we can definitely keep it simple and get rid of this
    return vectorizer.transform(textData)


# https://stackoverflow.com/questions/48806010/bag-of-words-with-json-array
# https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
# https://machinelearningmastery.com/prepare-text-data-machine-learning-scikit-learn/
