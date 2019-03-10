import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import seaborn as sns
from sklearn.metrics import confusion_matrix
from numpy import newaxis

def barGraph(subfolder, combinedData, labels):
	plt.clf()
	df = pd.DataFrame.from_dict(combinedData)
	label_dict = dict(enumerate(labels))
	df['y'] = df['y'].map(label_dict)
	colors = []

	fig = plt.figure(figsize=(10,11))
	df.groupby('y').x_str.count().plot.bar(ylim=0)
	plt.title("All Data (Train & Test Sets) by Category ", fontsize='xx-large', pad=40)
	plt.ylabel("Qty Tweets", fontsize='large', labelpad=20)
	plt.xlabel("Category", fontsize='large', labelpad=20)
	plt.savefig(subfolder + "/category_counts.png")

def confusionMatrix(subfolder, labels, test_y, predicted_y, normalized=True, total_score=None):
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
		plt.title("Confusion Matrix", fontsize='xx-large', pad=40)
		plt.figtext(0.3, 
					0.9, 
					("Accuracy for All Categories: " + 
					 str(round(total_score, 4)) + "%"), 
					fontstyle='italic',
					fontsize='large')
	else:
		plt.title("Confusion Matrix", fontsize='xx-large', pad=20)
	plt.savefig(subfolder + "/confusion_matrix.png")