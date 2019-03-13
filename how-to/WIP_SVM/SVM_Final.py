"""
SVM tensorflow
This is the SVM implementation in tensorflow.
Cord Meados 2019
"""


"""###########################################################
https://www.tensorflow.org/guide/estimators

Four steps with estimators:
1. Training
2. Evaluation
3. Prediction
4. Export for Serving

"""###########################################################

import numpy as np
import matplotlib.pyplot as plt
import json
import tensorflow as tf
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from class_Finder import classification

print(tf.__version__)

# only displays the most important warnings
tf.logging.set_verbosity(tf.logging.FATAL)

#########################################################################################
# Prepare data
#########################################################################################

# pull data from json files and turn into pandas DataFrame
with open('Data/Activism_Final_Positive.json') as f:
    act_data = json.load(f)
    act_data = act_data['text']
    act_df = pd.DataFrame(act_data)
with open('Data/Ads_Final_Positive.json') as f:
    ads_data = json.load(f)
    ads_data = ads_data['text']
    ads_df = pd.DataFrame(ads_data)
with open('Data/Fitness_Final_Positive.json') as f:
    fit_data = json.load(f)
    fit_data = fit_data['text']
    fit_df = pd.DataFrame(fit_data)
with open('Data/Humour_Final_Positive.json') as f:
    hum_data = json.load(f)
    hum_data = hum_data['text']
    hum_df = pd.DataFrame(hum_data)
with open('Data/Political_Final_Positive.json') as f:
    pol_data = json.load(f)
    pol_data = pol_data['text']
    pol_df = pd.DataFrame(pol_data)
with open('Data/Tech_Final_Positive.json') as f:
    tec_data = json.load(f)
    tec_data = tec_data['text']
    tec_df = pd.DataFrame(tec_data)

# combine dataframes
data_df = act_df.append(ads_df, ignore_index=True)
data_df = data_df.append(fit_df, ignore_index=True)
data_df = data_df.append(hum_df, ignore_index=True)
data_df = data_df.append(pol_df, ignore_index=True)
data_df = data_df.append(tec_df, ignore_index=True)

# we'll get a binary classification matrix for each tweet.
act_clazz = classification('Activism')
ads_clazz = classification('Ads')
fit_clazz = classification('Fitness')
hum_clazz = classification('Humour')
pol_clazz = classification('Political')
tec_clazz = classification('Tec')


# create the vectorizer so we can turn this text into a bag of words.
data_series = data_df.T.squeeze() #turn the dataframe into a series for vectorizer
vectorizer = CountVectorizer(strip_accents='ascii', ngram_range=(1,2))
vectorizer.fit(data_series) # .fit() finds every unique word to create a word array
vector = vectorizer.transform(data_series) # transform creates our array
vectorArray = vector.toarray()

#reshape the data
numeric_columns = vectorizer.get_feature_names()
print(numeric_columns[0])
print(vectorArray[:, 0])
print(vectorArray[0])
X = {}
for i in range(0, np.size(vectorArray, 1)):
    X[numeric_columns[i]] = vectorArray[:, i]

print(X)


X_train_act, X_test_act, y_train_act, y_test_act = train_test_split(X, act_clazz, train_size=0.8)
#X_train_ads, X_test_ads, y_train_ads, y_test_ads = train_test_split(vectorArray, ads_clazz, train_size=0.8)
#X_train_fit, X_test_fit, y_train_fit, y_test_fit = train_test_split(vectorArray, fit_clazz, train_size=0.8)
#X_train_hum, X_test_hum, y_train_hum, y_test_hum = train_test_split(vectorArray, hum_clazz, train_size=0.8)
#X_train_pol, X_test_pol, y_train_pol, y_test_pol = train_test_split(vectorArray, pol_clazz, train_size=0.8)
#X_train_tec, X_test_tec, y_train_tec, y_test_tec = train_test_split(vectorArray, tec_clazz, train_size=0.8)


#########################################################################################
# prepare input functions to put data into estimator
#########################################################################################

input_fn_train = tf.estimator.inputs.numpy_input_fn(x=X_train_act, y=y_train_act, batch_size=10, num_epochs=4, shuffle=True)


#########################################################################################
# Define the feature columns
#########################################################################################
#numeric_columns = vectorizer.get_feature_names()
numeric_features = [tf.feature_column.numeric_column(key=column) for column in numeric_columns]

#########################################################################################
# Instantiate the relevant pre-made Estimator
#########################################################################################
linear_classifier = tf.estimator.LinearClassifier(feature_columns=numeric_features)

#########################################################################################
# Train the estimator
#########################################################################################
linear_classifier.train(input_fn=input_fn_train, steps=50)

#########################################################################################
# Test the estimator
#########################################################################################
results = linear_classifier.evaluate(input_fn=input_fn_train)
print(results)




# References
# https://medium.com/learning-machine-learning/introduction-to-tensorflow-estimators-part-1-39f9eb666bc7
# https://www.tensorflow.org/guide/estimators
# https://www.tensorflow.org/guide/datasets
# https://www.tensorflow.org/guide/datasets_for_estimators
# https://www.tensorflow.org/api_docs/python/tf/convert_to_tensor
# https://www.tensorflow.org/guide/custom_estimators
# https://www.tensorflow.org/tutorials/estimators/linear
# https://adventuresinmachinelearning.com/tensorflow-dataset-tutorial/
# https://towardsdatascience.com/how-to-use-dataset-in-tensorflow-c758ef9e4428
# https://medium.com/ymedialabs-innovation/how-to-use-dataset-and-iterators-in-tensorflow-with-code-samples-3bb98b6b74ab
# https://towardsdatascience.com/getting-data-into-tensorflow-estimator-models-3432f404a8da
