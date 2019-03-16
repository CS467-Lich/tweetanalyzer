"""
This file contains function for plotting our data.

Plots modified from:
https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import seaborn as sns
from sklearn.metrics import confusion_matrix
from numpy import newaxis

def barGraph(subfolder, combinedData, labels):
	""" Plots the count of tweets in each category as a simple bar graph.
	
	Arguments:
		subfolder = a string representing the subdirectory in the program's
			working directory where the user wants to save output files
		combinedData = a dict with keys 'x_str' and 'y' where both keys have
			the same number of values
		labels = the array of string label names such that each value of y 
			corresponds to an index in labels

	Outcomes:
		Saves the plot to the subfolder as "category_distribution.png"
	"""
	plt.clf()
	df = pd.DataFrame.from_dict(combinedData)
	label_dict = dict(enumerate(labels))
	df['y'] = df['y'].map(label_dict)
	fig = plt.figure(figsize=(10,11))
	df.groupby('y').x_str.count().plot.bar(ylim=0)
	plt.title("All Data (Train & Test Sets) by Category ", fontsize='xx-large', pad=40)
	plt.ylabel("Qty Tweets", fontsize='large', labelpad=20)
	plt.xlabel("Category", fontsize='large', labelpad=20)
	plt.savefig(subfolder + "/category_distribution.png")

def confusionMatrix(subfolder, alg_abbrev, labels, alg_name, test_y, predicted_y, 
					normalized=True, total_score=None):
	""" Plots a confusion matrix of real y-values (test_y) vs predicted y-values
	(predicted_y).
	
	Arguments:
		subfolder = a string representing the subdirectory in the program's
			working directory where the user wants to save output files
		alg_abbrev = a short string differentiating the algorithm from other
			algorithms like "LR" for Logistic Regression; used in the file name
		labels = the array of string label names such that each value of y 
			corresponds to an index in labels
		alg_name = a string containing the algorithm name as it should appear
			in the plot's title.
		test_y = the actual y-values for the test split
		predicted_y = the predicted y-values for the test split
		normalized = boolean; whether or not the values printed on the confusion
			matrix should be a count (False) or percentage all Tweets for a
			category (True)
		total_score = the total percent accuracy for the algorithm (included in
			the subtitle); could probably be calculated from test_y vs.
			predicted_y, but we've already computed this value so why do it 
			again?

	Outcomes:
		Saves the plot to the subfolder as "confusion_matrix_{alg_abbrev}.png"
	"""
	plt.clf()
	c_matrix = confusion_matrix(test_y, predicted_y)
	if normalized:
		c_matrix = c_matrix.astype('float') / c_matrix.sum(axis=1)[:, newaxis]
	fig, ax = plt.subplots(figsize=(10,10))
	palette = sns.cubehelix_palette(40, start=1, rot=-.75, dark=.2, light=.95)
	params = {
		'annot': True,
		'xticklabels': labels,
		'yticklabels': labels,
		'cmap': palette
	}
	if not normalized:
		params['fmt']='g'
	sns.heatmap(c_matrix, **params)
	plt.ylabel("Actual Category", fontsize='large', labelpad=20)
	plt.xlabel("Predicted Category", fontsize='large', labelpad=20)
	if total_score:
		plt.title("{0} Confusion Matrix".format(alg_name), fontsize='xx-large', pad=40)
		plt.figtext(0.3, 
					0.9, 
					("Accuracy for All Categories: " + str(round(total_score, 4)) + "%"), 
					fontstyle='italic',
					fontsize='large')
	else:
		plt.title("Confusion Matrix", fontsize='xx-large', pad=20)
	plt.savefig(subfolder + "/confusion_matrix_" + alg_abbrev + ".png")