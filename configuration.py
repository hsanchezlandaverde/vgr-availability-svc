import os

DEFAULT_PORT = 8092

class Configuration:

	def __init__(self):
		self.debug = False
		self.port = DEFAULT_PORT

	def fromEnv(self):
		debug = os.getenv('DEBUG_ENABLED') == 'True'
		port = os.getenv('PORT')
		if debug:
			self.debug = debug
		if port is not None and isinstance(port, int):
			self.port = port
		return self
