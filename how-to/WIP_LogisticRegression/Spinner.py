import threading
import sys
import time

class Spinner:
	""" Spinner class modified from:
	https://stackoverflow.com/questions/4995733/how-to-create-a-spinning-command-line-cursor
	and referencing:
	https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
	"""

	@staticmethod
	def __spinning_cursor():
		while True:
			for cursor in '|/-\\':
				yield cursor

	def __init__(self):
		self.__stop = threading.Event()
		self.spinner = self.__spinning_cursor()

	def __displaySpinner(self, message=''):
		sys.stdout.write(message + ' ')
		sys.stdout.flush()
		while not self.__stop.is_set():
			sys.stdout.write(next(self.spinner))
			sys.stdout.flush()
			time.sleep(0.1)
			sys.stdout.write('\b')
			sys.stdout.flush()

	def start(self, message=''):
		self.__spin = True
		thread = threading.Thread(target=self.__displaySpinner, args=(message,))
		self.__thread = thread
		thread.start()

	def stop(self):
		self.__stop.set()
		self.__thread.join()
		sys.stdout.write('\n')
		sys.stdout.flush()

def spinnerTask(task, *args, message=''):
		spinner = Spinner()
		try:
			msg = '\n' + message
			spinner.start(msg)
			returned = task(*args)
		except KeyboardInterrupt:
			spinner.stop()
			print('\nExiting...')
			sys.exit(0)
		except Exception as e:
			spinner.stop()
			raise e
		spinner.stop()
		del spinner
		return returned