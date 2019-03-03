"""
Test SVM
This is a LR test. The goal is to learn how to make an LR with Tensorflow
    to learn more and move onto a classifier.
Cord Meados 2019
https://medium.com/learning-machine-learning/introduction-to-tensorflow-estimators-part-1-39f9eb666bc7
"""

import tensorflow as tf
print(tf.__version__)

"""
Linear Regression from Scratch
"""

# Model Parameters
W = tf.Variable([3.0],name='weight')
b = tf.Variable([-2.0],name='bias')

# Model inputs
# training data
X = tf.placeholder(tf.float32)
# y
Y = tf.placeholder(tf.float32)

# Model definition
predictions = W*X + b

# loss function. Here we use sum of squared errors.
loss = tf.reduce_sum(tf.square(predictions-Y))

# training op
train = tf.train.GradientDescentOptimizer(0.001).minimize(loss)

# train data
x = [1.1,2.0,3.5,4.8]
y = [2.0,3.4,4.2,5.1]

sess = tf.Session()
sess.run(tf.global_variables_initializer())
for train_step in range(2000):
    sess.run(train, {X: x, Y: y})

weight, bias, loss = sess.run([W, b, loss], {X:x, Y:y})
# print("W: %s b: %s loss: %s"%(weight,bias,loss))

"""
Working with Canned Estimators
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("seaborn-colorblind")
# %matplotlib inline
# only displays the most important warnings
tf.logging.set_verbosity(tf.logging.FATAL)

# Define Features and pull data
used_features = ['property_type','room_type','bathrooms','bedrooms','beds','bed_type','accommodates','host_total_listings_count'
                ,'number_of_reviews','review_scores_value','neighbourhood_cleansed','cleaning_fee','minimum_nights','security_deposit','host_is_superhost',
                 'instant_bookable', 'price']

boston = pd.read_csv('boston_listings.csv', usecols = used_features)
# print(boston.shape)
# boston.head(2)

# Scrub the data
for feature in ["cleaning_fee", "security_deposit", "price"]:
    boston[feature] = boston[feature].map(lambda x: x.replace("$", '').replace(",", ''), na_action='ignore')
    boston[feature] = boston[feature].astype(float)
    boston[feature].fillna(boston[feature].median(), inplace=True)

for feature in ["bathrooms", "bedrooms", "beds", "review_scores_value"]:
    boston[feature].fillna(boston[feature].median(), inplace=True)

boston['property_type'].fillna('Apartment', inplace=True)

# Data is skewed, so we will remove anything below 50 and above 500
boston = boston[(boston["price"]>50)&(boston["price"]<500)]
target = np.log(boston.price)
target.hist()
plt.title("Price distribution after the subsetting and log-transformation")
features = boston.drop('price',axis=1)
features.head()
# print(features.head())
# print(target.head())

# split data into train, test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
     features, target, test_size=0.33, random_state=42)

"""
debug
"""
X_print = X_train.iat[0, 2]
#print(X_train.head())
#print(X_print)
#print(type(X_print))
#print(type(X_print))
"""
debug
"""

# Get all the numeric feature names
numeric_columns = ['host_total_listings_count','accommodates','bathrooms','bedrooms','beds',
 'security_deposit','cleaning_fee','minimum_nights','number_of_reviews',
 'review_scores_value']
# Get all the categorical feature names that contains strings
categorical_columns = ['host_is_superhost','neighbourhood_cleansed','property_type','room_type','bed_type','instant_bookable']

# Create numeric feature columns
numeric_features = [tf.feature_column.numeric_column(key = column) for column in numeric_columns]
# print(numeric_features[0])

# Create categorical feature columns using one hot representation
categorical_features = [tf.feature_column.categorical_column_with_vocabulary_list(key = column,
                                                                                 vocabulary_list = features[column].unique())
                                                                                for column in categorical_columns]
# print(categorical_features[3])

# Combine numeric and categorical feature columns
linear_features = numeric_features + categorical_features

# Create training input function
training_input_fn = tf.estimator.inputs.pandas_input_fn(x = X_train,
                                                        y=y_train,
                                                        batch_size=32,
                                                        shuffle= True,
                                                        num_epochs = None)
print(type(training_input_fn()))
print(training_input_fn())
# create testing input function
eval_input_fn = tf.estimator.inputs.pandas_input_fn(x=X_test,
                                                    y=y_test,
                                                    batch_size=32,
                                                    shuffle=False,
                                                    num_epochs = 1)

# Instantiate the model. This creates the estimator and defines the expected feature columns.
linear_regressor = tf.estimator.LinearRegressor(feature_columns=linear_features,
                                                model_dir = "linear_regressor")


# Train the estimator
linear_regressor.train(input_fn = training_input_fn,steps=2000)

# evaluate the model.
results = linear_regressor.evaluate(input_fn = eval_input_fn)
# print("Loss is " + str(loss))
# print(results)

#Get predictions from test set
pred = list(linear_regressor.predict(input_fn = eval_input_fn))
pred = [p['predictions'][0] for p in pred]
prices = np.exp(pred)
# print(prices)

# checking variable names
v_names = linear_regressor.get_variable_names()[5:10]
# print(v_names)

