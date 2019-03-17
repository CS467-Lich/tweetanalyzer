# Retrieving Raw Tweet Data

This package integrates both tweet searching and streaming using the Twython wrapper for the Twitter API.

## Getting Started

### Confirm Python Version

Check that your Python version is at least 3.4.

```
$ python --version
```

If using flip, use:

```
$ python3 --version
```

### Installing Requirements

Make sure the requirements in 'requirements.txt' have been installed.

```
$ pip3 install -r requirements.txt
```

### twitter_credentials.json

The main method will look for your 'twitter_credentials.json' file in project root directory. If you need to change this, redefine the credentialsPath global variable at the beginning of 'main.py':
```
credentialsPath = ...
```

## Executing the Program

### main.py

There is one main method with a command line interface to guide you through collecting raw tweet data.

*(Note: If you are working on flip, replace any command to 'python' with 'python3'.)*

```
$ python main.py
```

Terminate the program at any time by hitting 'CTRL-C'.

### Sample vs. Search

The first prompt will ask you if you want to sample tweets at random or search for tweets by keyword.

```
1 - Sample tweets at random
2 - Search tweets by keyword
```

Enter '1' or 'sample' to stream random recent tweets.

Enter '2' or 'search' to enter a query to collect targeted tweets.

#### Sampling Tweets

The CLI will prompt you to enter how many tweets to stream. Since the streamer has to filter out non-English tweets, it's a bit slow. Therefore, we've capped the maximum number of tweets at 500 for initial testing. This may be adjusted in getNumTweets() in 'interface.py' if needed.

No further user input is needed. The stream will begin and save data to JSON and CSV when finished.


#### Searching Tweets

##### Max Count
The CLI will prompt you to enter the maximum number of tweets you will accept. The Twitter API may return fewer tweets than requested (especially if the result type is set to popular), but it will not exceed this number. You may search for up to 100 tweets. This upper limit is imposed by the Twitter Search API.

##### Query
See [this resource](https://developer.twitter.com/en/docs/tweets/rules-and-filtering/overview/standard-operators.html) to learn about the operators available for forming Twitter queries. 

You have the option to read a query from a text file or enter it at the command line. 
```
Would you like to import a complex query from a
plaintext file? (Enter Y or N) 
```

For very long or complicated queries, it may be easier to save the query as a text file and enter the file name at the command line. To improve readability, you may break up your query onto multiple lines in this file. When reading the file, the program will remove line breaks and replace them with spaces.

If your query is simple, like "dogs" or "@cats", entering your query at the command line may be more convenient.

##### Result Type

Twitter will return the most recent tweets resulting from your query, the most popular, or a mix of the two. However, note that requesting 'popular' tweets often results in Twitter returning fewer tweets than requested. Requesting 'recent' or 'mixed' tweets tends to result in more tweets.

```
Twitter can provide one of three types of results.
1 - recent
2 - popular
3 - mixed
```

To make a selection, enter either the number (e.g. '1') or the type (e.g. 'recent').

After specifying the max count, query, and result type, the program will retrieve the tweets and save them to JSON and CSV.
 
### Output Files

The CSV and JSON output file paths are defined at the start of 'main.py'. Redefine here if needed.

```
outputJSON = 'data.json'
outputCSV = 'data.csv'
```

**The code is currently set to overwrite any existing files.**
