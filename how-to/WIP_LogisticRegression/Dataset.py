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
	def __init__(self, data_folder, files, vectorizer='CountVectorizer', 
				 remove_stopwords=False, include_usernames=True, 
				 preserve_symbols='none'):
		# File Origin
		self.data_folder = data_folder
		if type(files) is not dict: 
			msg = "files arg must be a dictionary like { 'category': 'filename', ... }"
			raise TypeError(msg)
		self.files = files

		# Vectorizer type
		if vectorizer.lower() == 'tfidfvectorizer':
			self.vectorizer = 'TfidfVectorizer'
		else:
			self.vectorizer = 'CountVectorizer'
		
		# Remove Stopwords
		if type(remove_stopwords) is not bool:
			self.remove_stopwords = False
		else:
			self.remove_stopwords = remove_stopwords

		# Include Usernames
		if type(include_usernames) is not bool:
			self.include_usernames = True
		else:
			self.include_usernames = include_usernames

		# Preserve #s and @s
		preserve_symbols_values = ['none', 'both', '#', '@']
		if preserve_symbols.lower() not in preserve_symbols_values:
			self.preserve_symbols = 'none'
		else:
			self.preserve_symbols = preserve_symbols.lower()

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

	def _checkFileContents(self, fileData, filepath):
		"""Checks that the fileData from filepath contains, at minimum, 'text' 
		and 'user' keys and both keys are mapped to arrays of the same length.

		Arguments:
		fileData -- (dictionary) A dictionary parsed from a JSON file
		filepath -- (string) The file fileData was pulled from
		"""

		try: 
			keys = list(fileData.keys())
			assert 'text' in keys and 'user' in keys
			assert len(fileData['text']) == len(fileData['user'])
		
		except AssertionError:
			msg = filepath + ' has unacceptable data.'
			raise ValueError(msg)

	def _combineUsersAndText(self, users, text):
		"""Returns an array of tweet text in the same order as users[] and 
		text[]. Appends author username to the beginning of each tweet text 
		with an @ symbol so it can be included in the text analysis.
		"""
		combined = []
		for i in range (0, len(users)):
			combined.append('@' + users[i] + ' ' + text[i])
		return combined

	def load(self):
		for idx, category in enumerate(self.files):
			self.labels.append(category)

			if self.files[category]:
				filepath = self.data_folder + self.files[category]
				try:
					file = open(filepath)
					fileData = json.load(file)
					file.close()
				except IOError:
					msg = ("Couldn't open " + filepath + ". Are you sure the " + 
						  "file exists?")
					raise IOError(msg)
				except json.decoder.JSONDecodeError:
					file.close()
					msg = filepath + " is not formatted for JSON parsing."
					raise ValueError(msg)
				
				self._checkFileContents(fileData, filepath)

				if self.include_usernames:
					# Combine username and text
					combined_text = self._combineUsersAndText(fileData['user'], 
															  fileData['text'])
					self.data['x_str'].extend(combined_text)
				else:
					self.data['x_str'].extend(fileData['text'])

				catlist = [idx] * len(fileData['text'])
				self.data['y'].extend(catlist)

	def clean(self):
		"""
		Scikit has its own punctuation cleaning process that we can use if we
		want to strip ALL punctuation. clean() doesn't do anything but remove
		periods if this is the case-- it leaves the good stuff for scikit to
		do. 
		However, it's difficult to make scikit's tokenizer preserve some symbols
		like '#' and '@' and not others; it treats every non-character symbol as
		a token seperator by default. Therefore, if we want to preserve some of 
		the punctuation, we probably want to clean our tweets ourselves.
		"""

		# This might seem overkill, but I'm removing periods instead of 
		# replacing them with spaces to preserve abbreviations like "U.S.A." or
		# "U.N." If we replace periods with spaces, these abbreviations get
		# totally broken up and won't get included in the vocabulary by our
		# tokenizer.
		for idx, text in enumerate(self.data['x_str']):
			legend = {'.': None}
			self.data['x_str'][idx] = text.translate(str.maketrans(legend))
			if self.preserve_symbols != 'none':
				# Normalize text by converting characters like é to e and 
				# changing to all lowercase
				normText = unicodedata.normalize('NFKD', self.data['x_str'][idx]).lower()
				if self.preserve_symbols == '#':
					normText = re.sub(r"[^a-zA-Z0-9#]", " ", normText)
				elif self.preserve_symbols == '@':
					normText = re.sub(r"[^a-zA-Z0-9@]", " ", normText)
				elif self.preserve_symbols == 'both':
					normText = re.sub(r"[^a-zA-Z0-9@#]", " ", normText)
				self.data['x_str'][idx] = normText

	def split(self, percent_test=0.1, seed=None):
		data = pd.DataFrame.from_dict(self.data)
		params = {
			'test_size': percent_test,
			'shuffle': True,
			'random_state': None
		}
		if seed: params['random_state'] = seed
		self.train, self.test = train_test_split(data, **params)

	def vectorize(self, ngram_range):
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
		if self.preserve_symbols == 'none':
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

		# While we're at it, let's save the most-correlated features for each
		# category within the ngram range.
		self.correlated_features = {}
		for cat_id, category in enumerate(self.labels):
			features_chi2 = chi2(self.train_x_vect, np.array(self.train_y) == cat_id)
			indices = np.argsort(features_chi2[0])
			feature_names = np.array(vect.get_feature_names())[indices]
			self.correlated_features[category] = {}
			for n in range(ngram_range[0], ngram_range[1] + 1):
				self.correlated_features[category][n] = [v for v in feature_names if len(v.split(' ')) == n]

	def dump_vocabulary(self, filepath='vocab.json'):
		vocab_dict = pd.Series(self.vocabulary).to_dict()
		fp = open(filepath, 'w+')
		json.dump(vocab_dict, fp, indent=4)
		fp.close()