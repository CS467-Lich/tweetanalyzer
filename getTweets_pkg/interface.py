import sys
import traceback
import enum
import utilities

class Selection(enum.Enum):
	SAMPLE = 1
	SEARCH = 2

def getSelection():
	print('*' * 50)
	print('\t\t  GET TWEETS')
	print('*' * 50)
	print('1 - Sample tweets at random')
	print('2 - Search tweets by keyword')
	print('-' * 50)
	while True:
		method = input('Enter Selection: ')
		if method.lower() == 'sample' or method == '1':
			return Selection.SAMPLE
		elif method.lower() == 'search' or method == '2':
			return Selection.SEARCH

def getNumTweets(method):
	msg = None
	MIN_TWEETS = 1
	MAX_TWEETS = None
	if (method is Selection.SEARCH):
		msg = 'Enter maximum number of results to accept: '
		MAX_TWEETS = 100	# Defined by Twitter API.
	elif (method is Selection.SAMPLE):
		msg = 'Enter number of tweets to stream: '
		MAX_TWEETS = 500	# Defined by us-- could be changed.
	else:
		raise ValueError('getNumTweets() cannot accept ' + str(method)  +
			' as an argument.')
	while True:
		numTweets = input(msg)
		if numTweets.isdigit() and int(numTweets) >= MIN_TWEETS and \
		   int(numTweets) <= MAX_TWEETS:
			return int(numTweets)

def isComplexQuery():
	while True:
		qtype = input('Would you like to import a complex query from a\n' + 
			'plaintext file? (Enter Y or N) ');
		if qtype.lower() == 'y' or qtype.lower() == 'yes':
			return True
		elif qtype.lower() == 'n' or qtype.lower() == 'no':
			return False

def getFile():
	filename = input('Enter file path/name: ')
	try:
		file = open(filename, "r")
		return file
	except IOError:
		print("getFile(): File does not exist!")
		return 0

def readFile(fileDescriptor):
	try: 
		contents = fileDescriptor.read()
		# replace newlines and carriage returns with spaces
		contents = contents.replace('\r\n', ' ')
		contents = contents.replace('\n', ' ')
		return contents
	except IOError:
		traceback.print_exc()
		sys.exit(1)

def getQuery():
	if (isComplexQuery()):
		while True:
			file = getFile()
			if (file != 0):
				query = readFile(file)
				file.close()
				return utilities.urlEncode(query)
	else:
		query = input('Enter query (e.g. keyword, hashtag, etc.): ')
		return utilities.urlEncode(query)

def getResultType():
	print('Twitter can provide one of three types of results.')
	print('1 - recent')
	print('2 - popular')
	print('3 - mixed')
	while True:
		resultType = input('Enter choice: ')
		if resultType == '1' or resultType.lower() == 'recent':
			return 'recent'
		elif resultType == '2' or resultType.lower() == 'popular':
			return 'popular'
		elif resultType == '3' or resultType.lower() == 'mixed':
			return 'mixed'
