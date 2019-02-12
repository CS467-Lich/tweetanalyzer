from twython import Twython
import json
import pandas as pd
import utilities


def connect(credentialsPath):
	# Load credentials and create Twython instance
	creds = utilities.loadCreds(credentialsPath)
	twitter = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
		oauth_version=2)
	
	# Get access token & authorize
	ACCESS_TOKEN = twitter.obtain_access_token()
	twitter = Twython(creds['CONSUMER_KEY'], access_token=ACCESS_TOKEN)

	return twitter


def dataToTable(data):
	tweets = {'user': [], 'date': [], 'text': [], 'source': [],
			'coordinates': [], 'language': [], 'hashtags': []}
	for status in data['statuses']:
		tweets['user'].append(status['user']['screen_name'])
		tweets['date'].append(status['created_at'])
		tweets['text'].append(status['full_text'])
		tweets['source'].append(status['source'])
		tweets['coordinates'].append(status['coordinates'])
		tweets['language'].append(status['lang'])
		tweets['hashtags'].append(status['entities']['hashtags'])
	return tweets


# Alternative to saving to table for dataframe-- array of dicts. Not currently
# used anywhere, but included just in case.
def dataToObjectArray(data):
	tweets = []
	for status in data['statuses']:
		# Take only what we want from the results
		twt = {}
		twt['user'] = status['user']['screen_name']
		twt['date'] = status['created_at']
		twt['text'] = status['full_text']
		twt['source'] = status['source']
		twt['coordinates'] = status['coordinates']
		twt['language'] = status['lang']
		twt['hashtags'] = status['entities']['hashtags']
		tweets.append(twt)
	return tweets


def searchTweets(credentialsPath, query, resultType, maxCount, outfileJSON, 
	outfileCSV):

	twitter = connect(credentialsPath)
	print('\nConnected to Twitter...')

	print('\nBeginning search...')
	results = twitter.search(q=query, result_type=resultType,
		count=str(maxCount), lang='en', tweet_mode='extended')
	print('Search complete.')

	data = dataToTable(results)

	# save to JSON
	utilities.writeAsJSON(outfileJSON, data)

	# save to CSV
	utilities.writeAsCSV(outfileCSV, data)

	print('\nResults saved to ' + outfileJSON + ' and ' + outfileCSV + '.')