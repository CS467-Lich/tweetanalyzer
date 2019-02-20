"""
Tensor flow hello world.
Cord Meados
2019
https://medium.com/ai-india/hello-world-tensorflow-6ce3f5bcbb6b
"""

import tensorflow as tf

#################################################################
# Just disables a warning, doesn't enable AVX/FMA
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#################################################################


sess = tf.Session()

# Create Tensorflow object to hold an input string
x = tf.placeholder(tf.string)
y = tf.placeholder(tf.int32)
z = tf.placeholder(tf.float32)

with tf.Session() as sess:
    # Run the tf.placeholder operation in the session
    output = sess.run(x, feed_dict={x: 'Test String', y: 123, z: 45.67})
    print(output)


