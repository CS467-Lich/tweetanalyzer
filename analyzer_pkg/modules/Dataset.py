"""
This file defines the Dataset class which loads our data from file(s), cleans
it according to our advanced settings, and vectorizes the text.
"""

import json
import unicodedata
import re
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2

class Dataset:
	def __init__(self, data_folder, files, vectorizer='count', 
				 remove_stopwords=True, preserve_symbols=True):
		""" Initializes Dataset object.

		Arguments:
			data_folder (string) = subfolder in program working directory
				where the data files are located.
			files (dict) = keys are string category names, values are string
				file names (JSON) where that category's tweets are located in
				data_folder.
			 vectorizer (string) = 'count' or 'tfidf'
			 remove_stopwords (bool) = whether or not to remove stopwords when
			 	vectorizing with scikit
			 preserve_symbols (bool) = whether or not to keep "#" and "@" in
			 	tweet text
		"""

		# File Origin
		if data_folder.endswith("/"):
			self.data_folder = data_folder
		else:
			self.data_folder = data_folder + "/"
		self.files = files

		# Vectorizer type
		if vectorizer.lower() == 'tfidf':
			self.vectorizer = 'TfidfVectorizer'
		else:
			self.vectorizer = 'CountVectorizer'
		
		# Remove Stopwords
		self.remove_stopwords = remove_stopwords

		# Preserve #s and @s
		self.preserve_symbols = preserve_symbols

		# To be added later...
		self.labels = []
		self.vocabulary = {}
		self.data = {
			'x_str': [],
			'y': []
		}
		self.train = None
		self.test = None
		self.feature_count = None
		self.correlated_features = None

	def _checkFileContents(self, fileData, filepath):
		"""Checks that the fileData from filepath contains, at minimum, 'text' 
		keys.

		Arguments:
		fileData -- (dictionary) A dictionary parsed from a JSON file
		filepath -- (string) The file fileData was pulled from
		"""

		try: 
			keys = list(fileData.keys())
			assert 'text' in keys
		
		except AssertionError:
			msg = ("(Dataset_checkFileContents) Error: '{}' is missing a key"
				   "called 'text'.").format(filepath)
			raise ValueError(msg)

	def load(self):
		""" Loads data from each item in self.files (dict with category names as
		keys and corresponding file names as values) in self.data_folder 
		(string).

		Outcomes:
		1. Saves array of tweet text from all files to self.data['x_str']
		2. Saves corresponding array of category codes to self.data['y'].
		   Both self.data['x_str'] and self.data['y'] are the same length;
		   self.data['x_str'][someIndex] has the category code stored at
		   self.data['y'][someIndex].
		3. Saves category names in the array self.labels. The index of the 
		   category in the array (0..num categories - 1) is the category's
		   integer code. 

		Prerequisites:
		Expects each file to contain tweets belonging to only one category. 
		"""
		for idx, category in enumerate(self.files):
			self.labels.append(category)

			if self.files[category]:
				filepath = self.data_folder + self.files[category]
				try:
					file = open(filepath)
					fileData = json.load(file)
					file.close()
				except IOError:
					msg = ("(Dataset.load) Error: Couldn't open {0}. Are you "
						   "sure the file exists?").format(filepath)
					raise IOError(msg)
				except json.decoder.JSONDecodeError:
					file.close()
					msg = ("(Dataset.load) Error: {0} is not formatted for "
						   "JSON parsing.").format(filepath)
					raise ValueError(msg)
				
				self._checkFileContents(fileData, filepath)

				self.data['x_str'].extend(fileData['text'])					

				catlist = [idx] * len(fileData['text'])
				self.data['y'].extend(catlist)

	def load_csv(self):
		""" Loads data from self.files[keys[0]] (string) in self.data_folder 
		(string).

		Outcomes:
		1. Saves array of tweet text from all files to self.data['x_str']
		2. Saves corresponding array of category codes to self.data['y'].
		   Both self.data['x_str'] and self.data['y'] are the same length;
		   self.data['x_str'][someIndex] has the category code stored at
		   self.data['y'][someIndex].
		3. Saves category names in the array self.labels. The index of the 
		   category in the array (0..num categories - 1) is the category's
		   integer code. 

		Prerequisites:
		Expects self.files to contain one key and the value corresponding to
		that key to be the name of a file that can be parsed as a CSV.
		"""

		# Input training data into a dataframe
		file = self.files[list(self.files.keys())[0]]
		path = self.data_folder + file
		try:
			df = pd.read_csv(path)
		except Exception:
			msg = ("(Dataset.load_csv) Error: Couldn't open {0}. Are you "
				   "sure the file exists?").format(path)
			raise IOError(msg)

		# Create a subset of data that includes our text and category because 
		# this algorithm will be learning based off of those two data points.
		col = ['text', 'Category']
		df = df[col]
		df.columns = ['text', 'Category']
		
		# Turn categories into numerical IDs
		df['category_id'] = df['Category'].factorize()[0]

		self.data['x_str'] = df['text'].tolist()
		self.data['y'] = df['category_id'].tolist()

		# Convert dataframe to list
		category_id_df = df[['Category','category_id']].drop_duplicates().sort_values('category_id')
		labels = category_id_df['Category'].tolist()
		self.labels = labels

	def clean(self):
		""" Scikit has its own punctuation cleaning process that we can use if
		we want to strip ALL punctuation. clean() doesn't do anything but remove
		periods if this is the case-- it leaves the good stuff for scikit to
		do. 
		However, it's difficult to make scikit's tokenizer preserve some symbols
		like '#' and '@' and not others; it treats every non-character symbol as
		a token seperator by default. Therefore, if we want to preserve some of 
		the punctuation, we probably want to clean our tweets ourselves.

		Outcomes:
			self.data['x_str'] is cleaned of punctuation depending on the value
				of self.preserve_symbols.
		"""

		# This might seem overkill, but I'm removing periods instead of 
		# replacing them with spaces to preserve abbreviations like "U.S.A." or
		# "U.N." If we replace periods with spaces, these abbreviations get
		# totally broken up and won't get included in the vocabulary by our
		# tokenizer.
		for idx, text in enumerate(self.data['x_str']):
			legend = {'.': None}
			self.data['x_str'][idx] = text.translate(str.maketrans(legend))
			if self.preserve_symbols:
				# Normalize text by converting characters like é to e and 
				# changing to all lowercase
				normText = unicodedata.normalize('NFKD', self.data['x_str'][idx]).lower()
				cleanText = re.sub(r"[^a-zA-Z0-9@#]", " ", normText)
				self.data['x_str'][idx] = cleanText

	def split(self, percent_test, seed=None):
		""" Splits the data in self.data into a training set and a test. Divided
		set is returned as lists self.train and self.test.

		Arguments: 
			percent_test (float) = value between 0 and 1 representing the
				proportion of the dataset to include in the test split; the size
				of the train split is 1 - percent_test.
			seed (int) = if included, the same seed can be used to replicate the
				same test split in the future.

		"""
		data = pd.DataFrame.from_dict(self.data)
		params = {
			'test_size': percent_test,
			'shuffle': True,
			'random_state': None
		}
		if seed: params['random_state'] = seed
		self.train, self.test = train_test_split(data, **params)

	def vectorize(self, ngram_range):
		""" Uses the specified ngram_range and the vectorizer in self.vectorizer
		to appropriately vectorize the data in self.train.x_str and 
		self.test.x_str. Saves the result as self.train_x_vect and
		self.test_x_vect. For uniformity, copies self.train.y and self.test.y to
		self.train_y and self.test_y. This is kind of messy, but I had
		difficulties adding a new column to self.test and self.train. Also
		savees the vectorizer's vocabulary to self.vocabulary and a dict of
		each category's most correlated features to self.correlated_features.

		Arguments:
			ngram_range = tuple of two ints; expects tuple[0] <= tuple[1]
		"""
		params = {
			'ngram_range': ngram_range,
			'strip_accents': None,
			'analyzer': 'word',
			'token_pattern': r'(?u)\S\S+',
			'lowercase': False,	#no use re-doing this if it's been done
			'stop_words': None
		}
		if self.remove_stopwords:
			params['stop_words'] = 'english'
		if not self.preserve_symbols:
			params['strip_accents'] = 'ascii'
			params['lowercase'] = True
			del params['token_pattern']

		if self.vectorizer == 'TfidfVectorizer':
			vect = TfidfVectorizer(**params)
		else:
			vect = CountVectorizer(**params)

		self.train_x_vect = vect.fit_transform(self.train.x_str)
		self.train_y = list(self.train.y)
		self.feature_count = self.train_x_vect.shape[1]
		self.test_x_vect = vect.transform(self.test.x_str)
		self.test_y = list(self.test.y)
		self.vocabulary = vect.vocabulary_

		# Save the most-correlated features for each category within the ngram 
		# range.
		self.correlated_features = {}
		for cat_id, category in enumerate(self.labels):
			features_chi2 = chi2(self.train_x_vect, np.array(self.train_y) == cat_id)
			indices = np.argsort(features_chi2[0])
			feature_names = np.array(vect.get_feature_names())[indices]
			self.correlated_features[category] = {}
			for n in range(ngram_range[0], ngram_range[1] + 1):
				self.correlated_features[category][n] = \
					[v for v in feature_names if len(v.split(' ')) == n]

	def dump_vocabulary(self, filepath):
		""" Saves self.vocabulary in JSON notation to file at specified path.
		"""
		fp = open(filepath, 'w+')
		json.dump(pd.Series(self.vocabulary).to_dict(), fp, indent=4)
		fp.close()