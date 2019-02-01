"""
Turn data.json into a vectorized array of words, also known as a Bag of Words
Cord Meados 2019
"""

import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_json('data.json',orient='values')
print(df.head())


# https://stackoverflow.com/questions/48806010/bag-of-words-with-json-array