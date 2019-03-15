"""
This file contains functions for interpreting and resetting the config INI file.
This file contains some "advanced" settings that the user can choose to
manipulate or ignore.
"""

import os
import configparser
import re
from pathlib import Path

def restore_configfile(**defaults):
	""" Writes a default version of the project's config file the program's
	working directory. Overwrites existing file or saves new file if one does 
	not already exist. Expects the following keys in defaults, at minimum:
		"test_train_split" (tuple of ints)
		"vectorizer" (string)
		"preserve_symbols" (bool)
		"remove_stopwords" (bool)
		"config_file" (string) 
	"""
	default_file_contents = ("################################################"
							 "################################\n"
							 "#  ADVANCED SETTINGS                            "
							 "                               #\n"
							 "################################################"
							 "################################\n\n"
							 "[DATASET PROCESSING]\n"
							 "\tTest-Train Split:\t\t{test}, {train}\n"
							 "\tVectorizer:\t\t\t\t{vect}\n\n"
							 "[TEXT PROCESSING]\n"
							 "\tKeep # and @ Symbols:\t{symbols}\n"
							 "\tRemove Stopwords:\t\t{stopwords}\n"
							 .format(test=defaults["test_train_split"][0],
							 		 train=defaults["test_train_split"][1],
							 		 vect=defaults["vectorizer"],
							 		 symbols=defaults["preserve_symbols"],
							 		 stopwords=defaults["remove_stopwords"]
							 		 )
							 )
	file = open(defaults["config_file"], "w+")
	file.write(default_file_contents)
	file.close()

def parse_settings(**defaults):
	""" Parses the config file specified in defaults dict for user-configured 
	advanced settings. If no config file is located, it creates a new one with
	default settings in the root directory.
	Expects the following keys in defaults, at minimum:
		"config_file" (string)
		"test_train_split" (tuple of ints)
		"vectorizer" (string)
		"preserve_symbols" (bool)
		"remove_stopwords" (bool)
		"config_file" (string) 
	"""
	settings = defaults.copy()

	if (Path(defaults["config_file"]).is_file()):
		# Config file exists-- update settings.
		config = configparser.ConfigParser()
		config.read(defaults["config_file"])
		try: 
			split = config["DATASET PROCESSING"]["Test-Train Split"].split()
			settings["vectorizer"] = config["DATASET PROCESSING"]["Vectorizer"].lower()
			settings["preserve_symbols"] = config["TEXT PROCESSING"]["Keep # and @ Symbols"].lower()
			settings["remove_stopwords"] = config["TEXT PROCESSING"]["Remove Stopwords"].lower()
		except KeyError as e:
			msg = "(config.ini) Error: Section {key} missing from config file.".format(key=str(e))
			raise KeyError(msg)

		try:
			settings["test_train_split"] = (int(re.sub("[^0-9]", "", split[0])),
											int(re.sub("[^0-9]", "", split[1])))
		except:
			msg = "(config.ini) Error: Test-Train Split must be two numbers."
			raise ValueError(msg)

		try:
			# Check some conditions...
			assert settings["test_train_split"][0] + \
				   settings["test_train_split"][1] == 100, \
				   "(config.ini) Error: Sum of integers in Test-Train Split must be 100."
			assert settings["vectorizer"] == "count" or \
				   settings["vectorizer"] == "tfidf" or \
				   settings["vectorizer"] == "tf-idf", \
				   "(config.ini) Error: Vectorizer must be 'count' or 'tfidf'."
			assert settings["preserve_symbols"] == "true" or \
				   settings["preserve_symbols"] == "false", \
				   "(config.ini) Error: 'Remove Stopwords' must be 'true' or 'false'."
			assert settings["remove_stopwords"] == "true" or \
				   settings["remove_stopwords"] == "false", \
				   "(config.ini) Error: 'Remove Stopwords' must be 'true' or 'false'."
		except AssertionError as e:
			# Repackage any assertion errors as value errors and raise
			raise ValueError(str(e))
		
	else:
		# File doesn't exist. Use defaults passed and generate new config file.
		restore_configfile(**defaults)

	return settings