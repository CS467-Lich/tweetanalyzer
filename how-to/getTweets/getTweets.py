# First things first, make sure you've installed twython and pandas:
# pip install twython pandas

from twython import Twython
import json
import pandas as pd


from helperFunctions import writeAsJSON

DIRECTORY = "Activism_Environmental"
#TWITTER_SEARCH = ['yoga', 'crossfit', 'run', 'fitness', 'lifting', 'cardio', 'rock climbing', 'PR', 'MMA', 'boxing', 'dance']
TWITTER_SEARCH = ['global warming', 'pollution', 'waste', 'ozone layer', 'water', 'earth', 'climate change', 'plastic', 'marine life', 'turtles', 'deforestation', 'overpopulation', 'biodiversity', 'endangered', 'extinct', 'lanfill']

# Load credentials from JSON file
with open('twitter_credentials.json', 'r') as file:
    creds = json.load(file)
print('CONSUMER_KEY = ' + creds['CONSUMER_KEY'])
print('CONSUMER_SECRET = ' + creds['CONSUMER_SECRET'])

# Get access token
twitter = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'], oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(creds['CONSUMER_KEY'], access_token=ACCESS_TOKEN)

# Send search request to Twitter
i = 0
results = {}
while (len(TWITTER_SEARCH)) > i:

    JSON_SAVE_FILE = "joinJSON/" + DIRECTORY + "/data" + str(i + 1) + ".json" 
    results.update(twitter.search(q=TWITTER_SEARCH[i], result_type='mixed', lang='en', count='25'))

    # Take only what we want from the results (just a couple attributes for now)
    dict_ = {'user': [], 'date': [], 'text': [], 'source': [], 'coordinates': [], 'language': [], 'hashtags': []}
    for status in results['statuses']:
        dict_['user'].append(status['user']['screen_name'])
        dict_['date'].append(status['created_at'])
        dict_['text'].append(status['text'])
        dict_['source'].append(status['source'])
        dict_['coordinates'].append(status['coordinates'])
        dict_['language'].append(status['lang'])
        dict_['hashtags'].append(status['entities']['hashtags'])


    # save data in json form to json file
    writeAsJSON(dict_, JSON_SAVE_FILE) 


    # Use pandas to structure data as a DataFrame. This isn't necessary for
    # just viewing the data, but would likely be necessary for any sort of 
    # analysis with pandas. Plus pandas has a nifty to_csv() function for
    # DataFrames.
    df = pd.DataFrame.from_dict(dict_)
    df.sort_values(by='date', inplace=True, ascending=False)
    i = i + 1

# Results to console
# print("Results Preview:")
# print(df)

# Results to CSV ('index=False' means don't save the dataframe line index--
# it's useless to us)
# df.to_csv('test_output.csv', index=False)

# References:
# https://stackabuse.com/accessing-the-twitter-api-with-python/
# https://twython.readthedocs.io/en/latest/usage/starting_out.html#oauth-2-application-authentication
