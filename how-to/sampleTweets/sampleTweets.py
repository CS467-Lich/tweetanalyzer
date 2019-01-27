from twython import Twython
from twython import TwythonStreamer
import json
import datetime

counter = 0
tweets = []

# Redefine StreamListener class
class StreamListener(TwythonStreamer):
	
	def on_success(self, status):
		if 'lang' in status and status['lang'] == 'en':
			# Take only what we want from the results
			data = {}
			data['user'] = status['user']['screen_name']
			data['date'] = status['created_at']
			data['text'] = status['text']
			data['source'] = status['source']
			data['coordinates'] = status['coordinates']
			data['hashtags'] = status['entities']['hashtags']
			tweets.append(data)
			global counter
			counter += 1
			# Print counter every 25 tweets.
			if counter % 25 == 0:
				print(counter, ' collected...')

	def on_error(self, status_code, data):
		print(status_code)
		self.disconnect()


# Load credentials from JSON file
with open('../../twitter_credentials.json', 'r') as file:
    creds = json.load(file)
consumer_key = creds['CONSUMER_KEY']
consumer_secret = creds['CONSUMER_SECRET']
access_token = creds['ACCESS_TOKEN']
access_token_secret = creds['ACCESS_TOKEN_SECRET']

stream = StreamListener(consumer_key, consumer_secret, access_token, access_token_secret)

try:
	print('Beginning stream. Hit Ctrl-C to stop...')
	stream.statuses.sample()
except KeyboardInterrupt:
	stream.disconnect()
	print('Stream disconnected. Tweets Saved: ', counter)
	with open('sample_output.json', 'w') as file:
		json.dump(tweets, file, indent=4)
except ValueError as error:
	logger.error(error)
	raise