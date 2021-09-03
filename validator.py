MIN_ID_VAL = 0
MIN_LEN_NAME = 4

class Validator:

	def availability(self, availability: dict) -> bool:
		return availability != {}

	def name(self, name: str) -> bool:
		return len(name) > MIN_LEN_NAME

	def id(self, id) -> bool:
		return id > MIN_ID_VAL