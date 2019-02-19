import sys
import json
from jsonmerge import Merger


acceptableKeys = ['user', 'date', 'text', 'coordinates', 'source', 'language',
				  'hashtags']


def fatalError(errorMsg='Fatal Error: Undefined'):
	"""Outputs the string `errorMsg` to stderr and exits with code 1.

	Arguments:
	errorMsg -- (string) Message to print (default 'Fatal Error: Undefined')
	"""

	print('Fatal Error: ' + errorMsg, file=sys.stderr)
	sys.exit(1)


def getBaseDict():
	"""Returns a dict with the keys 'tweet' and 'category'. The value for each
	key is an empty array.
	"""
	d = {}
	d['tweet'] = []
	d['category'] = []
	return d


def checkFileContents(data, originFilepath):
	"""Checks that the `data` created from parsing the JSON file located at
	`originFilepath` contains the expected keys defined in the global
	`acceptableKeys` array and also checks that the arrays for all keys have
	the same length.

	Arguments:
	data -- (dictionary) A dictionary parsed from a JSON file
	originFilepath -- (string) The file `data` was pulled from
	"""
	try:
		global acceptableKeys
		keys = list(data.keys())
		assert len(keys) is len(acceptableKeys)	# Check that data has expected
												# number of keys.
		arrayLength = len(data[keys[0]])	# Get length of array corresponding
									# to arbitrary key. All arrays should have
									# the same length, so it doesn't matter
									# which key.
		for key in keys:
			assert key in acceptableKeys	# Check that key is ok.
			assert arrayLength == len(data[key])	# Check that array is the
													# expected length.
	
	except AssertionError:
		fatalError(originFilepath + ' has unacceptable data.')
	

def combineUsersAndText(users, text):
	tweets = []
	for i in range (0, len(users)):
		tweets.append('@' + users[i] + ' ' + text[i])
	return tweets


def stitch(dataFolder, files):
	"""Returns a dictionary containing the combined tweets and their categories
	from ./datafolder/files. Each tweet is formed using an '@' symbol, the user,
	a space, and then the tweet text.

	Imports data from the JSON files named in the `files` array located in 
	the subdirectory `dataFolder` and combines them into a single dictionary.
	All the JSON files must be of the format:
	{
		'key': [...],
		'key2': [...],
		<etc.>
	}
	IMPORTANT: Each of the arrays is expected to have the same number of 
	elements.

	Arguments:
	dataFolder -- (string) The subfolder where the files in `files` are
		located
	files -- (array of strings) An array of file names containing JSON objects
		of key/value pairs to stitch together.
	"""
	combinedData = getBaseDict()

	for category in files:
		if files[category]:
			filepath = dataFolder + files[category]
			try:
				file = open(filepath)
				fileData = json.load(file)
				file.close()
			except IOError:
				fatalError('Couldn\'t open ' + filepath + '. Are you sure ' +
					'the file exists?')
			except json.decoder.JSONDecodeError:
				file.close()
				fatalError(filepath + ' is not properly formatted for JSON ' +
					'parsing.')
			
			checkFileContents(fileData, filepath)
			# Combine username and text and add the category
			tweets = combineUsersAndText(fileData['user'], fileData['text'])
			combinedData['tweet'].extend(tweets)
			catlist = [category] * len(fileData['user'])
			combinedData['category'].extend(catlist)

	return combinedData