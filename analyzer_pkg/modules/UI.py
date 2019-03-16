"""
This file contains functions that implement parts of our CLI.
"""

import time

def print_title():
	""" Prints program title block to the console.
	"""
	title = ("{0}\n"
			 "#{1}TWEET ANALYZER{1}#\n"
			 "#{2}#\n"
			 "#{3}Project Team Lich{4}#\n"
			 "#{4}CS467 - Winter 2019{5}#\n"
			 "{0}\n"
			).format(_num_chars("#", 80), _num_chars(" ", 32), \
					 _num_chars(" ", 78), _num_chars(" ", 31), \
					 _num_chars(" ", 30), _num_chars(" ", 29))

	subtitle = ("\n{0}\n{1}Select <Ctrl-C> at any time to quit.{1}\n{0}") \
				.format(_num_chars("-", 80), _num_chars(" ", 22))
	print(title, subtitle)

def initial_menu():
	""" Prints initial menu and retrieves numeric choice from user. Returns
	the number of the choice.
	"""
	msg = ("\n{bar}\nMENU:\n\n"
		   "[1] Analyze Data\n"
		   "[2] Reset Config File to Defaults\n{bar}\n"
		   "Enter Choice: "
		  ).format(bar=_num_chars("-", 80))
	return _get_choice(msg, 1, 2)

def choose_analysis():
	""" Prints analysis menu and retrieves numeric choice from user. Returns
	the number of the choice.
	"""
	msg = ("\n{bar}\nPlease select type of analysis...\n\n"
		   "[1] Logistic Regression\n"
		   "[2] Naive-Bayes Algorithm\n"
		   "[3] SVM (Support Vector Machine)\n"
		   "-or-\n"
		   "[4] Run all three\n{bar}\n"
		   "Enter Choice: "
		  ).format(bar=_num_chars("-", 80))
	return _get_choice(msg, 1, 4)

def get_output_dir():
	""" Prints directory choice menu and retrieves output directory name from 
	user if user chooses to define one. Otherwise, returns a directory name
	of the format "output_YYYYMMDD_HHMMSS" using system time.
	"""
	while True:
		msg = "\nName subdirectory for program output? (Y/N) "
		if _get_YN(msg):
				directory = input("Output Subdirectory Name: ")
				print("You entered '{}'.".format(directory))
				if _get_YN("Is this correct? (Y/N) "):
					break
		else: 
			directory = "output_" + time.strftime("%Y%m%d_%H%M%S")
			break
	return directory

def quit_menu():
	""" Asks the user if (s)he wants to quit the program and returns a bool
	value (yes=True, no=False).
	"""
	msg = ("\n{bar}\n[1] Return to Main Menu\n"
		   "[2] Quit\n{bar}\n"
		   "Enter: "
		   ).format(bar=_num_chars("-", 80))
	return _get_choice(msg, 1, 2)


################################################################################
# UI Helpers
################################################################################
def _num_chars(char, n):
	""" Returns a string of n characters (char) in sequence.
	"""
	return char * n

def _get_choice(msg, min_, max_):
	""" Prompts user for input until an integer between min_ and max_ 
	(inclusive) is provided. Returns the integer.
	"""
	while True:
		choice = input(msg)
		if not choice.isdigit() or int(choice) < min_ or int(choice) > max_:
			msg = "Please choose a valid number: "
		else:
			return int(choice)

def _get_YN(msg):
	""" Prompts user for input until 'y', 'yes', 'n', or 'no' is provided.
	Returns a bool value (yes=True, no=False).
	"""
	while True:
		choice = input(msg)
		acceptable = {"y": True, "yes": True, "n": False, "no": False}
		if choice.lower() in acceptable:
			return acceptable[choice]
		else:
			msg = "Please enter Y or N: "