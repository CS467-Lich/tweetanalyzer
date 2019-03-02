from sklearn.metrics import confusion_matrix
from numpy import newaxis
import matplotlib.pyplot as plt
import seaborn as sns

def confusionMatrix(subfolder, labels, test_y, predicted_y, normalized=True, total_score=None):
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