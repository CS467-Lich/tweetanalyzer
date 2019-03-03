"""
Test SVM
This is a SVM test. The goal is to learn how to make an SVM with data
    where the outcome is known, so any bugs in the code can be more easily identified.
    This will closely follow Test_SVM_3_LinearRegression_Guide
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
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split

print(tf.__version__)

# only displays the most important warnings
tf.logging.set_verbosity(tf.logging.FATAL)

#########################################################################################
# Prepare random points to test SVM
#########################################################################################
min_y = min_x = -5
max_y = max_x = 5
x1_coords = np.random.uniform(min_x,max_x, (500, 1))
x2_coords = np.random.uniform(min_y, max_y, (500,1))
clazz = np.greater(x2_coords, x1_coords).astype(int)
delta = 0.5 / np.sqrt(2.0)
x1_coords = x1_coords + ((0 - clazz) * delta) + ((1-clazz) * delta)
x2_coords = x2_coords + (clazz * delta) + ((clazz - 1) * delta)

# rename clazz
target = clazz
# Combine features into one variable
features = np.hstack((x1_coords, x2_coords))
# Turn features and target into a pandas dataframe. That's easier to work with.
features = pd.DataFrame(features,columns=['x1', 'x2'])
target = pd.DataFrame(target)
# print(features.head())
# print(target.head())

# Get train and test splits
X_train, X_test, y_train, y_test = train_test_split(
     features, target, test_size=0.33, random_state=42)

#print(X_train.iat[0,0])
#print(type(X_train.iat[0,0]))
#print(type(X_train))
#########################################################################################

# plot data to test
# plt.scatter(x1_coords, x2_coords, c=clazz)
# plt.show()

#########################################################################################
# prepare input functions to put data into estimator
#########################################################################################
input_fn_train = tf.estimator.inputs.pandas_input_fn(x=X_train,
                                               y=y_train,
                                               batch_size=32,
                                               shuffle= True,
                                               num_epochs = None)
#print(type(input_fn_train()))
#print(input_fn_train())

input_fn_test = tf.estimator.inputs.pandas_input_fn(x=X_test,
                                               y=y_test,
                                               batch_size=32,
                                               shuffle=False,
                                               num_epochs=1)

#########################################################################################
# Define the feature columns
#########################################################################################
numeric_columns = ['x1', 'x2']
numeric_features = [tf.feature_column.numeric_column(key=column) for column in numeric_columns]

#########################################################################################
# Instantiate the relevant pre-made Estimator
#########################################################################################
linear_classifier = tf.estimator.LinearClassifier(feature_columns=numeric_features)

#########################################################################################
# Train the estimator
#########################################################################################
#print(type(X_train))
#print(X_train.iat[0,0])
#print(type(X_train.iat[0,0]))
linear_classifier.train(input_fn=input_fn_train, steps=50)

#########################################################################################
# Test the estimator
#########################################################################################
#results = linear_classifier.evaluate(input_fn=input_fn_test)
#print(results)




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
