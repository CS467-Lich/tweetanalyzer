import sys
import traceback
import enum
import urllib.parse
import interface
import searchTweets
import sampleTweets

credentialsPath = '../twitter_credentials.json'
'''
outputJSON = 'data.json'
outputCSV = 'data.csv'
'''
outputJSON = './joinJSON/Ads_Positive/data.json'
outputCSV = './joinJSON/Ads_Positive/data.csv'

def main():
	method = interface.getSelection()
	numTweets = interface.getNumTweets(method)
	if method is interface.Selection.SEARCH:
		# Get query
		query = interface.getQuery()
		# Get result_type
		resultType = interface.getResultType()
		# Get Tweets
		searchTweets.searchTweets(credentialsPath, query, resultType, numTweets,
			outputJSON, outputCSV)
	elif method is interface.Selection.SAMPLE:
		sampleTweets.sampleTweets(credentialsPath, numTweets, outputJSON,
			outputCSV)
	else:
		raise ValueError('main(): Invalid tweet retrieval method selected.')
		sys.exit(1)


try:
	main()
except KeyboardInterrupt:
	print('\n' + '-' * 50)
	print('Exiting...')
	sys.exit(0)
except Exception:
	traceback.print_exc()