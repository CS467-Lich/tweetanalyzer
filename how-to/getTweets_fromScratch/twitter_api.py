'''
This module contains functions for accessing the Twitter Search API.
'''
import urllib.parse
import base64
import json
import requests			# requires installation



'''
key: string		(Consumer Key provided by Twitter)
secret: string	(Consumer Secret provided by Twitter)

Returns string version of base64 encoded 'key:secret' token
required by Twitter OAuth 2.0 auth flow.
'''
def base64_encode(key, secret):
	# URL-encoding per RFC1738 is recommended by Twitter in case
	# they implement future key/secret pairs that do not contain
	# standard characters, but it does not currently change the
	# values of the key and secret. Encoding below is on a 'just
	# in case' basis.
	creds = urllib.parse.quote_plus(key) + ':' + urllib.parse.quote_plus(secret)
	# Twitter requires above credentials to be encoded in base 64.
	creds_64 = base64.b64encode(creds.encode())
	return creds_64.decode()



'''
base64_creds: string		(base 64 encoding of 'KEY:SECRET')

Returns dict containing 'token_type' and 'access_token' if successful,
'errors' if unsuccessful.
'''
def twitter_auth(base64_creds):
	auth_endpoint = 'https://api.twitter.com/oauth2/token'
	headers = {
		'Authorization': 'Basic ' + base64_creds,
		'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
	}
	payload = 'grant_type=client_credentials'
	try:
		res = requests.post(auth_endpoint, headers=headers, data=payload)
		# Return dict parsed from from JSON object returned by Twitter.
		return json.loads(res.text)
	except ValueError as error:
		logger.error(error)
		raise



'''
key: string		(Consumer Key provided by Twitter)
secret: string	(Consumer Secret provided by Twitter)

Sends consumer key and secret to Twitter in exchange for a Bearer
token. Returns dict containing 'token_type' and 'access_token' if 
successful, 'errors' if unsuccessful.
'''
def get_access_token(key, secret):
	creds_64 = base64_encode(key, secret)
	response = twitter_auth(creds_64)
	if 'errors' in response:
		raise ValueError(response['errors'])
	else:
		return response


'''
Required Params:
	q: string		(Twitter Search query-- see
					https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
					for guidelines.)
Optional Params:	(See https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
					for descriptions)
	geocode: string
	lang: string
	locale: string
	result_type: string
	count: string
	until: string
	since_id: string
	max_id: string
	include_entities=''

Returns the URL to use to search Twitter based on the provided arguments.
'''
def build_search_url(q, geocode='', lang='', locale='', result_type='', 
					 count='', until='', since_id='', max_id='', 
					 include_entities=''):
	search_endpoint = 'https://api.twitter.com/1.1/search/tweets.json'

	if not q:
		raise ValueError('Must include query.')
	
	url = search_endpoint + '?q=' + urllib.parse.quote_plus(q)

	# Attach optional parameters
	if geocode:
		url = url + '&geocode=' + urllib.parse.quote_plus(geocode)
	if lang:
		url = url + '&lang=' + urllib.parse.quote_plus(lang)
	if locale:
		url = url + '&locale=' + urllib.parse.quote_plus(locale)
	if result_type:
		url = url + '&result_type=' + urllib.parse.quote_plus(result_type)
	if count:
		url = url + '&count=' + urllib.parse.quote_plus(count)

	if until:
		url = url + '&until=' + urllib.parse.quote_plus(until)

	if since_id:
		url = url + '&since_id=' + urllib.parse.quote_plus(since_id)

	if max_id:
		url = url + '&max_id=' + urllib.parse.quote_plus(max_id)

	if include_entities:
		include_entities_enc = urllib.parse.quote_plus(include_entities)
		url = url + '&include_entities=' + include_entities_enc

	return url

'''
Required Params:
	access_token: string	(Valid access token obtained from Twitter)
	q: string		(Twitter Search query-- see
					https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
					for guidelines.)
Optional Params:	(See https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
					for descriptions)
	geocode: string
	lang: string
	locale: string
	result_type: string
	count: string
	until: string
	since_id: string
	max_id: string
	include_entities=''

	Builds query from provided arguments and sends to Twitter. Returns results
	in the format specified by:
	https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html#example-response
'''
def twitter_search(access_token, q, geocode='', lang='', locale='', 
				   result_type='', count='', until='', since_id='', max_id='', 
				   include_entities=''):
	url = build_search_url(q, geocode, lang, locale, result_type, count, until,
						   since_id, max_id, include_entities)
	headers = {
		'Authorization': 'Bearer ' + access_token 
	}
	res = requests.get(url, headers=headers)
	return json.loads(res.text)