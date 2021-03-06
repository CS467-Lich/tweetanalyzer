"""
Test SVM
This is a SVM test. The goal is to learn how to make an SVM with data
    where the outcome is known, so any bugs in the code can be more easily identified.
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
#########################################################################################

# plot data to test
# plt.scatter(x1_coords, x2_coords, c=clazz)
# plt.show()

#########################################################################################
# prepare input function to put data into estimator
#########################################################################################
def input_fn_train():
    # Prep data
    features = np.hstack((x1_coords, x2_coords))
    labels = clazz

    # Convert data to Dataset class
    ds = tf.data.Dataset.from_tensor_slices((features, labels))

    return ds

def input_fn_dumb_test():
    return tf.tuple(2, 1)



# labels = np.array([2, 1])
# print(labels)
#########################################################################################
# Define the feature columns
#########################################################################################
x1 = tf.feature_column.numeric_column('x1')
x2 = tf.feature_column.numeric_column('x2')

#########################################################################################
# Instantiate the relevant pre-made Estimator
#########################################################################################
estimator = tf.estimator.LinearClassifier(feature_columns=['x1', 'x2'])

#########################################################################################
# Train the estimator
#########################################################################################
estimator.train(input_fn=input_fn_train, steps=1)






# References
# https://www.tensorflow.org/guide/estimators
# https://www.tensorflow.org/guide/datasets
# https://www.tensorflow.org/guide/datasets_for_estimators
# https://www.tensorflow.org/api_docs/python/tf/convert_to_tensor
# https://www.tensorflow.org/guide/custom_estimators
# https://www.tensorflow.org/tutorials/estimators/linear
# https://adventuresinmachinelearning.com/tensorflow-dataset-tutorial/
# https://towardsdatascience.com/how-to-use-dataset-in-tensorflow-c758ef9e4428
# https://medium.com/ymedialabs-innovation/how-to-use-dataset-and-iterators-in-tensorflow-with-code-samples-3bb98b6b74ab
