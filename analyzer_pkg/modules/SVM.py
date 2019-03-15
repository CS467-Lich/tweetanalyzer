"""
Cord Meados
"""

from sklearn.svm import LinearSVC

class SVM():
	def __init__(self):
		""" Simply a wrapper around scikit's LinearSVC class 
		constructor.
		"""
		self.SVM = LinearSVC()
	def run(self, x_train_vect, y_train, x_test_vect, y_test):
		""" Fits the vectorized training data (x_train_vect) and corresponding
		category codes (y_train) to the linear SVC model. Uses resulting
		model to predict category codes for vectorized test data (x_test_vect).

		Outcomes:
			1. self.SVM = a fitted LinearSVC model
			2. self.predicted (list) of prediced y-values for each x_test_vect
			   value
			3. self.percent_score = total percent accuracy (between 0 and 100)
			   for prediced y-values vs actual y-values (y_test) for all
			   categories combined
		"""
		self.SVM.fit(x_train_vect, y_train)
		self.predicted = self.SVM.predict(x_test_vect)
		self.percent_score = self.SVM.score(x_test_vect, y_test) * 100