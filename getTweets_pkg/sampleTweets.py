import sys
import traceback
from twython import TwythonStreamer
import json
import pandas as pd
import utilities

counter = 0
target = 0
data = {'user': [], 'date': [], 'text': [], 'source': [],
		'coordinates': [], 'language': [], 'hashtags': []}

# Redefine StreamListener class
class StreamListener(TwythonStreamer):
	
	def on_success(self, status):
		global data
		global counter
		if counter < target and 'lang' in status and status['lang'] == 'en':
			# Take only what we want from the results
			data['user'].append(status['user']['screen_name'])
			data['date'].append(status['created_at'])
			data['text'].append(status['text'])
			data['source'].append(status['source'])
			data['coordinates'].append(status['coordinates'])
			data['language'].append(status['lang'])
			data['hashtags'].append(status['entities']['hashtags'])
			counter += 1
			# Print progress every 25 tweets.
			if counter % 25 == 0:
				print(counter, ' collected...')
		elif counter >= target:
			print(counter, ' collected. FINISHED!')
			self.disconnect()

	def on_error(self, status_code, data):
		print(status_code)
		self.disconnect()

def connect(credentialsPath):
	creds = utilities.loadCreds(credentialsPath)
	stream = StreamListener(creds['CONSUMER_KEY'],
							creds['CONSUMER_SECRET'],
							creds['ACCESS_TOKEN'],
							creds['ACCESS_TOKEN_SECRET'])
	return stream

def sampleTweets(credentialsPath, count, outfileJSON, outfileCSV):
	global data
	global counter
	global target
	target = count
	stream = connect(credentialsPath)
	try:
		print('Beginning stream...')
		stream.statuses.sample()
		utilities.writeAsJSON(outfileJSON, data)
		utilities.writeAsCSV(outfileCSV, data)
		print('\nResults saved to ' + outfileJSON + ' and ' + outfileCSV + '.')
	except KeyboardInterrupt:
		stream.disconnect()
		print('Stream disconnected prematurely. Tweets retrieved: ', counter)
		utilities.writeAsJSON(outfileJSON, data)
		utilities.writeAsCSV(outfileCSV, data)
		print('\nResults saved to ' + outfileJSON + ' and ' + outfileCSV + '.')
	except Exception:
		traceback.print_exc()
		sys.exit(1)