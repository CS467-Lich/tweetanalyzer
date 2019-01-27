'''
Make sure requests and pandas are installed:
pip install requests pandas
'''
import pandas as pd
import json
from twitter_api import get_access_token, twitter_search

# Load credentials from JSON file
with open('../../twitter_credentials.json', 'r') as file:
	creds = json.load(file)

KEY = creds['CONSUMER_KEY']
SECRET = creds['CONSUMER_SECRET']

# Request access token from Twitter
response = get_access_token(KEY, SECRET)
ACCESS_TOKEN = response['access_token']

# Send query. 'q' is required, but other search params are optional. See
# https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
# for complete list of available parameters.
results = twitter_search(ACCESS_TOKEN, q='dogs', result_type='mixed', 
						 count='50')

print(results['statuses'])
print(results['search_metadata'])

# TODO - Add saving to CSV