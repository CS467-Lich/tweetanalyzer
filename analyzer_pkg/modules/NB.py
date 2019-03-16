"""
Sandhya Raman
"""
from sklearn.naive_bayes import MultinomialNB

class Naive_Bayes():
	def __init__(self):
		""" Simply a wrapper around scikit's MultinomialNB class constructor.
		"""
		self.MultinomialNB = MultinomialNB()
	def run(self, x_train_vect, y_train, x_test_vect, y_test):
		""" Fits the vectorized training data (x_train_vect) and corresponding
		category codes (y_train) to the multinomial NB model. Uses resulting
		model to predict category codes for vectorized test data (x_test_vect).

		Outcomes:
			1. self.MultinomialNB = a fitted NB model
			2. self.predicted (list) of prediced y-values for each x_test_vect
			   value
			3. self.percent_score = total percent accuracy (between 0 and 100)
			   for prediced y-values vs actual y-values (y_test) for all
			   categories combined
		"""
		self.MultinomialNB.fit(x_train_vect, y_train)
		self.predicted = self.MultinomialNB.predict(x_test_vect)
		self.percent_score = self.MultinomialNB.score(x_test_vect, y_test) * 100