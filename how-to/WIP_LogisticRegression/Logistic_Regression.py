from sklearn.linear_model import LogisticRegression

class Logistic_Regression():
	def __init__(self, solver):
		self.LR = LogisticRegression(solver=solver, multi_class='multinomial')
	def run(self, train_x, train_y, test_x, test_y):
		self.LR.fit(train_x, train_y)
		self.predicted = self.LR.predict(test_x)
		self.percent_score = self.LR.score(test_x, test_y) * 100