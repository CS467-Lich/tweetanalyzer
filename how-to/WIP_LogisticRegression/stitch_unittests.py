import unittest
import sys
from io import StringIO
from stitch_funcs import stitch

DATA_FOLDER = 'Unit_Test_Files/'

class TestBadInput(unittest.TestCase):

	global DATA_FOLDER

	def testFileWithBadKey(self):
		"""This test makes sure stitch() will appropriately reject a file with 
		the proper JSON format, but with an unacceptable key (stitch() will 
		only accept files containing JSON objects with all the keys 'user', 
		'date', 'text', 'coordinates', 'source', 'language', 'hashtags').
		"""
		
		files = {
			'BadKey': 'bad_key.json'
		}

		consoleOutput = StringIO()
		sys.stderr = consoleOutput
		with self.assertRaises(SystemExit) as sysexit:
			combinedData = stitch(DATA_FOLDER, files)	# call stitch() on file
		sys.stderr = sys.__stderr__
		
		# Is exit code correct?
		self.assertEqual(sysexit.exception.code, 1)

		# Is error message correct?
		expectedText = 'has unacceptable data'
		self.assertIn(expectedText, consoleOutput.getvalue())
	

	def testNotParseableFile(self):
		"""This test makes sure stitch() will appropriately reject a file whose
		contents aren't really parseable as JSON.
		"""

		files = {
			'BadFile': 'bad_file.json'
		}

		consoleOutput = StringIO()
		sys.stderr = consoleOutput
		with self.assertRaises(SystemExit) as sysexit:
			combinedData = stitch(DATA_FOLDER, files)	# call stitch() on file
		sys.stderr = sys.__stderr__
		
		# Is exit code correct?
		self.assertEqual(sysexit.exception.code, 1)

		# Is error message correct?
		expectedText = 'not properly formatted for JSON parsing'
		self.assertIn(expectedText, consoleOutput.getvalue())


	def testAbsentFile(self):
		"""This test makes sure stitch() will appropriately handle a request to
		open a file that doesn't exist.
		"""

		files = {
			'NonexistantFile': 'not_there.json'
		}

		consoleOutput = StringIO()
		sys.stderr = consoleOutput
		with self.assertRaises(SystemExit) as sysexit:
			combinedData = stitch(DATA_FOLDER, files)	# call stitch() on file
		sys.stderr = sys.__stderr__
		
		# Is exit code correct?
		self.assertEqual(sysexit.exception.code, 1)

		# Is error message correct?
		expectedText = 'Couldn\'t open'
		self.assertIn(expectedText, consoleOutput.getvalue())


class TestGoodFiles(unittest.TestCase):
	def testThis(self):
		files = {
			'Activism': 'activism_test.json',
			'Advertisement': 'ads_test.json',
			'Fitness': 'fitness_test.json',
			'Humor': 'humor_test.json',
			'Political': 'political_test.json',
			'Technology': 'tech_test.json'	
		}

		# stub
		self.assertEqual(1,1)



if __name__ == '__main__':
	unittest.main()


'''
SOURCES:
* https://docs.python.org/3/library/unittest.html
* https://stackoverflow.com/questions/15672151/is-it-possible-for-a-unit-test-to-assert-that-a-method-calls-sys-exit
* https://stackoverflow.com/questions/33767627/python-write-unittest-for-console-print
'''