import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import seaborn as sns

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
	