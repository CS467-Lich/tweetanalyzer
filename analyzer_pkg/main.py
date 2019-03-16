"""
Tweet Analyzer
by Emily Hamilton, Cord Meados, and Sandhya Raman
CS467 - Winter 2019
Oregon State University
"""

import sys
import os
import traceback
import modules.Config as config
import modules.UI as ui
import modules.Dataset as data
import modules.Spinner as spinner
import modules.Plots as plots
import modules.LR as LR
import modules.NB as NB
import modules.SVM as SVM

DEBUG = False

DEFAULTS = {
	"config_file": "config.ini",
	"subdir": "data",
	"files": {
			"Activism": "activism.json",
			"Advertising": "ads.json",
			"Comedy": "comedy.json",
			"Fitness": "fitness.json",
			"Politics": "politics.json",
			"Technology": "tech.json"
	},
	"test_train_split": (20, 80),
	"vectorizer": "count",
	"max_ngram": 2,
	"preserve_symbols": True,
	"remove_stopwords": True
}


################################################################################
# ERROR HANDLERS
################################################################################

def fatal_error(msg):
	print(msg, file=sys.stderr)
	sys.exit(1)

def excepthook(type_, value, tb):
	print("Uncaught Exception:", type_)
	print("Message:", value)
	traceback.print_tb(tb)
	sys.exit(1)

################################################################################
# HELPERS
################################################################################

def get_Dataset(settings):
	dataset = data.Dataset(settings["subdir"], settings["files"], 
						   vectorizer=settings["vectorizer"], 
						   remove_stopwords=settings["remove_stopwords"],
						   preserve_symbols=settings["preserve_symbols"])
	dataset.load()
	dataset.clean()
	dataset.split(settings["test_train_split"][0] / 100)
	dataset.vectorize(ngram_range=(1, settings["max_ngram"]))
	return dataset

def printMostCorrelatedNgrams(dataset, num_to_print=5):
	for category in dataset.correlated_features.keys():
		print("# {}:".format(category))
		for n in dataset.correlated_features[category].keys():
			print("- Features of length {}:".format(n))
			print('\t' + "\n\t".join(dataset.correlated_features[category][n][-num_to_print:]))
		print('')

def run_LR(dataset):
	# Run LR with spinner-- will take a little bit.
	model = LR.Logistic_Regression()
	spinner_msg = "Running Logistic Regression on tweet data..."
	spinner.spinnerTask(model.run, dataset.train_x_vect, dataset.train_y, 
						dataset.test_x_vect, dataset.test_y, message=spinner_msg)
	return model

def run_NB(dataset):
	# Run NB with spinner-- may take a little bit.
	model = NB.Naive_Bayes()
	spinner_msg = "Running Naive-Bayes on tweet data..."
	spinner.spinnerTask(model.run, dataset.train_x_vect, dataset.train_y, 
						dataset.test_x_vect, dataset.test_y, message=spinner_msg)
	return model

def run_SVM(dataset):
	# Run SVM with spinner-- may take a little bit.
	model = SVM.SVM()
	spinner_msg = "Running SVM on tweet data..."
	spinner.spinnerTask(model.run, dataset.train_x_vect, dataset.train_y, 
						dataset.test_x_vect, dataset.test_y, message=spinner_msg)
	return model


################################################################################
# Main Method
################################################################################
def main():
	# Load settings from config file or global DEFAULTS if file absent
	try:
		settings = config.parse_settings(**DEFAULTS)
		if DEBUG: print(settings)
	except Exception as e:
		fatal_error(str(e))

	# Title
	ui.print_title()

	while True:
		# Initial Menu: 1 = run analysis, 2 = reset config file to defaults
		menu_choice = ui.initial_menu()
		if DEBUG: print("Menu Choice:", menu_choice)
		
		# 1 = Run Analysis
		if menu_choice == 1:
			# Ask user for algorithm: 1 = LR, 2 = NB, 3 = SVM, 4 = All
			alg_choice = ui.choose_analysis()
			if DEBUG: print("Alg Choice: ", alg_choice)

			# Ask for destination directory for output
			output_dir = ui.get_output_dir()
			if DEBUG: print("Output Subdirectory:", output_dir)

			input("\n<Press ENTER to begin.>")

			# Create output directory
			while os.path.exists(output_dir):
				output_dir += ("_copy")
			os.makedirs(output_dir)

			# Initialize dataset
			spinner_msg = "Loading dataset..."
			dataset = spinner.spinnerTask(get_Dataset, settings, message=spinner_msg)
			print("\nTraining Set's Most-Correlated Features by Category:\n")
			printMostCorrelatedNgrams(dataset)

			# Save bar graph to output directory
			plots.barGraph(output_dir, dataset.data, dataset.labels)			

			# Hang here to give user a chance to inspect console output.
			input("<Press ENTER to proceed with analysis.>")

			# Run 1 or more analyses and save outputs...
			
			# Logistic Regression
			if alg_choice == 1 or alg_choice == 4:
				model = run_LR(dataset)
				print("Logistic Regression % Accuracy:", model.percent_score)
				plots.confusionMatrix(subfolder=output_dir,
									  alg_name="Logistic Regression",
									  alg_abbrev="LR",
									  labels=dataset.labels, 
									  test_y=dataset.test_y, 
									  predicted_y=model.predicted, 
									  normalized=True, 
									  total_score=model.percent_score)

			# Naive-Bayes
			if alg_choice == 2 or alg_choice == 4:
				model = run_NB(dataset)
				print("Naive-Bayes % Accuracy:", model.percent_score)
				plots.confusionMatrix(subfolder=output_dir,
									  alg_name="Naive-Bayes",
									  alg_abbrev="NB",
									  labels=dataset.labels, 
									  test_y=dataset.test_y, 
									  predicted_y=model.predicted, 
									  normalized=True, 
									  total_score=model.percent_score)

			# SVM
			if alg_choice == 3 or alg_choice == 4:
				model = run_SVM(dataset)
				print("SVM % Accuracy:", model.percent_score)
				plots.confusionMatrix(subfolder=output_dir,
									  alg_name="SVM",
									  alg_abbrev="SVM",
									  labels=dataset.labels, 
									  test_y=dataset.test_y, 
									  predicted_y=model.predicted, 
									  normalized=True, 
									  total_score=model.percent_score)

			# Ask user to quit or start over-- helpful for PyInstaller
			# executable so console will remain open until user wants it to 
			# close instead of closing immediately upon program termination.
			if ui.quit_menu() == 2:
				break
		else:
			# 2 = Reset Config File:
			config.restore_configfile(**DEFAULTS)
			print("\nSettings in 'config.ini' have been reset to default values.")
		
		# Loop back to main menu


################################################################################
# Program Execution
################################################################################
if __name__ == "__main__":
	sys.excepthook = excepthook		# Handler for uncaught exceptions

	try:
		main()
	except KeyboardInterrupt:
		print("\n\nExiting...")
		sys.exit(0)