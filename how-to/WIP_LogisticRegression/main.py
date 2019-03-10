import sys
import os
from Logistic_Regression import *
from Spinner import *
from Dataset import *
from Plots import *

# Set DEBUG_MODE=True to make the data split the same way every time (should
# yield same % accuracy every time) and print some debug information to the 
# console.
DEBUG_MODE = False

DATA_FOLDER = 'Final_Positives/'
FILES = {
	'Activism': 'Activism_Final_Positive.json',
	'Advertisement': 'Ads_Final_Positive.json',
	'Fitness': 'Fitness_Final_Positive.json',
	'Humor': 'Humour_Final_Positive.json',
	'Political': 'Political_Final_Positive.json',
	'Technology': 'Tech_Final_Positive.json'
}
TEST_SIZE = 0.15
SPLIT_SEED = 123
MAX_NGRAM = 3

def getData():
	dataset = Dataset(DATA_FOLDER, FILES, vectorizer='CountVectorizer',
		remove_stopwords=False, include_usernames=True, preserve_symbols='both')
	dataset.load()
	dataset.clean()
	if DEBUG_MODE:
		dataset.split(TEST_SIZE, seed=SPLIT_SEED)
	else:
		dataset.split(TEST_SIZE)
	dataset.vectorize(ngram_range=(1, MAX_NGRAM))
	dataset.dump_vocabulary('vocabulary.json')
	return dataset

def printMostCorrelatedNgrams(dataset, num_to_print=5):
	for category in dataset.correlated_features.keys():
		print("# %s:" % category)
		for n in dataset.correlated_features[category].keys():
			print("- Most-correlated features of length %d:" % n)
			print('\t' + "\n\t".join(dataset.correlated_features[category][n][-num_to_print:]))
		print('')

if __name__ == '__main__':
	spinner_msg = "Loading dataset..."
	dataset = spinnerTask(getData, message=spinner_msg)

	if DEBUG_MODE:
		print("#" * 80)
		print("DATASET SETTINGS:")
		print("-" * 80)

		print("Data Folder: ", dataset.data_folder)
		print("Files: ", dataset.files)
		print("Vectorizer: ", dataset.vectorizer)
		print("Remove stopwords? ", dataset.remove_stopwords)
		print("Include usernames? ", dataset.include_usernames)
		print("Symbols to preserve: ", dataset.preserve_symbols)

		print("Labels: ", dataset.labels)

		print("Train:")
		print(dataset.train.head(5))
		print("x_str: ", dataset.train.x_str.shape)
		print("train_x_vect: ", dataset.train_x_vect.shape)
		print("y: ", dataset.train.y.shape)

		print("\nTest:")
		print(dataset.test.head(5))
		print("x_str: ", dataset.test.x_str.shape)
		print("test_x_vect: ", dataset.test_x_vect.shape)
		print("y: ", dataset.test.y.shape)
		
		print("#" * 80)

	# Run LR with spinner-- will take a little bit.
	model = Logistic_Regression('lbfgs')
	spinner_msg = "Running Logistic Regression on tweet data..."
	spinnerTask(model.run, dataset.train_x_vect, dataset.train_y, 
				dataset.test_x_vect, dataset.test_y, message=spinner_msg)
	
	
	# Print 5 most-correlated ngrams for each category
	printMostCorrelatedNgrams(dataset, num_to_print=5)

	# Total Score
	print("\nPercent of test tweets accurately categorized: ", 
		  model.percent_score)

	# Plots
	plots_subfolder = "plots"
	if not os.path.exists(plots_subfolder):
		os.mkdir(plots_subfolder)

	# Save confusion matrix
	confusionMatrix(plots_subfolder, dataset.labels, dataset.test_y, 
					model.predicted, normalized=True, 
					total_score=model.percent_score)

	barGraph(plots_subfolder, dataset.data, dataset.labels)