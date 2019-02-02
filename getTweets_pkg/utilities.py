import sys
import traceback
import json
import urllib.parse
import pandas as pd

def urlEncode(text):
	text.encode('utf-8')
	return urllib.parse.quote_plus(text)

def loadCreds(filepath):
	try:
		with open(filepath, 'r') as file:
			return json.load(file)
	except IOError:
		print("loadCreds(): File does not exist!")
		return 0

def writeAsJSON(filename, data):
	try:
		with open(filename, 'w') as outfile:
			json.dump(data, outfile, indent=4)
	except IOError:
		traceback.print_exc()
		sys.exit(1)

def writeAsCSV(filename, data):
	try:
		# Save to pandas DataFrame & sort by date descending
		df = pd.DataFrame.from_dict(data)
		df.sort_values(by='date', inplace=True, ascending=False)
		# Save to CSV
		df.to_csv(filename, index=False)
	except IOError:
		traceback.print_exc()
		sys.exit(1)