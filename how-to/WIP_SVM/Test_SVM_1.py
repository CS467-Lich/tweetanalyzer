"""

This didn't work. Bad guide, bad idea, deprecated code.

"""


"""
Test SVM
This is a SVM using iris data. The goal is to learn how to make and SVM with data
    where the outcome is known, so any bugs in the code can be more easily identified.
Cord Meados 2019
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf


#########################################################################################
# Prepare random points to test SVM
#########################################################################################
min_y = min_x = -5
max_y = max_x = 5
x_coords = np.random.uniform(min_x,max_x, (500, 1))
y_coords = np.random.uniform(min_y, max_y, (500,1))
clazz = np.greater(y_coords, x_coords).astype(int)
delta = 0.5 / np.sqrt(2.0)
x_coords = x_coords + ((0 - clazz) * delta) + ((1-clazz) * delta)
y_coords = y_coords + (clazz * delta) + ((clazz - 1) * delta)
#########################################################################################

# plot data to test
plt.plot(x_coords, y_coords, 'bo')
plt.show()

def input_fn():
    return{
        'example_id': tf.constant(map(lambda x: str(x + 1), np.arange(len(x_coords)))),
        'x': tf.constant(np.reshape(x_coords, [x_coords.shape[0],1])),
        'y': tf.constant(np.reshape(y_coords, [y_coords.shape[0], 1])),
    }, tf.constant(clazz)

#########################################################################################
# All this stuff is deprecated. I'll try pasting and running to see what happens.
#########################################################################################
#feature1 = tf.contrib.layers.real_valued_column('x')
#feature2 = tf.contrib.layers.real_valued_column('y')
#svm_classifier = tf.contrib.learn.SVM(
#  feature_columns=[feature1, feature2],
#  example_id_column='example_id')
# svm_classifier.fit(input_fn=input_fn, steps=30)
#metrics = svm_classifier.evaluate(input_fn=input_fn, steps=1)
#print("Loss", metrics['loss'], "\nAccuracy", metrics['accuracy'])


#########################################################################################

# https://ml-with-tensorflow.info/2017/03/01/svm-with-tensorflow/
# https://matplotlib.org/gallery/lines_bars_and_markers/arctest.html#sphx-glr-gallery-lines-bars-and-markers-arctest-py
# https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib-pyplot-plot